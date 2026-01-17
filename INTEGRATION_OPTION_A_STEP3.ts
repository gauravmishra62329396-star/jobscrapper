/**
 * ============================================
 * STEP 3: Job Ingestion Queue (BullMQ)
 * ============================================
 * 
 * File: backend/queues/jobIngestionQueue.ts
 * 
 * Reliable queue for processing scraped jobs
 * Handles rate limiting, retries, and error handling
 */

import Bull from 'bull'
import Redis from 'redis'
import { Job as MongoJob } from '../models/Job'
import { JobMatch } from '../models/JobMatch'
import { embeddingService } from '../services/embeddingService'
import { matchingEngine } from '../services/matchingEngine'
import { Logger } from '../utils/logger'

const logger = new Logger('JobIngestionQueue')

// Connect to Redis (or use in-memory fallback)
let redisClient: any = null
try {
  redisClient = Redis.createClient({
    url: process.env.REDIS_URL || 'redis://localhost:6379'
  })
  redisClient.connect()
  logger.info('✅ Connected to Redis')
} catch (error) {
  logger.warn('⚠️ Redis not available, using in-memory queue')
}

// Create BullMQ queue
export const jobIngestionQueue = new Bull('job-ingestion', {
  redis: redisClient || undefined,
  defaultJobOptions: {
    attempts: 3, // Retry 3 times
    backoff: {
      type: 'exponential',
      delay: 2000 // Start with 2 second delay
    },
    removeOnComplete: true,
    removeOnFail: false // Keep failed jobs for analysis
  }
})

/**
 * Job data interface
 */
interface JobIngestionData {
  parsedJob: {
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
}

/**
 * Process job ingestion
 */
jobIngestionQueue.process(async (job: Bull.Job<JobIngestionData>) => {
  const { parsedJob } = job.data
  let savedJobId: string | null = null

  try {
    logger.info(
      `[Job ${job.id}] Processing: ${parsedJob.title} at ${parsedJob.company}`
    )

    // Step 1: Check if job already exists
    const existing = await MongoJob.findOne({
      'source_metadata.external_id': parsedJob.external_id,
      'source_metadata.source': parsedJob.source
    })

    if (existing) {
      logger.info(`[Job ${job.id}] ✅ Job already exists (ID: ${existing._id})`)

      // Update last scraped
      existing.last_scraped_at = new Date()
      await existing.save()

      return {
        status: 'skipped',
        reason: 'already_exists',
        jobId: existing._id.toString()
      }
    }

    // Step 2: Generate embedding
    logger.info(`[Job ${job.id}] Generating embedding...`)
    const embedText = `${parsedJob.title} ${parsedJob.description}`
    const embedding = await embeddingService.getEmbedding(embedText)

    // Step 3: Create job in MongoDB
    logger.info(`[Job ${job.id}] Creating job record...`)
    const newJob = new MongoJob({
      title: parsedJob.title,
      company: parsedJob.company,
      location: parsedJob.location,
      salary: parsedJob.salary,
      description: parsedJob.description,
      requirements: parsedJob.requirements,
      preferred_skills: parsedJob.preferredSkills,
      employment_type: parsedJob.employment_type,
      is_remote: parsedJob.is_remote,
      apply_url: parsedJob.apply_url,
      source: parsedJob.source,
      source_metadata: {
        external_id: parsedJob.external_id,
        scraped_at: parsedJob.source_metadata.scraped_at,
        raw_response: parsedJob.source_metadata.raw_response,
        extraction_method: parsedJob.source_metadata.extraction_method,
        confidence: parsedJob.source_metadata.confidence
      },
      embedding,
      embedding_generated_at: new Date(),
      is_duplicate: false,
      total_matches: 0,
      status: 'active'
    })

    const savedJob = await newJob.save()
    savedJobId = savedJob._id.toString()

    logger.info(
      `[Job ${job.id}] ✅ Job saved to MongoDB (ID: ${savedJobId})`
    )

    // Step 4: Trigger matching engine (in background)
    logger.info(`[Job ${job.id}] Triggering matching engine...`)
    try {
      await matchingEngine.matchJobAgainstAllResumes(
        savedJob._id,
        embedding
      )
      logger.info(`[Job ${job.id}] ✅ Matching complete`)
    } catch (matchError) {
      logger.error(
        `[Job ${job.id}] ⚠️ Matching error (non-blocking): ${matchError}`
      )
      // Don't fail the job if matching fails
    }

    return {
      status: 'success',
      jobId: savedJobId,
      message: `Job created and matched against resumes`
    }

  } catch (error: any) {
    logger.error(
      `[Job ${job.id}] ❌ Error processing job: ${error.message}`
    )

    // If we created the job, clean it up
    if (savedJobId) {
      try {
        await MongoJob.deleteOne({ _id: savedJobId })
        logger.info(`[Job ${job.id}] Cleaned up partially created job`)
      } catch (cleanupError) {
        logger.error(`[Job ${job.id}] Failed to cleanup: ${cleanupError}`)
      }
    }

    throw error // Re-throw to trigger retry
  }
})

/**
 * Job completion handler
 */
jobIngestionQueue.on('completed', (job: Bull.Job) => {
  logger.info(`✅ [Job ${job.id}] Completed: ${job.data.parsedJob.title}`)
})

/**
 * Job failure handler
 */
jobIngestionQueue.on('failed', (job: Bull.Job, err: Error) => {
  logger.error(
    `❌ [Job ${job.id}] Failed after 3 attempts: ${err.message}`
  )
})

/**
 * Job retry handler
 */
jobIngestionQueue.on('stalled', (job: Bull.Job) => {
  logger.warn(`⚠️ [Job ${job.id}] Stalled, will retry...`)
})

/**
 * Queue event listeners
 */
jobIngestionQueue.on('error', (error) => {
  logger.error(`Queue error: ${error}`)
})

jobIngestionQueue.on('waiting', (jobId) => {
  logger.debug(`Job ${jobId} is waiting to be processed`)
})

/**
 * Helper: Add job to queue
 */
export async function queueJobForIngestion(parsedJob: JobIngestionData['parsedJob']) {
  try {
    const job = await jobIngestionQueue.add(
      { parsedJob },
      {
        jobId: `job-${parsedJob.external_id}`, // Unique job ID
        priority: 5 // Default priority
      }
    )

    logger.info(
      `📝 Queued job for ingestion: ${parsedJob.title} (Queue ID: ${job.id})`
    )
    return job
  } catch (error) {
    logger.error(`Failed to queue job: ${error}`)
    throw error
  }
}

/**
 * Helper: Get queue status
 */
export async function getQueueStatus() {
  const counts = await jobIngestionQueue.getJobCounts()
  const activeJobs = await jobIngestionQueue.getActive()
  const failedJobs = await jobIngestionQueue.getFailed()
  const waitingJobs = await jobIngestionQueue.getWaiting()

  return {
    total: counts.total,
    active: counts.active,
    failed: counts.failed,
    waiting: counts.waiting,
    completed: counts.completed,
    activeJobsDetails: activeJobs.map(j => ({
      id: j.id,
      title: j.data.parsedJob.title,
      attempts: j.attemptsMade
    })),
    failedJobsDetails: failedJobs.slice(0, 5).map(j => ({
      id: j.id,
      title: j.data.parsedJob.title,
      error: j.failedReason
    }))
  }
}

/**
 * Helper: Clear queue (use carefully!)
 */
export async function clearQueue() {
  logger.warn('⚠️ Clearing job ingestion queue')
  await jobIngestionQueue.empty()
  logger.info('✅ Queue cleared')
}

export default jobIngestionQueue
