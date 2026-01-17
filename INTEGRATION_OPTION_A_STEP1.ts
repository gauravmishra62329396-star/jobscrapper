/**
 * ============================================
 * OPTION A: FULL INTEGRATION GUIDE
 * LinkedIn Scraper → JobIntel (Node.js/TypeScript)
 * ============================================
 * 
 * This file contains the complete, ready-to-use
 * TypeScript code for integrating the Python scraper
 * directly into your Express.js backend.
 * 
 * Implementation Time: 2-3 weeks
 * Complexity: Medium
 * Files to Create: ~12 new files
 */

// ============================================
// STEP 1: Create JSearchClient Service
// ============================================

/**
 * File: backend/services/jsearchClient.ts
 * 
 * Direct port from Python scraper
 * Handles API communication with OpenWeb Ninja JSearch API
 */

import axios, { AxiosInstance } from 'axios'
import { Logger } from '../utils/logger'

interface SearchParams {
  query: string
  country?: string
  page?: number
  num_pages?: number
  date_posted?: string
  employment_types?: string
  radius?: number
  language?: string
}

interface SalaryParams {
  job_title: string
  location?: string
  experience_level?: string
  country?: string
}

interface RawJobResponse {
  job_id: string
  job_title: string
  job_description: string
  employer_name: string
  job_employment_type: string
  job_required_experience?: string
  job_required_skills?: string[]
  job_min_salary?: number
  job_max_salary?: number
  job_salary_currency?: string
  job_salary_period?: string
  job_city?: string
  job_country?: string
  job_state?: string
  job_latitude?: number
  job_longitude?: number
  job_apply_link?: string
  job_posted_at_timestamp?: number
  job_posted_at_datetime_utc?: string
  job_is_remote?: boolean
  job_google_link?: string
}

export class JSearchClient {
  private client: AxiosInstance
  private apiKey: string
  private apiHost: string
  private logger: Logger
  private lastRequestTime: number = 0
  private requestDelay: number = 1000 // 1 second rate limiting

  constructor(apiKey: string, apiHost: string = 'api.openwebninja.com', logger?: Logger) {
    this.apiKey = apiKey
    this.apiHost = apiHost
    this.logger = logger || new Logger('JSearchClient')

    this.client = axios.create({
      baseURL: `https://${apiHost}`,
      timeout: 30000,
      headers: {
        'User-Agent': 'JobIntel-Scraper/1.0'
      }
    })

    this.logger.info(`JSearchClient initialized for ${apiHost}`)
  }

  /**
   * Rate limiting: Wait if necessary to maintain 1 req/sec
   */
  private async enforceRateLimit(): Promise<void> {
    const now = Date.now()
    const elapsed = now - this.lastRequestTime

    if (elapsed < this.requestDelay) {
      const waitTime = this.requestDelay - elapsed
      this.logger.debug(`Rate limiting: waiting ${waitTime}ms`)
      await new Promise(resolve => setTimeout(resolve, waitTime))
    }

    this.lastRequestTime = Date.now()
  }

  /**
   * Retry logic with exponential backoff
   */
  private async withRetry<T>(
    fn: () => Promise<T>,
    maxRetries: number = 3,
    backoffMs: number = 2000
  ): Promise<T> {
    for (let attempt = 0; attempt < maxRetries; attempt++) {
      try {
        return await fn()
      } catch (error: any) {
        const statusCode = error.response?.status

        // Rate limited - wait longer
        if (statusCode === 429) {
          const waitTime = backoffMs * Math.pow(2, attempt)
          this.logger.warn(`Rate limited. Waiting ${waitTime}ms before retry...`)
          await new Promise(resolve => setTimeout(resolve, waitTime))
          continue
        }

        // Last attempt - throw
        if (attempt === maxRetries - 1) {
          throw error
        }

        // Exponential backoff
        const waitTime = backoffMs * Math.pow(2, attempt)
        this.logger.warn(
          `Request failed (attempt ${attempt + 1}/${maxRetries}). ` +
          `Retrying in ${waitTime}ms...`
        )
        await new Promise(resolve => setTimeout(resolve, waitTime))
      }
    }

    throw new Error(`Failed after ${maxRetries} attempts`)
  }

  /**
   * Search for jobs using JSearch API
   */
  async searchJobs(params: SearchParams): Promise<RawJobResponse[]> {
    await this.enforceRateLimit()

    return this.withRetry(async () => {
      this.logger.info(
        `Searching jobs: "${params.query}" in ${params.country || 'global'}`
      )

      const response = await this.client.get('/jsearch/search', {
        params: {
          apikey: this.apiKey,
          query: params.query,
          country: params.country || 'in',
          page: params.page || 1,
          num_pages: params.num_pages || 1,
          date_posted: params.date_posted || 'month',
          employment_types: params.employment_types || 'FULLTIME',
          radius: params.radius,
          language: params.language,
          ...params
        }
      })

      if (response.data.status !== 'ok') {
        throw new Error(`API returned status: ${response.data.status}`)
      }

      const jobs = response.data.data || []
      this.logger.info(`Found ${jobs.length} jobs`)

      return jobs
    })
  }

  /**
   * Get details for specific job
   */
  async getJobDetails(
    jobId: string,
    country: string = 'in'
  ): Promise<RawJobResponse> {
    await this.enforceRateLimit()

    return this.withRetry(async () => {
      this.logger.info(`Getting details for job ${jobId}`)

      const response = await this.client.get('/jsearch/job-details', {
        params: {
          apikey: this.apiKey,
          job_id: jobId,
          country
        }
      })

      if (response.data.status !== 'ok') {
        throw new Error(`API returned status: ${response.data.status}`)
      }

      return response.data.data[0] // Returns array
    })
  }

  /**
   * Get estimated salary for job title
   */
  async estimateSalary(params: SalaryParams): Promise<any[]> {
    await this.enforceRateLimit()

    return this.withRetry(async () => {
      this.logger.info(`Estimating salary for ${params.job_title}`)

      const response = await this.client.get('/jsearch/estimated-salary', {
        params: {
          apikey: this.apiKey,
          job_title: params.job_title,
          location: params.location,
          experience_level: params.experience_level || 'ALL',
          country: params.country || 'in'
        }
      })

      return response.data.data || []
    })
  }

  /**
   * Get company salary data
   */
  async companySalary(params: any): Promise<any[]> {
    await this.enforceRateLimit()

    return this.withRetry(async () => {
      this.logger.info(`Getting company salary data for ${params.company_name}`)

      const response = await this.client.get('/jsearch/company-job-salary', {
        params: {
          apikey: this.apiKey,
          company_name: params.company_name,
          country: params.country || 'in'
        }
      })

      return response.data.data || []
    })
  }

  /**
   * Test connection to API
   */
  async healthCheck(): Promise<boolean> {
    try {
      await this.searchJobs({
        query: 'test',
        country: 'in',
        num_pages: 1
      })
      this.logger.info('✅ Health check passed')
      return true
    } catch (error) {
      this.logger.error('❌ Health check failed:', error)
      return false
    }
  }
}

export default JSearchClient
