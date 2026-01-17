/**
 * ============================================
 * STEP 4: Scheduled Scraper with Cron
 * ============================================
 * 
 * File: backend/jobs/scraperScheduler.ts
 * 
 * Automatically runs scraping at scheduled intervals
 * Tracks logs and handles errors
 */

import cron from 'node-cron'
import JobScraperService from '../services/jobScraperService'
import JSearchClient from '../services/jsearchClient'
import { queueJobForIngestion } from '../queues/jobIngestionQueue'
import { ScrapingLog } from '../models/ScrapingLog'
import { Logger } from '../utils/logger'

const logger = new Logger('ScraperScheduler')

export class ScraperScheduler {
  private jsearchClient: JSearchClient
  private scraperService: JobScraperService
  private isRunning: boolean = false

  // Predefined searches for India
  private readonly SEARCHES = [
    { query: 'software engineer india bangalore', country: 'in' },
    { query: 'data scientist machine learning india', country: 'in' },
    { query: 'frontend developer react india', country: 'in' },
    { query: 'backend developer python india', country: 'in' },
    { query: 'devops engineer kubernetes india', country: 'in' },
    { query: 'qa engineer automation testing india', country: 'in' },
    { query: 'fullstack developer mern node india', country: 'in' },
    { query: 'cloud architect aws azure india', country: 'in' },
    { query: 'ai ml engineer deep learning india', country: 'in' },
    { query: 'systems engineer infrastructure india', country: 'in' }
  ]

  constructor(apiKey: string) {
    this.jsearchClient = new JSearchClient(apiKey)
    this.scraperService = new JobScraperService(this.jsearchClient, logger)
    logger.info('✅ ScraperScheduler initialized')
  }

  /**
   * Initialize scheduler and set up cron jobs
   */
  initialize() {
    logger.info('🚀 Initializing scheduler...')

    // Run full scrape every 6 hours (at 0, 6, 12, 18)
    cron.schedule('0 */6 * * *', async () => {
      logger.info('⏰ Cron triggered: Full scrape (every 6 hours)')
      await this.runFullScrape()
    })

    // Run predefined searches every 3 hours
    cron.schedule('0 */3 * * *', async () => {
      logger.info('⏰ Cron triggered: Predefined searches (every 3 hours)')
      await this.runPredefinedSearches()
    })

    // Cleanup old logs daily at 2 AM
    cron.schedule('0 2 * * *', async () => {
      logger.info('⏰ Cron triggered: Cleanup old logs (daily 2 AM)')
      await this.cleanupOldLogs()
    })

    logger.info('✅ Scheduler initialized with cron jobs:')
    logger.info('   - Full scrape: Every 6 hours')
    logger.info('   - Predefined searches: Every 3 hours')
    logger.info('   - Cleanup logs: Daily at 2 AM')
  }

  /**
   * Run full scrape of all predefined searches
   */
  async runFullScrape() {
    if (this.isRunning) {
      logger.warn('⚠️ Scraper already running, skipping...')
      return
    }

    const logId = new Date().getTime()
    logger.info(`🔍 [${logId}] Starting full scrape...`)

    this.isRunning = true
    const startTime = Date.now()

    try {
      // Create scraping log
      const log = await ScrapingLog.create({
        source: 'jsearch_full',
        started_at: new Date(),
        status: 'running'
      })

      let totalFound = 0
      let totalQueued = 0
      let errorCount = 0
      const errors: string[] = []

      // Run each search
      for (const search of this.SEARCHES) {
        try {
          logger.info(`[${logId}] 🔍 Searching: "${search.query}"`)

          const jobs = await this.scraperService.scrapeJobs(
            search.query,
            search.country
          )

          logger.info(`[${logId}] ✅ Got ${jobs.length} jobs`)
          totalFound += jobs.length

          // Deduplicate
          const unique = await this.scraperService.deduplicateJobs(jobs)

          // Queue each job
          for (const job of unique) {
            try {
              await queueJobForIngestion(job)
              totalQueued++
            } catch (queueError) {
              logger.error(`[${logId}] Failed to queue job: ${queueError}`)
              errors.push(`Queue error for ${job.title}: ${queueError}`)
            }
          }

          // Rate limiting between searches
          await new Promise(resolve => setTimeout(resolve, 1000))

        } catch (searchError: any) {
          errorCount++
          const errorMsg = `${search.query}: ${searchError.message}`
          logger.error(`[${logId}] ❌ ${errorMsg}`)
          errors.push(errorMsg)

          // Continue with next search
          continue
        }
      }

      // Update log
      log.completed_at = new Date()
      log.status = errorCount === 0 ? 'success' : 'partial'
      log.jobs_found = totalFound
      log.jobs_queued = totalQueued
      log.error_count = errorCount
      log.errors = errors
      await log.save()

      const duration = ((Date.now() - startTime) / 1000).toFixed(2)
      logger.info(
        `[${logId}] ✅ Full scrape completed in ${duration}s: ` +
        `${totalFound} found, ${totalQueued} queued, ${errorCount} errors`
      )

    } catch (error) {
      logger.error(`[${logId}] ❌ Fatal error in full scrape: ${error}`)
    } finally {
      this.isRunning = false
    }
  }

  /**
   * Run predefined searches only
   */
  async runPredefinedSearches() {
    if (this.isRunning) {
      logger.warn('⚠️ Scraper already running, skipping...')
      return
    }

    const logId = new Date().getTime()
    logger.info(`[${logId}] Running predefined searches...`)

    this.isRunning = true
    const startTime = Date.now()

    try {
      const log = await ScrapingLog.create({
        source: 'jsearch_predefined',
        started_at: new Date(),
        status: 'running'
      })

      let totalQueued = 0
      const errors: string[] = []

      // Run top 5 searches
      for (const search of this.SEARCHES.slice(0, 5)) {
        try {
          logger.info(`[${logId}] 🔍 ${search.query}`)

          const jobs = await this.scraperService.scrapeJobs(
            search.query,
            search.country
          )

          const unique = await this.scraperService.deduplicateJobs(jobs)

          for (const job of unique) {
            await queueJobForIngestion(job)
            totalQueued++
          }

          await new Promise(resolve => setTimeout(resolve, 500))

        } catch (error) {
          const errorMsg = `${search.query}: ${error}`
          logger.error(`[${logId}] Error: ${errorMsg}`)
          errors.push(errorMsg)
        }
      }

      log.completed_at = new Date()
      log.status = errors.length === 0 ? 'success' : 'partial'
      log.jobs_queued = totalQueued
      log.error_count = errors.length
      log.errors = errors
      await log.save()

      const duration = ((Date.now() - startTime) / 1000).toFixed(2)
      logger.info(
        `[${logId}] ✅ Predefined search complete in ${duration}s: ` +
        `${totalQueued} queued, ${errors.length} errors`
      )

    } catch (error) {
      logger.error(`[${logId}] ❌ Fatal error: ${error}`)
    } finally {
      this.isRunning = false
    }
  }

  /**
   * Manual trigger - run full scrape immediately
   */
  async triggerFullScrape() {
    logger.info('🚀 Manual scrape triggered')
    await this.runFullScrape()
  }

  /**
   * Get current status
   */
  getStatus() {
    return {
      isRunning: this.isRunning,
      timestamp: new Date()
    }
  }

  /**
   * Cleanup old logs (keep last 30 days)
   */
  private async cleanupOldLogs() {
    try {
      const thirtyDaysAgo = new Date()
      thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

      const result = await ScrapingLog.deleteMany({
        started_at: { $lt: thirtyDaysAgo }
      })

      logger.info(`🧹 Cleanup: Deleted ${result.deletedCount} old logs`)
    } catch (error) {
      logger.error(`Cleanup error: ${error}`)
    }
  }
}

// Global instance
let scheduler: ScraperScheduler | null = null

/**
 * Initialize global scheduler
 */
export function initializeScheduler(apiKey: string) {
  if (!scheduler) {
    scheduler = new ScraperScheduler(apiKey)
    scheduler.initialize()
  }
  return scheduler
}

/**
 * Get scheduler instance
 */
export function getScheduler(): ScraperScheduler {
  if (!scheduler) {
    throw new Error('Scheduler not initialized. Call initializeScheduler first.')
  }
  return scheduler
}

export default ScraperScheduler
