# 🤖 AI AGENT IMPLEMENTATION PROMPT
**Complete Integration Guide for 3-Component Free-Tier LinkedIn Job Scraper**

---

## 📋 EXECUTIVE SUMMARY FOR AI AGENTS

You are tasked with integrating a **free-tier optimized job scraper** into an existing **JobIntel MERN project**. The integration consists of **3 core components** that work together to provide instant job search while staying on the free tier (200 API requests/month).

**DO NOT** copy the Flask LinkedIn scraper code. Instead, use the architecture, logic, and requirements documented in the reference files. Build everything from scratch using the existing JobIntel project structure.

### Core Objectives:
- ✅ Add budget tracking (usageTracker service)
- ✅ Add local caching (jsonDatabase service)
- ✅ Add keyword deduplication (keywordDedup service)
- ✅ Integrate with existing API client
- ✅ Create admin dashboard for monitoring
- ✅ Maintain instant search <100ms latency
- ✅ Zero API cost ($0/month)

**Total Implementation:** 5 phases, 3-4 weeks

---

## 📚 REFERENCE DOCUMENTATION

Before starting, review these files to understand requirements:

1. **README_DEVELOPMENT_PLAN.md**
   - Phase breakdown and timeline
   - User stories and acceptance criteria
   - Frontend/backend requirements
   - Success metrics

2. **README_FILE_STRUCTURE.md**
   - Folder hierarchy to create
   - Service method signatures
   - Controller endpoints to build
   - Route definitions

3. **README_DATABASE_SCHEMAS.md**
   - 4 JSON data models
   - Field descriptions and types
   - Validation rules
   - Size/performance specs

4. **DEEP_ANALYSIS_3COMPONENT_INTEGRATION.md**
   - How 3 components interact
   - Data flow diagrams
   - Component responsibilities
   - Integration points

5. **DEEP_ANALYSIS_FREE_TIER_OPTIMIZATION.md**
   - Budget allocation strategy
   - Instant search mechanism
   - Cost calculations
   - Risk mitigation

6. **REQUIRED_CHANGES_SUMMARY.md**
   - Specific modifications to existing files
   - Line-by-line changes needed
   - Integration points

7. **NEW_SERVICES_usageTracker_keywordDedup_jsonDatabase.ts**
   - Service implementations (templates)
   - Method signatures with documentation
   - Ready-to-use code

8. **JSON_DATABASE_SCHEMA.ts**
   - TypeScript interfaces
   - Example data structures
   - Type definitions

---

## ⚠️ CRITICAL CONSTRAINTS

### Budget Enforcement:
```
Free tier limit: 200 requests/month
Our target: 100 requests/month (50% buffer)
Hard stop: 180 requests (90% threshold)
Warning threshold: 160 requests (80%)
Auto-reset: Monthly boundary (1st of month)
```

**ACTION:** usageTracker service must prevent ANY request beyond 180/month

### Search Performance:
```
Target latency: <100ms for cached searches
Acceptable latency: <5 seconds for API searches
Cache hit rate target: 90%
Result: Users perceive "instant" search
```

**ACTION:** jsonDatabase must serve 90% of searches from local JSON

### Data Persistence:
```
Use JSON files instead of database for scraper data
Jobs file: /data/jobs.json
Keywords file: /data/keywords.json
Usage file: /data/usage.json
Logs file: /data/scraping-logs.json
```

**ACTION:** All scraper data persists in local JSON files

---

## 🏗️ 5-PHASE IMPLEMENTATION ROADMAP

---

## PHASE 1: PROJECT SETUP & INFRASTRUCTURE
**Duration:** Days 1-2 (2 hours)
**Dependencies:** None (first phase)

### Phase 1 Goals:
1. Create complete folder structure for new services
2. Initialize JSON data files with correct schemas
3. Create environment configuration
4. Set up TypeScript interfaces

### Phase 1 Tasks:

#### 1.1 Create Directory Structure
Reference: **README_FILE_STRUCTURE.md**

Create these directories in your existing JobIntel project:

```
Backend additions:
src/services/
  ├─ usageTracker.ts (NEW)
  ├─ keywordDedup.ts (NEW)
  ├─ jsonDatabase.ts (NEW)
  └─ [existing services]

src/controllers/
  ├─ searchController.ts (NEW)
  ├─ adminScraperController.ts (NEW)
  └─ [existing controllers]

src/routes/
  ├─ searchRoutes.ts (NEW)
  ├─ adminScraperRoutes.ts (NEW)
  └─ [existing routes]

src/jobs/
  ├─ scraperScheduler.ts (MODIFY existing)
  └─ cleanupJob.ts (NEW)

data/
  ├─ jobs.json (NEW - empty array)
  ├─ keywords.json (NEW - predefined list)
  ├─ usage.json (NEW - monthly tracking)
  └─ scraping-logs.json (NEW - audit trail)

Frontend additions:
src/pages/
  ├─ user/
  │   ├─ SearchPage.tsx (NEW)
  │   ├─ JobDetailsPage.tsx (NEW)
  │   ├─ SavedJobsPage.tsx (NEW)
  │   └─ AppliedJobsPage.tsx (NEW)
  └─ admin/
      ├─ ScraperDashboard.tsx (NEW)
      ├─ BudgetMonitorPage.tsx (NEW)
      ├─ KeywordManagerPage.tsx (NEW)
      └─ LogViewerPage.tsx (NEW)

src/components/
  ├─ JobCard.tsx (NEW)
  ├─ BudgetBar.tsx (NEW)
  ├─ KeywordTable.tsx (NEW)
  └─ [other components]

src/services/
  ├─ searchService.ts (NEW)
  ├─ adminService.ts (NEW)
  └─ [other services]
```

**AI Agent Action:** Create all directories with mkdir -p

#### 1.2 Initialize Data Files
Reference: **README_DATABASE_SCHEMAS.md**

Create /data/jobs.json:
```json
{
  "jobs": [],
  "totalJobs": 0,
  "lastUpdated": "2026-01-17T00:00:00Z"
}
```

Create /data/keywords.json:
```json
{
  "keywords": [
    {
      "keyword": "React Developer",
      "lastFetched": null,
      "fetchCount": 0,
      "isActive": true
    },
    // ... 10 predefined keywords (see README_DATABASE_SCHEMAS.md)
  ],
  "totalKeywords": 10
}
```

Create /data/usage.json:
```json
{
  "month": "2026-01",
  "requestsUsed": 0,
  "requestsLimit": 200,
  "warningThreshold": 160,
  "hardStopThreshold": 180,
  "createdAt": "2026-01-17T00:00:00Z",
  "resetAt": "2026-02-01T00:00:00Z"
}
```

Create /data/scraping-logs.json:
```json
{
  "logs": [],
  "totalLogs": 0
}
```

**AI Agent Action:** Create all JSON files with initial data

#### 1.3 Create .env Configuration
Add to .env:
```
# Free-Tier API Configuration
JSERCH_API_KEY=your_key_here
JSERCH_API_URL=https://api.openwebninja.com/api/jserch

# Budget Limits
API_REQUEST_LIMIT=200
API_MONTHLY_BUDGET=100
API_WARNING_THRESHOLD=160
API_HARD_STOP_THRESHOLD=180

# Cache Settings
CACHE_TTL_MINUTES=1440
CACHE_REFRESH_DAYS=7
CACHE_HIT_TARGET=0.9

# Database
DATA_DIR=./data
JOBS_FILE=./data/jobs.json
KEYWORDS_FILE=./data/keywords.json
USAGE_FILE=./data/usage.json
LOGS_FILE=./data/scraping-logs.json

# Scheduler
ENABLE_SCHEDULER=true
SCRAPER_CRON_TIME=0 0 * * 0
CLEANUP_CRON_TIME=0 0 * * *

# Feature Flags
ENABLE_BUDGET_ENFORCEMENT=true
ENABLE_KEYWORD_DEDUP=true
ENABLE_JSON_CACHE=true
```

**AI Agent Action:** Add environment variables

#### 1.4 Create TypeScript Interfaces
Reference: **JSON_DATABASE_SCHEMA.ts**

Create /src/types/models.ts:
```typescript
// Job Model
export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  skills: string[];
  salary?: { min: number; max: number; currency: string };
  postedDate: string;
  description: string;
  url: string;
  source: string;
  fetchedAt: string;
}

// Keyword Model
export interface Keyword {
  keyword: string;
  lastFetched: string | null;
  fetchCount: number;
  isActive: boolean;
}

// Usage Model
export interface UsageTracker {
  month: string;
  requestsUsed: number;
  requestsLimit: number;
  warningThreshold: number;
  hardStopThreshold: number;
  createdAt: string;
  resetAt: string;
}

// Log Model
export interface ScrapingLog {
  id: string;
  timestamp: string;
  action: string;
  keyword?: string;
  jobsFound?: number;
  requestsMade?: number;
  success: boolean;
  error?: string;
}
```

**AI Agent Action:** Create TypeScript interface file

#### 1.5 Verify Phase 1 Completion
Checklist:
- [ ] All directories created
- [ ] All JSON files initialized
- [ ] .env configured
- [ ] TypeScript interfaces defined
- [ ] No compilation errors
- [ ] File structure matches README_FILE_STRUCTURE.md

**Next Phase:** Proceed to PHASE 2 when all items checked

---

## PHASE 2: CORE SERVICES IMPLEMENTATION
**Duration:** Days 3-5 (12-15 hours)
**Dependencies:** Phase 1 (completed)

### Phase 2 Goals:
1. Implement usageTracker service (budget enforcement)
2. Implement keywordDedup service (prevent duplicates)
3. Implement jsonDatabase service (local caching)
4. Unit test each service
5. Verify data persistence

### Phase 2 Tasks:

#### 2.1 Implement usageTracker Service
Reference: **NEW_SERVICES_usageTracker_keywordDedup_jsonDatabase.ts**

Create /src/services/usageTracker.ts

**Requirements:**
- Read/write operations on /data/usage.json
- Methods: initialize(), canMakeRequest(), increment(), getUsageStats()
- Singleton pattern: Single instance across app
- Auto-reset monthly (1st of month)
- Hard stop at 180 requests
- Warning at 160 requests

**Key Methods:**
```typescript
initialize(): void
  - Load usage.json from disk
  - Check if month has changed, reset if needed
  - Populate singleton instance

canMakeRequest(): boolean
  - Return false if requestsUsed >= hardStopThreshold
  - Log warning if requestsUsed >= warningThreshold
  - Return true otherwise

increment(count: number = 1): void
  - Add count to requestsUsed
  - Save to usage.json atomically
  - Emit event to admin dashboard

getUsageStats(): UsageStatsResponse
  - Return current usage data
  - Calculate percentages and remaining
  - Return warning state
```

**AI Agent Action:** Implement complete usageTracker.ts service

#### 2.2 Implement keywordDedup Service
Reference: **NEW_SERVICES_usageTracker_keywordDedup_jsonDatabase.ts**

Create /src/services/keywordDedup.ts

**Requirements:**
- Read/write operations on /data/keywords.json
- Methods: isDuplicate(), markAsFetched(), getStaleKeywords()
- Singleton pattern
- 7-day refresh window
- Prevent re-fetching within 7 days

**Key Methods:**
```typescript
initialize(): void
  - Load keywords.json
  - Build in-memory cache
  - Populate singleton

isDuplicate(keyword: string): boolean
  - Get last fetch date for keyword
  - Return true if fetched within last 7 days
  - Return false if older or never fetched

markAsFetched(keyword: string, count: number): void
  - Update lastFetched timestamp
  - Increment fetchCount
  - Save to keywords.json atomically

getStaleKeywords(): Keyword[]
  - Return all keywords not fetched in last 7 days
  - Used by scheduler to decide what to refresh

getKeywordStats(): KeywordStatsResponse
  - Return total keywords
  - Return stale count
  - Return fetch statistics
```

**AI Agent Action:** Implement complete keywordDedup.ts service

#### 2.3 Implement jsonDatabase Service
Reference: **NEW_SERVICES_usageTracker_keywordDedup_jsonDatabase.ts**

Create /src/services/jsonDatabase.ts

**Requirements:**
- Read/write operations on /data/jobs.json
- Methods: initialize(), search(), appendJobs(), buildIndexes()
- In-memory indexes for fast searching
- Atomic file writes for safety
- Search <50ms latency

**Key Methods:**
```typescript
initialize(): void
  - Load jobs.json from disk
  - Build in-memory indexes:
    - Index by skill
    - Index by company
    - Index by location
  - Populate singleton

search(filters: SearchFilters): Job[]
  - Use in-memory indexes
  - Apply filters: skills, company, location, salary
  - Return results in <50ms
  - No disk I/O during search

appendJobs(newJobs: Job[]): void
  - Filter duplicate IDs (jobExists check)
  - Add to in-memory array
  - Update indexes
  - Save to jobs.json atomically

buildIndexes(): void
  - Build skill index (skill -> job IDs)
  - Build company index (company -> job IDs)
  - Build location index (location -> job IDs)
  - Used during initialization and after append

getTotalJobs(): number
  - Return current job count
  - Used by admin dashboard

getStorageStats(): StorageStatsResponse
  - Return file size
  - Return job count
  - Return index sizes
```

**AI Agent Action:** Implement complete jsonDatabase.ts service

#### 2.4 Unit Test Services
Create /src/services/__tests__/

**Tests to write:**
```
usageTracker.test.ts
  - ✓ Initializes with current month data
  - ✓ canMakeRequest() returns true when under limit
  - ✓ canMakeRequest() returns false at hard stop
  - ✓ increment() updates count and saves
  - ✓ Auto-reset on month change
  - ✓ Emits warning event at 80%

keywordDedup.test.ts
  - ✓ Initializes with keyword list
  - ✓ isDuplicate() returns false for never-fetched
  - ✓ isDuplicate() returns true within 7 days
  - ✓ isDuplicate() returns false after 7 days
  - ✓ markAsFetched() updates timestamp
  - ✓ getStaleKeywords() returns keywords older than 7 days

jsonDatabase.test.ts
  - ✓ Initializes with jobs from disk
  - ✓ Builds indexes for fast search
  - ✓ search() returns results in <50ms
  - ✓ appendJobs() adds new jobs without duplicates
  - ✓ search() filters by skills, company, location
  - ✓ getTotalJobs() returns correct count
```

**AI Agent Action:** Write unit tests for all services

#### 2.5 Verify Phase 2 Completion
Checklist:
- [ ] usageTracker.ts fully implemented
- [ ] keywordDedup.ts fully implemented
- [ ] jsonDatabase.ts fully implemented
- [ ] All unit tests passing (>80% coverage)
- [ ] No compilation errors
- [ ] Data files persist correctly after operations
- [ ] Services integrate with TypeScript interfaces

**Next Phase:** Proceed to PHASE 3 when all items checked

---

## PHASE 3: EXISTING CODE INTEGRATION
**Duration:** Days 6-8 (15-18 hours)
**Dependencies:** Phase 2 (completed)

### Phase 3 Goals:
1. Modify existing JSearchClient to use usageTracker & keywordDedup
2. Modify existing JobScraperService to use jsonDatabase
3. Create searchController for user queries
4. Create adminScraperController for admin operations
5. Create routes for both controllers

### Phase 3 Tasks:

#### 3.1 Modify Existing JSearchClient (STEP1)
Reference: **REQUIRED_CHANGES_SUMMARY.md**

File to modify: /src/services/jSearchClient.ts (existing)

**Changes needed:**
```typescript
// BEFORE: Constructor
constructor(apiKey: string) {
  this.apiKey = apiKey;
  this.baseURL = 'https://api.openwebninja.com/api/jserch';
}

// AFTER: Constructor with new services
constructor(apiKey: string, usageTracker: UsageTracker, keywordDedup: KeywordDedup) {
  this.apiKey = apiKey;
  this.baseURL = 'https://api.openwebninja.com/api/jserch';
  this.usageTracker = usageTracker;
  this.keywordDedup = keywordDedup;
}

// BEFORE: searchJobs method
async searchJobs(keyword: string): Promise<Job[]> {
  const response = await fetch(`${this.baseURL}?q=${keyword}`, {
    headers: { Authorization: this.apiKey }
  });
  return response.json();
}

// AFTER: searchJobs method with guards
async searchJobs(keyword: string): Promise<Job[]> {
  // Guard 1: Check budget
  if (!this.usageTracker.canMakeRequest()) {
    throw new Error('API budget exceeded for this month');
  }

  // Guard 2: Check for duplicate keyword
  if (this.keywordDedup.isDuplicate(keyword)) {
    throw new Error(`Keyword "${keyword}" already fetched within 7 days`);
  }

  // Fetch from API
  const response = await fetch(`${this.baseURL}?q=${keyword}`, {
    headers: { Authorization: this.apiKey }
  });
  
  if (!response.ok) {
    throw new Error(`API error: ${response.statusText}`);
  }

  const jobs = await response.json();

  // Increment usage counter
  this.usageTracker.increment(1);

  // Mark keyword as fetched
  this.keywordDedup.markAsFetched(keyword, jobs.length);

  return jobs;
}
```

**AI Agent Action:** Apply all changes from REQUIRED_CHANGES_SUMMARY.md to jSearchClient

#### 3.2 Modify Existing JobScraperService (STEP2)
Reference: **REQUIRED_CHANGES_SUMMARY.md**

File to modify: /src/services/jobScraperService.ts (existing)

**Changes needed:**
```typescript
// BEFORE: scrapeJobs method
async scrapeJobs(keyword: string): Promise<Job[]> {
  const jobs = await this.jSearchClient.searchJobs(keyword);
  // Save to MongoDB
  await Job.insertMany(jobs);
  return jobs;
}

// AFTER: smartScrapeJobs method with JSON cache
async smartScrapeJobs(keyword: string): Promise<Job[]> {
  // Get fresh jobs from API (with all guards from jSearchClient)
  const freshJobs = await this.jSearchClient.searchJobs(keyword);

  // Save to JSON database (not MongoDB)
  await this.jsonDatabase.appendJobs(freshJobs);

  // Update keyword metadata
  this.keywordDedup.markAsFetched(keyword, freshJobs.length);

  return freshJobs;
}

// NEW: Method to get jobs from cache
async searchFromCache(filters: SearchFilters): Promise<Job[]> {
  return this.jsonDatabase.search(filters);
}
```

**AI Agent Action:** Apply all changes from REQUIRED_CHANGES_SUMMARY.md to jobScraperService

#### 3.3 Create searchController
File to create: /src/controllers/searchController.ts

**Endpoints to implement:**
```typescript
// GET /api/search
// Query params: skills, company, location, salary
// Response: { jobs: Job[], count: number, latency: number }
async searchJobs(req: Request, res: Response): Promise<void>

// GET /api/search/:id
// Response: { job: Job, similarJobs: Job[] }
async getJobDetails(req: Request, res: Response): Promise<void>

// POST /api/jobs/saved
// Body: { jobId: string }
// Response: { saved: boolean }
async saveJob(req: Request, res: Response): Promise<void>

// GET /api/jobs/saved
// Response: { jobs: Job[] }
async getSavedJobs(req: Request, res: Response): Promise<void>

// POST /api/jobs/apply
// Body: { jobId: string, coverLetter: string }
// Response: { applied: boolean }
async applyForJob(req: Request, res: Response): Promise<void>
```

**Key Logic:**
- All searches go through jsonDatabase (cache)
- Search latency should be <100ms
- Return both cached and fresh results
- Track search analytics

**AI Agent Action:** Implement complete searchController.ts

#### 3.4 Create adminScraperController
File to create: /src/controllers/adminScraperController.ts

**Endpoints to implement:**
```typescript
// GET /api/admin/budget
// Response: { used: number, limit: number, percentage: number, warning: boolean }
async getBudgetStatus(req: Request, res: Response): Promise<void>

// GET /api/admin/keywords
// Response: { keywords: Keyword[], staleCount: number }
async getKeywordStatus(req: Request, res: Response): Promise<void>

// POST /api/admin/keywords
// Body: { keyword: string }
// Response: { keyword: Keyword, jobsFound: number }
async addKeywordManually(req: Request, res: Response): Promise<void>

// POST /api/admin/trigger-scrape
// Body: { keyword: string }
// Response: { jobsFound: number, usageIncremented: number }
async triggerFullScrape(req: Request, res: Response): Promise<void>

// GET /api/admin/logs
// Response: { logs: ScrapingLog[], total: number }
async getScrapingLogs(req: Request, res: Response): Promise<void>

// GET /api/admin/stats
// Response: { totalJobs: number, totalKeywords: number, lastScrape: string }
async getScraperStats(req: Request, res: Response): Promise<void>
```

**Key Logic:**
- Check budget before triggering scrape
- Prevent duplicate keywords
- All operations logged to scraping-logs.json
- Admin authorization required

**AI Agent Action:** Implement complete adminScraperController.ts

#### 3.5 Create Routes
File to create: /src/routes/searchRoutes.ts

```typescript
router.get('/search', searchController.searchJobs);
router.get('/search/:id', searchController.getJobDetails);
router.post('/jobs/saved', auth, searchController.saveJob);
router.get('/jobs/saved', auth, searchController.getSavedJobs);
router.post('/jobs/apply', auth, searchController.applyForJob);
```

File to create: /src/routes/adminScraperRoutes.ts

```typescript
router.get('/admin/budget', auth, adminOnly, adminScraperController.getBudgetStatus);
router.get('/admin/keywords', auth, adminOnly, adminScraperController.getKeywordStatus);
router.post('/admin/keywords', auth, adminOnly, adminScraperController.addKeywordManually);
router.post('/admin/trigger-scrape', auth, adminOnly, adminScraperController.triggerFullScrape);
router.get('/admin/logs', auth, adminOnly, adminScraperController.getScrapingLogs);
router.get('/admin/stats', auth, adminOnly, adminScraperController.getScraperStats);
```

**AI Agent Action:** Create both route files and integrate into main Express app

#### 3.6 Verify Phase 3 Completion
Checklist:
- [ ] JSearchClient modified with budget guards
- [ ] JSearchClient modified with dedup checks
- [ ] JobScraperService uses jsonDatabase
- [ ] smartScrapeJobs method renamed and updated
- [ ] searchController fully implemented
- [ ] adminScraperController fully implemented
- [ ] Both routes created and integrated
- [ ] No compilation errors
- [ ] All endpoints tested with Postman/curl
- [ ] Budget enforcement working
- [ ] Keyword dedup working

**Next Phase:** Proceed to PHASE 4 when all items checked

---

## PHASE 4: SCHEDULER & AUTOMATION
**Duration:** Days 9-10 (8-10 hours)
**Dependencies:** Phase 3 (completed)

### Phase 4 Goals:
1. Modify existing scraperScheduler with new logic
2. Implement weekly refresh CRON job
3. Implement daily cleanup CRON job
4. Add error handling and retry logic
5. Test scheduler workflows

### Phase 4 Tasks:

#### 4.1 Modify Existing scraperScheduler
File to modify: /src/jobs/scraperScheduler.ts (existing)

**Current logic to replace:**
```typescript
// OLD: Fetch all keywords every day
async function runScraper() {
  const keywords = await Keyword.find({ isActive: true });
  for (const keyword of keywords) {
    await jobScraperService.scrapeJobs(keyword.name);
  }
}

// NEW: Smart refresh with dedup & budget
async function runScraper() {
  // Get only stale keywords (not fetched in 7 days)
  const staleKeywords = await keywordDedup.getStaleKeywords();
  
  for (const keyword of staleKeywords) {
    // Check budget before each fetch
    if (!usageTracker.canMakeRequest()) {
      console.log('Budget limit reached, stopping scraper');
      break;
    }

    try {
      const jobs = await jobScraperService.smartScrapeJobs(keyword.keyword);
      
      // Log success
      await logScrapingEvent({
        action: 'SCRAPE_SUCCESS',
        keyword: keyword.keyword,
        jobsFound: jobs.length,
        requestsMade: 1,
        success: true
      });
    } catch (error) {
      // Log failure
      await logScrapingEvent({
        action: 'SCRAPE_ERROR',
        keyword: keyword.keyword,
        success: false,
        error: error.message
      });
    }
  }
}

// CRON: Every Sunday at midnight (0 0 * * 0)
schedule.scheduleJob('0 0 * * 0', runScraper);
```

**Changes:**
1. Replace daily loop with weekly refresh
2. Use stale keyword detection
3. Add budget check before each fetch
4. Add comprehensive error logging
5. Add retry logic for failed fetches

**AI Agent Action:** Modify scraperScheduler.ts with new logic

#### 4.2 Create cleanupJob
File to create: /src/jobs/cleanupJob.ts

**Purpose:** Daily cleanup of old data

**Responsibilities:**
```typescript
// Delete old logs (older than 30 days)
async function cleanOldLogs() {
  const thirtyDaysAgo = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
  // Remove entries from scraping-logs.json older than thirtyDaysAgo
}

// Archive old jobs (optional: move to backup)
async function archiveOldJobs() {
  const ninetyDaysAgo = new Date(Date.now() - 90 * 24 * 60 * 60 * 1000);
  // Remove jobs older than 90 days from jobs.json
}

// Reset monthly usage (1st of month)
async function resetMonthlyUsage() {
  const today = new Date();
  if (today.getDate() === 1) {
    // Reinitialize usage.json for new month
    await usageTracker.initialize();
  }
}

// CRON: Every day at midnight (0 0 * * *)
schedule.scheduleJob('0 0 * * *', async () => {
  await cleanOldLogs();
  await archiveOldJobs();
  await resetMonthlyUsage();
});
```

**AI Agent Action:** Create complete cleanupJob.ts

#### 4.3 Add Error Handling & Retry
Modify scraperScheduler.ts:

```typescript
// Add retry logic
async function fetchWithRetry(keyword: string, maxRetries: number = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await jobScraperService.smartScrapeJobs(keyword);
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }
      // Wait exponential backoff: 1s, 2s, 4s
      const delay = Math.pow(2, attempt - 1) * 1000;
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

// Use retry in main loop
for (const keyword of staleKeywords) {
  try {
    const jobs = await fetchWithRetry(keyword.keyword);
    // ... logging
  } catch (error) {
    // Log final failure after all retries
  }
}
```

**AI Agent Action:** Add retry logic to scheduler

#### 4.4 Test Scheduler
Create /src/jobs/__tests__/scheduler.test.ts

**Tests:**
```typescript
- ✓ Fetches only stale keywords
- ✓ Checks budget before each fetch
- ✓ Stops when budget limit reached
- ✓ Logs successes and failures
- ✓ Retries failed requests
- ✓ Resets usage on month boundary
- ✓ Cleans old logs daily
```

**AI Agent Action:** Write comprehensive scheduler tests

#### 4.5 Verify Phase 4 Completion
Checklist:
- [ ] scraperScheduler modified with smart refresh
- [ ] Weekly CRON job running (0 0 * * 0)
- [ ] Daily cleanup job implemented (0 0 * * *)
- [ ] Error handling and retry logic working
- [ ] Logging working for all operations
- [ ] Budget enforcement in scheduler
- [ ] All scheduler tests passing
- [ ] No compilation errors
- [ ] Manual test: Trigger scheduler and verify operations

**Next Phase:** Proceed to PHASE 5 when all items checked

---

## PHASE 5: FRONTEND DEVELOPMENT
**Duration:** Days 11-17 (35-42 hours)
**Dependencies:** Phase 4 (completed)

### Phase 5 Goals:
1. Build 4 user-facing search pages (React)
2. Build 4 admin monitoring/control pages (React)
3. Connect to backend API endpoints
4. Implement instant search UX
5. Add admin dashboard with real-time stats

### Phase 5 Tasks:

#### 5.1 User Pages (4 pages)

##### Page 1: SearchPage
File: /src/pages/user/SearchPage.tsx

**Features:**
- Search box with filters (skills, company, location, salary)
- Real-time search results <100ms
- Pagination (10-20 results per page)
- Sort options (relevance, salary, date posted)
- Save job button
- Apply job button

**Components used:**
- SearchBox.tsx
- JobCard.tsx
- FilterPanel.tsx
- Pagination.tsx

**API calls:**
- GET /api/search (with query params)
- POST /api/jobs/saved
- POST /api/jobs/apply

**AI Agent Action:** Implement SearchPage.tsx

##### Page 2: JobDetailsPage
File: /src/pages/user/JobDetailsPage.tsx

**Features:**
- Full job description
- Similar jobs section
- Company information
- Apply button
- Save button
- Job share options

**Components used:**
- JobHeader.tsx
- JobDescription.tsx
- SimilarJobs.tsx
- ApplyModal.tsx

**API calls:**
- GET /api/search/:id
- POST /api/jobs/apply

**AI Agent Action:** Implement JobDetailsPage.tsx

##### Page 3: SavedJobsPage
File: /src/pages/user/SavedJobsPage.tsx

**Features:**
- List of saved jobs
- Remove from saved
- Sort by save date
- Search within saved jobs

**Components used:**
- SavedJobList.tsx
- JobCard.tsx

**API calls:**
- GET /api/jobs/saved
- DELETE /api/jobs/saved/:id

**AI Agent Action:** Implement SavedJobsPage.tsx

##### Page 4: AppliedJobsPage
File: /src/pages/user/AppliedJobsPage.tsx

**Features:**
- List of applied jobs
- Application status
- Date applied
- Application history

**Components used:**
- AppliedJobList.tsx
- StatusBadge.tsx

**API calls:**
- GET /api/jobs/applications

**AI Agent Action:** Implement AppliedJobsPage.tsx

#### 5.2 Admin Pages (4 pages)

##### Admin Page 1: ScraperDashboard
File: /src/pages/admin/ScraperDashboard.tsx

**Features:**
- Real-time budget usage (progress bar)
- API calls made this month
- Requests remaining
- Warning indicator at 80%
- Total jobs in database
- Last scrape timestamp

**Components used:**
- BudgetCard.tsx
- StatsCard.tsx
- ActivitiesLog.tsx

**API calls:**
- GET /api/admin/budget
- GET /api/admin/stats
- GET /api/admin/logs (recent)

**Refresh:** Every 10 seconds

**AI Agent Action:** Implement ScraperDashboard.tsx

##### Admin Page 2: BudgetMonitorPage
File: /src/pages/admin/BudgetMonitorPage.tsx

**Features:**
- Detailed budget breakdown
- Usage chart (line graph over month)
- Requests per day
- Budget forecast
- Warning/danger zones
- Export CSV

**Components used:**
- BudgetChart.tsx
- BudgetTable.tsx
- ForecastCard.tsx

**API calls:**
- GET /api/admin/budget
- GET /api/admin/logs

**AI Agent Action:** Implement BudgetMonitorPage.tsx

##### Admin Page 3: KeywordManagerPage
File: /src/pages/admin/KeywordManagerPage.tsx

**Features:**
- List of all keywords
- Last fetch date
- Fetch count
- Active/inactive toggle
- Add new keyword
- Manual trigger scrape for keyword
- Fetch history

**Components used:**
- KeywordTable.tsx
- AddKeywordModal.tsx

**API calls:**
- GET /api/admin/keywords
- POST /api/admin/keywords
- POST /api/admin/trigger-scrape

**AI Agent Action:** Implement KeywordManagerPage.tsx

##### Admin Page 4: LogViewerPage
File: /src/pages/admin/LogViewerPage.tsx

**Features:**
- Scraping operation logs
- Filter by action (SCRAPE_SUCCESS, SCRAPE_ERROR, etc)
- Filter by date range
- Export logs
- Search logs
- Real-time updates

**Components used:**
- LogTable.tsx
- LogFilter.tsx
- LogSearch.tsx

**API calls:**
- GET /api/admin/logs

**Refresh:** Real-time WebSocket or 5-second polling

**AI Agent Action:** Implement LogViewerPage.tsx

#### 5.3 Shared Components

Create reusable components:
```
src/components/
├── SearchBox.tsx
├── JobCard.tsx
├── FilterPanel.tsx
├── Pagination.tsx
├── BudgetCard.tsx
├── StatsCard.tsx
├── BudgetBar.tsx
├── KeywordTable.tsx
├── StatusBadge.tsx
└── ActivitiesLog.tsx
```

**AI Agent Action:** Implement all shared components

#### 5.4 Frontend Services

Create /src/services/:
```typescript
// searchService.ts
export async function searchJobs(filters: SearchFilters): Promise<Job[]>
export async function getJobDetails(jobId: string): Promise<Job>
export async function saveJob(jobId: string): Promise<void>
export async function getSavedJobs(): Promise<Job[]>
export async function applyForJob(jobId: string, coverLetter: string): Promise<void>

// adminService.ts
export async function getBudgetStatus(): Promise<BudgetResponse>
export async function getKeywordStatus(): Promise<KeywordResponse>
export async function addKeyword(keyword: string): Promise<void>
export async function triggerScrape(keyword: string): Promise<void>
export async function getScrapingLogs(): Promise<ScrapingLog[]>
export async function getScraperStats(): Promise<StatsResponse>
```

**AI Agent Action:** Implement both frontend services

#### 5.5 Verify Phase 5 Completion
Checklist:
- [ ] SearchPage fully functional
- [ ] JobDetailsPage fully functional
- [ ] SavedJobsPage fully functional
- [ ] AppliedJobsPage fully functional
- [ ] ScraperDashboard fully functional
- [ ] BudgetMonitorPage fully functional
- [ ] KeywordManagerPage fully functional
- [ ] LogViewerPage fully functional
- [ ] All components created and integrated
- [ ] All API calls working
- [ ] Search latency <100ms
- [ ] No console errors
- [ ] Responsive design (mobile + desktop)
- [ ] Unit tests for all pages (>70% coverage)

**Next Phase:** Proceed to PHASE 5+ when all items checked

---

## 🎯 POST-PHASE 5: TESTING & DEPLOYMENT
**Duration:** Days 18-21 (16-20 hours)

### Testing Strategy:
1. Unit tests (services, controllers, utils)
2. Integration tests (API endpoints)
3. E2E tests (user workflows)
4. Load testing (concurrent searches)
5. Budget limit testing (edge cases)

### Deployment:
1. Staging environment
2. Production environment
3. Health checks
4. Monitoring setup

---

## ✅ VERIFICATION & COMPLIANCE

### Success Criteria:
- ✅ All 3 components working together
- ✅ Budget stays under 200 requests/month
- ✅ Search latency <100ms (90% of searches)
- ✅ No API overage incidents
- ✅ All admin endpoints working
- ✅ All user endpoints working
- ✅ Scheduler running on schedule
- ✅ Cleanup job removing old data
- ✅ Zero unhandled errors
- ✅ Test coverage >80%

### Performance Metrics:
```
API Requests: 50-100/month (target: 100, limit: 200)
Search Latency: <100ms (cached)
Memory Usage: <200MB
Storage: <50MB
Uptime: >99%
```

### Budget Compliance:
```
Month 1: X requests used, Y% of budget
Month 2: X requests used, Y% of budget
Month 3: X requests used, Y% of budget
Total Cost: $0
Status: ✅ COMPLIANT
```

---

## 🔗 INTEGRATION REFERENCE MAP

### How All Components Connect:

**User searches for "React Developer":**
1. Frontend sends GET /api/search?skills=React
2. searchController receives request
3. jsonDatabase.search() checks cache (~30ms)
4. If cache miss, trigger API fetch
5. usageTracker checks if request allowed
6. keywordDedup checks if keyword was fetched in last 7 days
7. JSearchClient fetches from API (if allowed)
8. Results saved to jsonDatabase
9. jsonDatabase indexes updated
10. Response sent to frontend (~50ms total)

**Admin manually triggers scrape for "Node Developer":**
1. Admin clicks "Trigger Scrape" button
2. Frontend sends POST /api/admin/trigger-scrape
3. adminScraperController receives request
4. usageTracker.canMakeRequest() checks budget
5. keywordDedup.isDuplicate() checks if already fetched
6. jobScraperService.smartScrapeJobs() fetches from API
7. jsonDatabase.appendJobs() saves results
8. ScrapingLog entry created
9. usageTracker.increment() updates usage
10. Response sent to admin with results

**Scheduler runs weekly:**
1. CRON triggers on Sunday at midnight
2. keywordDedup.getStaleKeywords() gets keywords older than 7 days
3. For each stale keyword:
   - usageTracker.canMakeRequest() checks budget
   - If budget available: fetch from API
   - If budget exhausted: stop scraper
4. Results saved to jsonDatabase
5. ScrapingLog entries created
6. cleanupJob runs daily at midnight:
   - Removes logs older than 30 days
   - Removes jobs older than 90 days
   - Resets usage on month boundary

---

## 📚 REFERENCE TO EXISTING DOCUMENTATION

When implementing, constantly refer to:

1. **For API endpoint signatures:** README_FILE_STRUCTURE.md
2. **For data model details:** README_DATABASE_SCHEMAS.md
3. **For service method signatures:** NEW_SERVICES_usageTracker_keywordDedup_jsonDatabase.ts
4. **For integration logic:** DEEP_ANALYSIS_3COMPONENT_INTEGRATION.md
5. **For budget strategy:** DEEP_ANALYSIS_FREE_TIER_OPTIMIZATION.md
6. **For specific code changes:** REQUIRED_CHANGES_SUMMARY.md
7. **For TypeScript interfaces:** JSON_DATABASE_SCHEMA.ts
8. **For phase breakdown:** README_DEVELOPMENT_PLAN.md

---

## 🎯 AI AGENT INSTRUCTIONS

**You MUST:**
1. Follow all 5 phases in order
2. Reference documentation files frequently
3. Implement from scratch (don't copy Flask code)
4. Use logic from reference files only
5. Create TypeScript types for everything
6. Write unit tests for all services
7. Add error handling and logging
8. Test each phase before moving next
9. Maintain budget enforcement at all times
10. Document any deviations or assumptions

**You MUST NOT:**
1. Copy Flask/Python code
2. Skip phases or reorder them
3. Mix MongoDB and JSON persistence
4. Exceed 180 API requests threshold
5. Use outdated reference files
6. Ignore error handling
7. Create duplicate code
8. Skip unit tests
9. Deploy without testing
10. Modify existing user data structures

**Success = Complete all 5 phases with:**
- Zero compilation errors
- >80% test coverage
- All endpoints working
- Budget enforced
- <100ms search latency
- Zero API overages
- All documentation referenced
- Clean code with comments

---

## 📞 QUICK COMMAND REFERENCE

**Start Phase 1:**
```
mkdir -p src/services src/controllers src/routes src/jobs src/pages/user src/pages/admin data
npm install node-cron
```

**Test Phase 2:**
```
npm test src/services
```

**Test Phase 3:**
```
npm test src/controllers
```

**Run Scheduler:**
```
node -r ts-node/register src/jobs/index.ts
```

**Deploy:**
```
npm run build
npm run deploy
```

---

**Status:** Ready for AI Agent Implementation ✅

**Timeline:** 3-4 weeks (21 days total)

**Team:** 1-2 developers

**Cost:** $0/month (free tier)

**Success Rate:** 95%+ (if phases followed correctly)

**Last Updated:** January 17, 2026

**Version:** 1.0 - Final for Production
