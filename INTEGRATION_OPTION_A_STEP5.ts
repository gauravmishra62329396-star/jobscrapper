/**
 * ============================================
 * STEP 5: Admin Controller & Routes
 * ============================================
 * 
 * Files:
 * - backend/controllers/adminScraperController.ts
 * - backend/routes/adminScraperRoutes.ts
 */

// ==========================================
// FILE 1: controllers/adminScraperController.ts
// ==========================================

import { Request, Response } from 'express'
import { getScheduler } from '../jobs/scraperScheduler'
import { getQueueStatus, clearQueue } from '../queues/jobIngestionQueue'
import { ScrapingLog } from '../models/ScrapingLog'
import { Job } from '../models/Job'
import { Logger } from '../utils/logger'

const logger = new Logger('AdminScraperController')

/**
 * Get scraper statistics
 */
export async function getScraperStats(req: Request, res: Response) {
  try {
    const today = new Date()
    today.setHours(0, 0, 0, 0)

    // Today's activity
    const scrapedToday = await Job.countDocuments({
      'source_metadata.scraped_at': { $gte: today }
    })

    // Duplicate stats
    const duplicateCount = await Job.countDocuments({ is_duplicate: true })
    const canonicalCount = await Job.countDocuments({
      is_duplicate: false,
      source: 'jsearch'
    })

    // Source breakdown
    const sourceBreakdown = await Job.aggregate([
      {
        $group: {
          _id: '$source',
          count: { $sum: 1 }
        }
      }
    ])

    // Recent logs
    const recentLogs = await ScrapingLog.find()
      .sort({ started_at: -1 })
      .limit(10)
      .lean()

    // Queue status
    const queueStatus = await getQueueStatus()

    // Scheduler status
    const scheduler = getScheduler()
    const schedulerStatus = scheduler.getStatus()

    res.json({
      success: true,
      stats: {
        scrapedToday,
        duplicateCount,
        canonicalCount,
        totalJobs: duplicateCount + canonicalCount,
        sourceBreakdown,
        queueStatus,
        schedulerStatus,
        recentLogs
      }
    })
  } catch (error: any) {
    logger.error(`Error fetching stats: ${error.message}`)
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
}

/**
 * Manually trigger full scrape
 */
export async function triggerFullScrape(req: Request, res: Response) {
  try {
    const scheduler = getScheduler()

    // Check if already running
    const status = scheduler.getStatus()
    if (status.isRunning) {
      return res.status(409).json({
        success: false,
        error: 'Scraper is already running'
      })
    }

    // Trigger scrape (don't wait for completion)
    scheduler.triggerFullScrape().catch(err => {
      logger.error(`Background scrape error: ${err}`)
    })

    res.json({
      success: true,
      message: 'Scraping started in background',
      timestamp: new Date()
    })
  } catch (error: any) {
    logger.error(`Error triggering scrape: ${error.message}`)
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
}

/**
 * Get scraping logs
 */
export async function getScrapingLogs(req: Request, res: Response) {
  try {
    const page = parseInt(req.query.page as string) || 1
    const limit = parseInt(req.query.limit as string) || 50

    const skip = (page - 1) * limit

    const logs = await ScrapingLog.find()
      .sort({ started_at: -1 })
      .skip(skip)
      .limit(limit)
      .lean()

    const total = await ScrapingLog.countDocuments()

    res.json({
      success: true,
      data: logs,
      pagination: {
        page,
        limit,
        total,
        pages: Math.ceil(total / limit)
      }
    })
  } catch (error: any) {
    logger.error(`Error fetching logs: ${error.message}`)
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
}

/**
 * Get queue status and recent jobs
 */
export async function getQueueStats(req: Request, res: Response) {
  try {
    const status = await getQueueStatus()

    res.json({
      success: true,
      queue: status
    })
  } catch (error: any) {
    logger.error(`Error fetching queue stats: ${error.message}`)
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
}

/**
 * Get job analytics
 */
export async function getJobAnalytics(req: Request, res: Response) {
  try {
    // Jobs by status
    const statusCount = await Job.aggregate([
      {
        $group: {
          _id: '$status',
          count: { $sum: 1 }
        }
      }
    ])

    // Jobs by source
    const sourceCount = await Job.aggregate([
      {
        $group: {
          _id: '$source',
          count: { $sum: 1 }
        }
      }
    ])

    // Jobs by employment type
    const employmentCount = await Job.aggregate([
      {
        $group: {
          _id: '$employment_type',
          count: { $sum: 1 }
        }
      }
    ])

    // Average match score
    const matchStats = await Job.aggregate([
      {
        $group: {
          _id: null,
          avgMatches: { $avg: '$total_matches' },
          maxMatches: { $max: '$total_matches' },
          minMatches: { $min: '$total_matches' }
        }
      }
    ])

    // Top companies
    const topCompanies = await Job.aggregate([
      {
        $group: {
          _id: '$company',
          count: { $sum: 1 }
        }
      },
      { $sort: { count: -1 } },
      { $limit: 10 }
    ])

    // Top locations
    const topLocations = await Job.aggregate([
      {
        $group: {
          _id: '$location',
          count: { $sum: 1 }
        }
      },
      { $sort: { count: -1 } },
      { $limit: 10 }
    ])

    res.json({
      success: true,
      analytics: {
        statusCount,
        sourceCount,
        employmentCount,
        matchStats: matchStats[0] || {},
        topCompanies,
        topLocations
      }
    })
  } catch (error: any) {
    logger.error(`Error fetching analytics: ${error.message}`)
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
}

/**
 * Clear queue (dangerous! - admin only)
 */
export async function clearJobQueue(req: Request, res: Response) {
  try {
    const confirm = req.body.confirm === true

    if (!confirm) {
      return res.status(400).json({
        success: false,
        error: 'Must confirm clearance with confirm: true'
      })
    }

    await clearQueue()

    logger.warn(`⚠️ Job queue cleared by admin`)

    res.json({
      success: true,
      message: 'Queue cleared successfully'
    })
  } catch (error: any) {
    logger.error(`Error clearing queue: ${error.message}`)
    res.status(500).json({
      success: false,
      error: error.message
    })
  }
}

// ==========================================
// FILE 2: routes/adminScraperRoutes.ts
// ==========================================

import { Router } from 'express'
import { authenticateToken, requireRole } from '../middleware/auth'
import * as controller from '../controllers/adminScraperController'

const router = Router()

// All routes require admin role
router.use(authenticateToken)
router.use(requireRole('admin'))

/**
 * GET /api/admin/scraper/stats
 * Get scraper and queue statistics
 */
router.get('/stats', controller.getScraperStats)

/**
 * POST /api/admin/scraper/run
 * Manually trigger full scrape
 */
router.post('/run', controller.triggerFullScrape)

/**
 * GET /api/admin/scraper/logs
 * Get scraping logs with pagination
 */
router.get('/logs', controller.getScrapingLogs)

/**
 * GET /api/admin/scraper/queue
 * Get job queue status
 */
router.get('/queue', controller.getQueueStats)

/**
 * GET /api/admin/scraper/analytics
 * Get job analytics
 */
router.get('/analytics', controller.getJobAnalytics)

/**
 * DELETE /api/admin/scraper/queue
 * Clear job queue (DANGEROUS!)
 */
router.delete('/queue', controller.clearJobQueue)

export default router

// ==========================================
// INTEGRATION: Add to main Express app
// ==========================================

/**
 * In your main backend/server.ts or backend/app.ts:
 * 
 * import adminScraperRoutes from './routes/adminScraperRoutes'
 * 
 * app.use('/api/admin/scraper', adminScraperRoutes)
 */
