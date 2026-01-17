/**
 * ============================================
 * STEP 2: Job Scraper Service
 * ============================================
 * 
 * File: backend/services/jobScraperService.ts
 * 
 * Orchestrates job scraping, parsing, and validation
 */

import { Job } from '../models/Job'
import { ScrapingLog } from '../models/ScrapingLog'
import JSearchClient from './jsearchClient'
import { Logger } from '../utils/logger'

interface ParsedJob {
  title: string
  company: string
  location: string
  salary?: {
    min: number
    max: number
    currency: string
    period: string
  }
  description: string
  requirements: string[]
  preferredSkills: string[]
  employment_type: string
  is_remote: boolean
  apply_url: string
  external_id: string
  source: string
  source_metadata: {
    scraped_at: Date
    raw_response: any
    extraction_method: string
    confidence: number
  }
}

export class JobScraperService {
  private jsearchClient: JSearchClient
  private logger: Logger

  constructor(jsearchClient: JSearchClient, logger?: Logger) {
    this.jsearchClient = jsearchClient
    this.logger = logger || new Logger('JobScraperService')
  }

  /**
   * Main scraping function
   * Searches for jobs and returns parsed results
   */
  async scrapeJobs(query: string, country: string = 'in'): Promise<ParsedJob[]> {
    try {
      this.logger.info(`🔍 Starting scrape for: "${query}" in ${country}`)

      // Call JSearch API
      const rawJobs = await this.jsearchClient.searchJobs({
        query,
        country,
        page: 1,
        num_pages: 1,
        date_posted: 'month',
        employment_types: 'FULLTIME'
      })

      this.logger.info(`✅ Got ${rawJobs.length} raw jobs`)

      // Parse each job
      const parsedJobs = await Promise.all(
        rawJobs.map(rawJob => this.parseJobResponse(rawJob))
      )

      return parsedJobs
    } catch (error) {
      this.logger.error(`❌ Scraping error: ${error}`)
      throw error
    }
  }

  /**
   * Parse raw API response into standardized format
   */
  private async parseJobResponse(rawJob: any): Promise<ParsedJob> {
    try {
      // Extract location
      const location = this.extractLocation(rawJob)

      // Extract salary
      const salary = this.extractSalary(rawJob)

      // Extract skills and requirements
      const { requirements, preferredSkills } = this.extractSkills(rawJob)

      // Create parsed job object
      const parsedJob: ParsedJob = {
        title: rawJob.job_title || 'N/A',
        company: rawJob.employer_name || 'N/A',
        location,
        salary,
        description: rawJob.job_description || '',
        requirements,
        preferredSkills,
        employment_type: rawJob.job_employment_type || 'FULLTIME',
        is_remote: rawJob.job_is_remote === true,
        apply_url: rawJob.job_apply_link || '',
        external_id: rawJob.job_id,
        source: 'jsearch',
        source_metadata: {
          scraped_at: new Date(),
          raw_response: rawJob,
          extraction_method: 'api',
          confidence: 95
        }
      }

      return parsedJob
    } catch (error) {
      this.logger.warn(`Failed to parse job: ${error}`)
      // Return minimal parsed job
      return {
        title: rawJob.job_title || 'Unknown',
        company: rawJob.employer_name || 'Unknown',
        location: 'Unknown',
        description: rawJob.job_description || '',
        requirements: [],
        preferredSkills: [],
        employment_type: 'FULLTIME',
        is_remote: false,
        apply_url: rawJob.job_apply_link || '',
        external_id: rawJob.job_id,
        source: 'jsearch',
        source_metadata: {
          scraped_at: new Date(),
          raw_response: rawJob,
          extraction_method: 'api',
          confidence: 50 // Lower confidence due to parse error
        }
      }
    }
  }

  /**
   * Extract location from API response
   */
  private extractLocation(rawJob: any): string {
    const parts = []

    if (rawJob.job_city) parts.push(rawJob.job_city)
    if (rawJob.job_state) parts.push(rawJob.job_state)
    if (rawJob.job_country) parts.push(rawJob.job_country)

    if (parts.length === 0) {
      // Fallback: extract from description
      const locationMatch = rawJob.job_description?.match(
        /location:?\s*([^,\n]+)/i
      )
      return locationMatch ? locationMatch[1].trim() : 'Unknown'
    }

    return parts.join(', ')
  }

  /**
   * Extract salary information
   */
  private extractSalary(rawJob: any): ParsedJob['salary'] {
    const min = rawJob.job_min_salary
    const max = rawJob.job_max_salary
    const currency = rawJob.job_salary_currency || 'USD'
    const period = rawJob.job_salary_period || 'YEAR'

    if (min && max) {
      return { min, max, currency, period }
    }

    if (min || max) {
      return {
        min: min || 0,
        max: max || min || 0,
        currency,
        period
      }
    }

    return undefined
  }

  /**
   * Extract skills and requirements
   */
  private extractSkills(rawJob: any): {
    requirements: string[]
    preferredSkills: string[]
  } {
    const requirements = rawJob.job_required_skills || []
    const preferredSkills = []

    // Parse description for common skills
    const description = (rawJob.job_description || '').toLowerCase()
    const commonSkills = [
      'javascript',
      'typescript',
      'python',
      'java',
      'c++',
      'react',
      'angular',
      'vue',
      'node.js',
      'express',
      'mongodb',
      'sql',
      'docker',
      'kubernetes',
      'aws',
      'gcp',
      'azure',
      'git',
      'rest api',
      'graphql'
    ]

    for (const skill of commonSkills) {
      if (description.includes(skill) && !requirements.includes(skill)) {
        preferredSkills.push(skill)
      }
    }

    return { requirements, preferredSkills }
  }

  /**
   * Scrape all predefined searches
   */
  async scrapeAllPredefinedSearches(): Promise<ParsedJob[]> {
    const searches = [
      'software engineer india bangalore',
      'data scientist machine learning india',
      'frontend developer react india',
      'backend developer python india',
      'devops engineer india',
      'qa engineer automation india',
      'fullstack developer mern india',
      'cloud architect aws india',
      'ai ml engineer india',
      'systems engineer india'
    ]

    const allJobs: ParsedJob[] = []
    let successCount = 0
    let errorCount = 0

    for (const search of searches) {
      try {
        const jobs = await this.scrapeJobs(search, 'in')
        allJobs.push(...jobs)
        successCount++
        this.logger.info(`✅ Scraped: ${search} (${jobs.length} jobs)`)
      } catch (error) {
        errorCount++
        this.logger.error(`❌ Failed: ${search} - ${error}`)
      }

      // Small delay between searches
      await new Promise(resolve => setTimeout(resolve, 500))
    }

    this.logger.info(
      `✅ Scraping complete: ${successCount} successful, ` +
      `${errorCount} failed, ${allJobs.length} total jobs`
    )

    return allJobs
  }

  /**
   * Deduplicate jobs by external_id
   */
  async deduplicateJobs(jobs: ParsedJob[]): Promise<ParsedJob[]> {
    const seen = new Set<string>()
    const unique: ParsedJob[] = []

    for (const job of jobs) {
      if (!seen.has(job.external_id)) {
        seen.add(job.external_id)
        unique.push(job)
      }
    }

    this.logger.info(
      `🔄 Deduplication: ${jobs.length} → ${unique.length} ` +
      `(${jobs.length - unique.length} duplicates removed)`
    )

    return unique
  }

  /**
   * Check if job already exists in database
   */
  async jobExists(externalId: string, source: string): Promise<boolean> {
    const existing = await Job.findOne({
      source_metadata: {
        $elemMatch: { external_id: externalId }
      },
      source
    })

    return !!existing
  }

  /**
   * Save scraping log
   */
  async createScrapingLog(
    source: string,
    status: 'success' | 'partial' | 'failed',
    data: {
      jobsFound: number
      jobsNew: number
      jobsUpdated: number
      jobsDuplicate: number
      errors: string[]
    }
  ): Promise<void> {
    try {
      await ScrapingLog.create({
        source,
        started_at: new Date(),
        completed_at: new Date(),
        status,
        jobs_found: data.jobsFound,
        jobs_new: data.jobsNew,
        jobs_updated: data.jobsUpdated,
        jobs_duplicate: data.jobsDuplicate,
        errors: data.errors,
        error_count: data.errors.length
      })

      this.logger.info(
        `📝 Scraping log saved: ${status} - ` +
        `${data.jobsNew} new, ${data.jobsDuplicate} duplicates`
      )
    } catch (error) {
      this.logger.error(`Failed to save scraping log: ${error}`)
    }
  }
}

export default JobScraperService
