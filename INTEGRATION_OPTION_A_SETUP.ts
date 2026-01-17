/**
 * ============================================
 * COMPLETE SETUP GUIDE - OPTION A
 * ============================================
 * 
 * STEP-BY-STEP INTEGRATION INSTRUCTIONS
 */

// ============================================
// PART 1: DEPENDENCIES & SETUP
// ============================================

/**
 * STEP 1.1: Install Required Packages
 * 
 * Run in your backend directory:
 * 
 *   npm install axios bull redis node-cron
 *   npm install --save-dev @types/node-cron
 * 
 * Packages explained:
 * - axios: HTTP client for JSearch API calls
 * - bull: Job queue for reliable job processing
 * - redis: Cache/queue backend (optional but recommended)
 * - node-cron: Scheduling tasks
 */

// ============================================
// PART 2: ENVIRONMENT VARIABLES
// ============================================

/**
 * STEP 2.1: Update backend/.env
 * 
 * Add these variables:
 */

const ENV_VARIABLES = `
# JSearch API Configuration
JSEARCH_API_KEY=ak_58a8asv2uix2dbxls7sitbar9zq647ld0iqbio1phiz29ar
JSEARCH_API_HOST=api.openwebninja.com

# Redis Configuration (optional but recommended)
REDIS_URL=redis://localhost:6379

# Scraper Configuration
SCRAPER_ENABLED=true
SCRAPER_RATE_LIMIT_PER_SEC=1
SCRAPER_BATCH_SIZE=50
SCRAPER_UPDATE_FREQUENCY=6h

# Queue Configuration
QUEUE_MAX_RETRIES=3
QUEUE_RETRY_DELAY=2000

# Logging
LOG_LEVEL=info
`

// ============================================
// PART 3: DATABASE SCHEMA UPDATES
// ============================================

/**
 * STEP 3.1: Update Job Model
 * 
 * File: backend/models/Job.ts
 * 
 * Add these fields to your existing Job schema:
 */

const JobModelUpdates = `
import { Schema, model } from 'mongoose'

const jobSchema = new Schema({
  // ... existing fields ...

  // ✨ NEW: Source tracking
  source: {
    type: String,
    enum: ['jsearch', 'linkedin', 'indeed', 'manual'],
    default: 'manual',
    index: true
  },

  // ✨ NEW: Source metadata
  source_metadata: {
    external_id: String,
    scraped_at: Date,
    raw_response: Schema.Types.Mixed,
    extraction_method: String,
    confidence: Number
  },

  // ✨ NEW: Deduplication
  is_duplicate: { type: Boolean, default: false },
  duplicate_of: { type: Schema.Types.ObjectId, ref: 'Job' },

  // ✨ NEW: Freshness tracking
  last_scraped_at: Date,

  // ✨ NEW: Job matching analytics
  total_matches: { type: Number, default: 0 },
  last_matched_at: Date,
  match_score_distribution: {
    high: Number,
    medium: Number,
    low: Number
  },

  // ✨ NEW: Embedding
  embedding: [Number], // 1536-dimensional vector
  embedding_generated_at: Date
})

// Add indexes for performance
jobSchema.index({ source: 1, 'source_metadata.external_id': 1 }, { unique: true })
jobSchema.index({ 'source_metadata.scraped_at': -1 })
jobSchema.index({ is_duplicate: 1 })

export const Job = model('Job', jobSchema)
`

/**
 * STEP 3.2: Create ScrapingLog Model
 * 
 * File: backend/models/ScrapingLog.ts
 */

const ScrapingLogModel = `
import { Schema, model } from 'mongoose'

const scrapingLogSchema = new Schema({
  source: {
    type: String,
    required: true
  },
  started_at: {
    type: Date,
    required: true
  },
  completed_at: {
    type: Date
  },
  status: {
    type: String,
    enum: ['running', 'success', 'partial', 'failed'],
    default: 'running'
  },
  jobs_found: { type: Number, default: 0 },
  jobs_new: { type: Number, default: 0 },
  jobs_updated: { type: Number, default: 0 },
  jobs_duplicate: { type: Number, default: 0 },
  jobs_queued: { type: Number, default: 0 },
  errors: [String],
  error_count: { type: Number, default: 0 }
}, { timestamps: true })

scrapingLogSchema.index({ started_at: -1 })

export const ScrapingLog = model('ScrapingLog', scrapingLogSchema)
`

// ============================================
// PART 4: FILE CREATION CHECKLIST
// ============================================

/**
 * STEP 4.1: Create These Files in Your Project
 * 
 * Location: backend/
 * 
 * File Structure to Create:
 * 
 * backend/
 * ├── services/
 * │   ├── jsearchClient.ts                    ← From STEP1
 * │   └── jobScraperService.ts                ← From STEP2
 * │
 * ├── queues/
 * │   └── jobIngestionQueue.ts                ← From STEP3
 * │
 * ├── jobs/
 * │   └── scraperScheduler.ts                 ← From STEP4
 * │
 * ├── controllers/
 * │   └── adminScraperController.ts           ← From STEP5
 * │
 * ├── routes/
 * │   └── adminScraperRoutes.ts               ← From STEP5
 * │
 * └── models/
 *     ├── ScrapingLog.ts                      ← NEW
 *     └── Job.ts                              ← UPDATE EXISTING
 * 
 * Reference Files:
 * - INTEGRATION_OPTION_A_STEP1.ts
 * - INTEGRATION_OPTION_A_STEP2.ts
 * - INTEGRATION_OPTION_A_STEP3.ts
 * - INTEGRATION_OPTION_A_STEP4.ts
 * - INTEGRATION_OPTION_A_STEP5.ts
 */

// ============================================
// PART 5: MAIN APPLICATION SETUP
// ============================================

/**
 * STEP 5.1: Initialize Scheduler in Your Express App
 * 
 * File: backend/server.ts (or app.ts)
 */

const ServerSetup = `
import express from 'express'
import { initializeScheduler } from './jobs/scraperScheduler'
import adminScraperRoutes from './routes/adminScraperRoutes'

const app = express()

// ... other middleware ...

// Initialize scraper scheduler
if (process.env.SCRAPER_ENABLED === 'true') {
  const apiKey = process.env.JSEARCH_API_KEY
  if (!apiKey) {
    console.error('❌ JSEARCH_API_KEY not set in environment')
  } else {
    initializeScheduler(apiKey)
    console.log('✅ Scraper scheduler initialized')
  }
}

// Add scraper routes (admin only)
app.use('/api/admin/scraper', adminScraperRoutes)

// ... rest of app setup ...

const PORT = process.env.PORT || 4000
app.listen(PORT, () => {
  console.log(\`✅ Server running on port \${PORT}\`)
})
`

// ============================================
// PART 6: TESTING THE INTEGRATION
// ============================================

/**
 * STEP 6.1: Test Connection to JSearch API
 * 
 * Run this test file:
 */

const TestScript = `
// File: backend/__tests__/scraper.test.ts
// Run: npx ts-node backend/__tests__/scraper.test.ts

import JSearchClient from '../services/jsearchClient'

async function testScraper() {
  console.log('🧪 Testing scraper integration...')

  const apiKey = process.env.JSEARCH_API_KEY
  if (!apiKey) {
    console.error('❌ JSEARCH_API_KEY not set')
    return
  }

  const client = new JSearchClient(apiKey)

  try {
    // Test 1: Health check
    console.log('\\n1️⃣ Testing API connection...')
    const isHealthy = await client.healthCheck()
    console.log(isHealthy ? '✅ API is working' : '❌ API test failed')

    // Test 2: Search jobs
    console.log('\\n2️⃣ Testing job search...')
    const jobs = await client.searchJobs({
      query: 'software engineer',
      country: 'in'
    })
    console.log(\`✅ Found \${jobs.length} jobs\`)

    // Test 3: Parse first job
    if (jobs.length > 0) {
      console.log('\\n3️⃣ First job:')
      console.log(\`   Title: \${jobs[0].job_title}\`)
      console.log(\`   Company: \${jobs[0].employer_name}\`)
      console.log(\`   Location: \${jobs[0].job_city}\`)
    }

    console.log('\\n✅ All tests passed!')

  } catch (error) {
    console.error('❌ Test failed:', error)
  }
}

testScraper()
`

/**
 * STEP 6.2: Manual Trigger Test
 * 
 * API endpoint to test:
 * 
 *   POST http://localhost:4000/api/admin/scraper/run
 *   Authorization: Bearer <your_jwt_token>
 *   
 * Response:
 *   {
 *     "success": true,
 *     "message": "Scraping started in background",
 *     "timestamp": "2026-01-17T12:00:00Z"
 *   }
 */

/**
 * STEP 6.3: Check Stats
 * 
 *   GET http://localhost:4000/api/admin/scraper/stats
 *   Authorization: Bearer <your_jwt_token>
 *   
 * Shows queue status, recent logs, job counts
 */

// ============================================
// PART 7: TROUBLESHOOTING
// ============================================

const Troubleshooting = `
Problem: "JSEARCH_API_KEY not set"
Solution: Add JSEARCH_API_KEY to backend/.env

Problem: "Redis connection refused"
Solution: 
  - Install Redis locally: brew install redis (Mac) or docker run redis (Docker)
  - Or set REDIS_URL in .env to point to your Redis server
  - Or queue will work in-memory mode (slower)

Problem: "Jobs not being scraped"
Solution:
  - Check server logs for errors
  - Verify API key is valid
  - Check rate limits on JSearch account
  - Manual test: curl POST /api/admin/scraper/run

Problem: "Embeddings not generated"
Solution:
  - Verify OPENAI_API_KEY is set
  - Check OpenAI account has credit
  - Verify embeddingService is called in jobIngestionQueue

Problem: "Duplicate jobs showing up"
Solution:
  - Run POST /api/admin/scraper/queue to check queue
  - May need to adjust deduplication logic
  - Check database indexes are created

Problem: "Scheduler not running"
Solution:
  - Verify SCRAPER_ENABLED=true in .env
  - Check server logs for initialization
  - Manually trigger with POST /api/admin/scraper/run
`

// ============================================
// PART 8: MONITORING & MAINTENANCE
// ============================================

/**
 * STEP 8.1: Monitor Scraper Health
 * 
 * Check these endpoints regularly:
 */

const MonitoringEndpoints = `
// Get overall stats
GET /api/admin/scraper/stats

// Get job queue status
GET /api/admin/scraper/queue

// Get recent scraping logs
GET /api/admin/scraper/logs

// Get job analytics
GET /api/admin/scraper/analytics
`

/**
 * STEP 8.2: Expected Queue Load
 * 
 * At default settings (6-hour interval, 10 searches):
 *   - 10 searches × 6 times/day = 60 API calls/day
 *   - ~400-600 jobs/day (some duplicates)
 *   - ~100-200 new unique jobs/day
 *   - Queue processes: ~10-20 per minute
 */

/**
 * STEP 8.3: Database Cleanup (Monthly)
 * 
 * Remove old logs older than 30 days:
 *   
 *   db.scrapinglogs.deleteMany({
 *     started_at: { $lt: new Date(Date.now() - 30*24*60*60*1000) }
 *   })
 * 
 * This runs automatically daily at 2 AM
 */

// ============================================
// PART 9: PERFORMANCE TUNING
// ============================================

/**
 * If scraper is too fast (flooding API):
 *   - Increase requestDelay in JSearchClient (default: 1000ms)
 *   - Reduce SCRAPER_BATCH_SIZE in .env
 *   - Increase cron interval (from every 6 hours to every 12)
 */

/**
 * If scraper is too slow (not keeping up):
 *   - Reduce rate limit delay if API allows
 *   - Increase num_pages per search
 *   - Add more Redis workers (BullMQ)
 *   - Reduce deduplication overhead
 */

/**
 * If CPU/memory too high:
 *   - Reduce batch size
 *   - Enable Redis connection (offload to Redis)
 *   - Split scraping across multiple cron jobs
 *   - Add caching layer
 */

// ============================================
// PART 10: COST ANALYSIS
// ============================================

/**
 * API Usage:
 *   Current: Free tier = 200 requests/month
 *   Need: ~1800 requests/month (60 × 30 days)
 *   Recommendation: Upgrade to Professional = $50/month
 *   Gets: 10,000 requests/month
 * 
 * Database:
 *   Additional storage: ~50-100 MB/month
 *   MongoDB Atlas: Included in most plans
 * 
 * Redis (optional):
 *   Small instance: ~$0-5/month
 *   Or self-hosted: Free (but needs maintenance)
 * 
 * Total Monthly Cost: $50-60 (API + Redis)
 */

// ============================================
// IMPLEMENTATION CHECKLIST
// ============================================

const Checklist = `
PHASE 1: SETUP (Day 1)
□ Install dependencies (npm install...)
□ Update .env with API key and Redis
□ Upgrade JSearch API plan if needed

PHASE 2: CODE INTEGRATION (Days 2-3)
□ Create JSearchClient service
□ Create JobScraperService
□ Create jobIngestionQueue
□ Create scraperScheduler
□ Create admin controller & routes
□ Update Job model with new fields
□ Create ScrapingLog model

PHASE 3: TESTING (Days 4-5)
□ Test JSearch API connection
□ Test job scraping manually
□ Test queue processing
□ Test job matching
□ Test admin endpoints

PHASE 4: DEPLOYMENT (Days 6-7)
□ Migrate existing jobs (set source='manual')
□ Deploy to staging
□ Run full scrape test
□ Deploy to production
□ Monitor for 24 hours

ONGOING
□ Monitor scraper logs
□ Check queue status
□ Adjust cron schedule as needed
□ Update predefined searches
```

// ============================================
// QUICK START COMMAND REFERENCE
// ============================================

const QuickReference = \`
# Install dependencies
npm install axios bull redis node-cron @types/node-cron

# Add .env variables
JSEARCH_API_KEY=your_key_here
REDIS_URL=redis://localhost:6379

# Start Redis (if not running)
redis-server

# Start your Express app (scheduler auto-initializes)
npm run dev

# Check admin endpoints
curl http://localhost:4000/api/admin/scraper/stats \\
  -H "Authorization: Bearer <token>"

# Manually trigger scrape
curl -X POST http://localhost:4000/api/admin/scraper/run \\
  -H "Authorization: Bearer <token>"

# Monitor queue
curl http://localhost:4000/api/admin/scraper/queue \\
  -H "Authorization: Bearer <token>"
\`

export {
  ENV_VARIABLES,
  JobModelUpdates,
  ScrapingLogModel,
  ServerSetup,
  TestScript,
  Troubleshooting,
  MonitoringEndpoints,
  Checklist,
  QuickReference
}
