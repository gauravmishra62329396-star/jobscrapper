# 📋 DEVELOPMENT PLAN README
**Free-Tier LinkedIn Scraper + JSON Cache + Instant Search**

---

## 📖 TABLE OF CONTENTS

1. **Project Overview** - What you're building
2. **Architecture Summary** - How 3 components work
3. **Development Phases** - Week-by-week breakdown
4. **File Structure** - Folder organization
5. **Database Models** - Data schemas
6. **API Endpoints** - Backend routes
7. **Frontend Pages** - User & Admin UIs
8. **User Roles & Permissions** - Access control
9. **Testing Strategy** - How to verify
10. **Deployment Checklist** - Go-live requirements

---

## 1️⃣ PROJECT OVERVIEW

### What Are You Building?

**LinkedIn Job Scraper for Free Tier** - A web application that:

```
✅ Scrapes jobs from OpenWeb Ninja JSearch API
✅ Stores jobs in JSON files (zero database cost)
✅ Provides instant search (<100ms) from cached data
✅ Enforces 200 request/month budget (free tier)
✅ Automatically refreshes stale data weekly
✅ Allows admin to manually add new keywords
✅ Tracks API usage and shows warnings
```

### Three Main Components:

| Component | Purpose | Technology |
|-----------|---------|-----------|
| **API Cost Limiter** | Prevents overage charges | usageTracker.ts |
| **JSON Cache** | Instant search results | jsonDatabase.ts |
| **Smart Scraper** | Budget-aware job fetching | keywordDedup.ts + JSearchClient |

### Target Users:

| User Type | What They Do | Pages They Use |
|-----------|-------------|----------------|
| **End User** | Search for jobs instantly | SearchPage, JobDetails, SavedJobs |
| **Admin** | Manage budget & keywords | ScraperDashboard, BudgetMonitor, KeywordManager |
| **System** | Auto-refresh data | CRON scheduler, Background jobs |

---

## 2️⃣ ARCHITECTURE SUMMARY

### How Everything Connects:

```
┌─────────────────────────────────────────────────────┐
│                   USER SEARCHES                     │
│              "Python Developer"                     │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │ searchController │  (Frontend API)
        └────────┬────────┘
                 │
        ┌────────▼──────────────┐
        │ jsonDatabase.search() │  Try cache first
        └────────┬──────────────┘
                 │
        ┌─YES───┴───NO───┐
        │                │
        ▼                ▼
    Return 50ms     Check Budget
    Results ⚡      (usageTracker)
                        │
              ┌─────────┴────────┐
              │                  │
          ✅ SAFE            ❌ LIMIT
              │                  │
              ▼                  ▼
        Check Dedup         Return Cached
        (keywordDedup)      Results Only
              │
        ┌─YES─┴─NO─┐
        │          │
        │      Call API
        │      (1 request)
        │          │
        │      Save JSON
        │          │
        └──────┬───┘
               ▼
        Return Results
```

### Data Flow Paths:

**Path 1: Search Hit Cache (90% of time)**
- User search → Check keywords.json → Found recently → Return in 50ms ⚡

**Path 2: Search Miss Cache, Budget OK (5% of time)**
- User search → Not in cache → Check budget → Call API → Save JSON → Return in 5s

**Path 3: Search Miss Cache, Budget Exhausted (5% of time)**
- User search → Not in cache → Check budget → BLOCKED → Return archived data

---

## 3️⃣ DEVELOPMENT PHASES

### Phase 1: Setup (Day 1-2)

**Objectives:**
- [ ] Set up project structure
- [ ] Create data directories
- [ ] Initialize JSON files
- [ ] Set up environment variables

**Deliverables:**
- Directory structure created
- .env configured with API key
- data/ folder with initial JSON files

**Time:** 4-6 hours

---

### Phase 2: Core Services (Day 3-5)

**Objectives:**
- [ ] Build usageTracker service
- [ ] Build keywordDedup service
- [ ] Build jsonDatabase service
- [ ] Test services in isolation

**Deliverables:**
- usageTracker.ts (ready to track API calls)
- keywordDedup.ts (ready to deduplicate keywords)
- jsonDatabase.ts (ready to cache jobs)

**Time:** 12-15 hours

---

### Phase 3: API Integration (Day 6-8)

**Objectives:**
- [ ] Update JSearchClient with budget checks
- [ ] Update JobScraperService with JSON save
- [ ] Create searchController for instant search
- [ ] Create admin controller for budget management

**Deliverables:**
- JSearchClient checks budget before API call
- JobScraperService saves to JSON
- searchController returns cached results instantly
- Admin endpoints working

**Time:** 15-18 hours

---

### Phase 4: Scheduler & Automation (Day 9-10)

**Objectives:**
- [ ] Create scraperScheduler for CRON jobs
- [ ] Set up weekly refresh
- [ ] Set up daily cleanup
- [ ] Test scheduling

**Deliverables:**
- CRON jobs running on schedule
- Weekly keyword refresh working
- Log cleanup happening daily

**Time:** 8-10 hours

---

### Phase 5: Frontend - User Pages (Day 11-14)

**Objectives:**
- [ ] Build SearchPage component
- [ ] Build JobDetailsPage component
- [ ] Build SavedJobsPage component
- [ ] Integrate with searchController

**Deliverables:**
- User can search instantly
- User can view job details
- User can save jobs
- All pages responsive

**Time:** 20-24 hours

---

### Phase 6: Frontend - Admin Pages (Day 15-17)

**Objectives:**
- [ ] Build ScraperDashboard
- [ ] Build BudgetMonitorPage
- [ ] Build KeywordManagerPage
- [ ] Build LogViewerPage

**Deliverables:**
- Admin sees real-time stats
- Admin sees budget usage
- Admin can manage keywords
- Admin can view logs

**Time:** 15-18 hours

---

### Phase 7: Testing & Deployment (Day 18-21)

**Objectives:**
- [ ] Unit tests for services
- [ ] Integration tests for API
- [ ] E2E tests for user flows
- [ ] Deploy to staging
- [ ] Deploy to production

**Deliverables:**
- 80%+ code coverage
- All tests passing
- Live on production

**Time:** 16-20 hours

---

## 4️⃣ FILE STRUCTURE

### Backend Structure:

```
backend/
├── services/
│   ├── usageTracker.ts              ← Track API budget
│   ├── keywordDedup.ts              ← Prevent duplicate fetches
│   ├── jsonDatabase.ts              ← Cache & search
│   ├── jsearchClient.ts             ← API communication (MODIFIED)
│   └── jobScraperService.ts         ← Job scraping (MODIFIED)
│
├── controllers/
│   ├── searchController.ts          ← User search (NEW)
│   ├── adminScraperController.ts    ← Admin management (MODIFIED)
│   └── jobController.ts             ← Job CRUD (if needed)
│
├── routes/
│   ├── searchRoutes.ts              ← /api/search/* (NEW)
│   ├── adminScraperRoutes.ts        ← /api/admin/scraper/* (MODIFIED)
│   └── jobRoutes.ts                 ← /api/jobs/* (if needed)
│
├── jobs/
│   ├── scraperScheduler.ts          ← CRON scheduling (MODIFIED)
│   └── cleanupJob.ts                ← Daily cleanup (NEW)
│
├── middleware/
│   ├── auth.ts                      ← JWT authentication
│   ├── errorHandler.ts              ← Error handling
│   └── rateLimit.ts                 ← API rate limiting
│
├── models/
│   └── (Optional - for tracking purposes)
│
├── data/
│   ├── jobs.json                    ← Cached job listings
│   ├── keywords.json                ← Keyword tracking
│   ├── usage.json                   ← API budget tracking
│   ├── scraping-logs.json           ← Audit trail
│   └── backups/
│       ├── jobs.backup.*.json
│       └── keywords.backup.*.json
│
├── utils/
│   ├── logger.ts                    ← Logging utility
│   ├── validators.ts                ← Input validation
│   └── formatters.ts                ← Data formatting
│
├── config/
│   └── constants.ts                 ← Constants & defaults
│
├── __tests__/
│   ├── services/
│   │   ├── usageTracker.test.ts
│   │   ├── keywordDedup.test.ts
│   │   └── jsonDatabase.test.ts
│   ├── controllers/
│   │   ├── searchController.test.ts
│   │   └── adminScraperController.test.ts
│   └── integration/
│       └── scraper.integration.test.ts
│
├── server.ts                        ← Express app setup
├── .env.example                     ← Environment template
└── package.json                     ← Dependencies
```

### Frontend Structure:

```
frontend/
├── pages/
│   ├── user/
│   │   ├── SearchPage.tsx          ← Main search UI
│   │   ├── JobDetailsPage.tsx      ← Job detail view
│   │   ├── SavedJobsPage.tsx       ← Bookmarked jobs
│   │   └── AppliedJobsPage.tsx     ← Applied jobs tracking
│   │
│   └── admin/
│       ├── ScraperDashboard.tsx    ← Real-time stats
│       ├── BudgetMonitorPage.tsx   ← Budget tracking
│       ├── KeywordManagerPage.tsx  ← Keyword management
│       └── LogViewerPage.tsx       ← Audit logs
│
├── components/
│   ├── SearchBar.tsx               ← Search input
│   ├── JobCard.tsx                 ← Job listing card
│   ├── FilterPanel.tsx             ← Search filters
│   ├── BudgetWidget.tsx            ← Budget display
│   ├── KeywordList.tsx             ← Keyword list
│   └── Charts.tsx                  ← Dashboard charts
│
├── services/
│   ├── searchService.ts            ← API calls for search
│   ├── adminService.ts             ← API calls for admin
│   └── storageService.ts           ← Local storage
│
├── hooks/
│   ├── useSearch.ts                ← Search hook
│   ├── useAdmin.ts                 ← Admin hook
│   └── useBudget.ts                ← Budget hook
│
├── styles/
│   ├── globals.css
│   └── components.module.css
│
└── App.tsx                         ← Main app component
```

### Data Directory Structure:

```
data/
├── jobs.json
│   └── Stores: 10,000+ cached jobs
│       Size: ~5-10MB
│       Schema: [See Database Models]
│
├── keywords.json
│   └── Stores: Keyword timestamps
│       Size: <100KB
│       Schema: [See Database Models]
│
├── usage.json
│   └── Stores: Monthly API usage
│       Size: <50KB
│       Schema: [See Database Models]
│
├── scraping-logs.json
│   └── Stores: Audit trail
│       Size: <500KB (pruned monthly)
│       Schema: [See Database Models]
│
└── backups/
    ├── jobs.backup.2025-01-17.json
    ├── jobs.backup.2025-01-18.json
    └── keywords.backup.*.json
```

---

## 5️⃣ DATABASE MODELS / JSON SCHEMAS

### Model 1: jobs.json

```typescript
// Structure:
{
  "jobs": [
    {
      "id": "job_1705500000_abc123",           // Unique ID
      "external_id": "jsearch_12345",          // JSearch ID
      "title": "Senior Python Developer",
      "company": "Google India",
      "location": "Bangalore, Karnataka",
      "country": "India",
      "salary_min": 500000,                    // In INR
      "salary_max": 800000,
      "employment_type": "full-time",
      "skills": ["Python", "FastAPI"],
      "apply_url": "https://careers.google.com/...",
      "is_remote": false,
      "source": "openwebninja",
      "keyword": "python developer bangalore",
      "fetched_at": "2025-01-17T10:30:00Z",
      "dedup_key": "hash_of_title_company_location",
      "is_duplicate": false,
      "job_status": "active"
    }
  ],
  "metadata": {
    "total_jobs": 10234,
    "last_updated": "2025-01-17T10:30:00Z"
  }
}
```

**Purpose:** Cache all jobs for instant searching
**Read-only access:** Frontend (via searchController)
**Write access:** jobScraperService only
**Refresh:** Weekly + manual admin trigger
**Size limit:** 10,000-50,000 jobs (~5-25MB)

---

### Model 2: keywords.json

```typescript
{
  "keywords": [
    {
      "keyword": "python developer bangalore",
      "keyword_normalized": "python-developer-bangalore",
      "fetched_at": "2025-01-17T10:30:00Z",
      "next_refresh_date": "2025-01-24T10:30:00Z",   // 7 days later
      "jobs_returned": 245,
      "request_count": 1,
      "status": "active"
    }
  ],
  "metadata": {
    "total_keywords": 10,
    "active_keywords": 10,
    "last_updated": "2025-01-17T10:30:00Z"
  }
}
```

**Purpose:** Track which keywords were fetched and when
**Read access:** searchController (check cache hit)
**Write access:** jobScraperService (mark fetched)
**Rules:** 
  - Same keyword: Skip if fetched < 7 days ago
  - New keyword: Fetch immediately
  - Stale keyword: Refresh on CRON

---

### Model 3: usage.json

```typescript
{
  "current_month": {
    "month": "2025-01",
    "total_requests": 45,
    "remaining_requests": 155,          // 200 - 45
    "max_requests": 200,
    "warning_triggered": false,          // At 80% (160 requests)
    "hard_limit_triggered": false,       // At 90% (180 requests)
    "requests_by_date": {
      "2025-01-17": 5,
      "2025-01-16": 3
    },
    "requests_by_keyword": {
      "python developer bangalore": 1,
      "data scientist india": 1
    }
  },
  "previous_months": []
}
```

**Purpose:** Track API budget and prevent overage
**Read access:** usageTracker (before API calls), admin dashboard
**Write access:** JSearchClient (after each API call)
**Rules:**
  - Hard stop at 180 requests
  - Warn at 160 requests (80%)
  - Auto-reset on month boundary

---

### Model 4: scraping-logs.json

```typescript
{
  "logs": [
    {
      "id": "log_1705500000_abc123",
      "timestamp": "2025-01-17T10:30:00Z",
      "status": "success",                     // success|failure|partial
      "keyword": "python developer bangalore",
      "request_type": "manual",                // manual|scheduled|refresh
      "triggered_by": "admin:user@example.com",
      "jobs_fetched": 245,
      "jobs_added": 200,                       // New jobs
      "jobs_updated": 45,                      // Existing jobs refreshed
      "duplicates_removed": 10,
      "error": null,
      "duration_ms": 5432,
      "api_requests_used": 1,
      "monthly_usage_after": 46
    }
  ],
  "metadata": {
    "total_logs": 1,
    "success_count": 1,
    "failure_count": 0
  }
}
```

**Purpose:** Audit trail for debugging & monitoring
**Read access:** Admin only (LogViewerPage)
**Write access:** jobScraperService (log each fetch)
**Retention:** 30 days (auto-delete older logs)

---

## 6️⃣ API ENDPOINTS

### User API Endpoints

#### 1. Search Jobs
```
GET /api/search
Query params:
  - q: string (search query)
  - limit: number (default: 50)
  - offset: number (default: 0)
  - minSalary: number (optional)
  - maxSalary: number (optional)
  - location: string (optional)
  - skills: string[] (optional)

Response:
{
  "success": true,
  "results": [
    {
      "id": "job_...",
      "title": "Senior Python Developer",
      "company": "Google India",
      ...
    }
  ],
  "total": 45,
  "cached": true,
  "cachedAt": "2025-01-17T10:30:00Z"
}
```

#### 2. Get Job Details
```
GET /api/jobs/:jobId

Response:
{
  "success": true,
  "job": {
    "id": "job_...",
    "title": "Senior Python Developer",
    "description": "Full job description...",
    "company": "Google India",
    "salary": {
      "min": 500000,
      "max": 800000,
      "currency": "INR"
    },
    "location": "Bangalore, Karnataka",
    "skills": ["Python", "FastAPI"],
    "apply_url": "https://...",
    "posted_at": "2025-01-10",
    "freshness": {
      "cached_at": "2025-01-17T10:30:00Z",
      "days_old": 3
    }
  }
}
```

#### 3. Save Job
```
POST /api/jobs/:jobId/save
Auth: Required (user JWT)

Response:
{
  "success": true,
  "message": "Job saved successfully"
}
```

#### 4. Get Saved Jobs
```
GET /api/user/saved-jobs
Auth: Required

Response:
{
  "success": true,
  "jobs": [
    { job object }
  ],
  "total": 10
}
```

---

### Admin API Endpoints

#### 1. Get Scraper Stats
```
GET /api/admin/scraper/stats
Auth: Required (admin)

Response:
{
  "success": true,
  "stats": {
    "scrapedToday": 45,
    "totalJobs": 10234,
    "budgetStatus": {
      "used": 45,
      "remaining": 155,
      "percentUsed": 22,
      "isNearLimit": false
    },
    "cacheStatus": {
      "totalJobs": 10234,
      "lastRefresh": "2025-01-17T10:30:00Z"
    },
    "keywords": {
      "active": 10,
      "stale": 2
    }
  }
}
```

#### 2. Get Budget Status
```
GET /api/admin/scraper/budget
Auth: Required (admin)

Response:
{
  "success": true,
  "budget": {
    "used": 45,
    "remaining": 155,
    "percentUsed": 22,
    "warnings": [],
    "byDate": { "2025-01-17": 5, ... },
    "byKeyword": { "python developer": 1, ... }
  }
}
```

#### 3. Trigger Full Scrape
```
POST /api/admin/scraper/run
Auth: Required (admin)
Body: {}

Response:
{
  "success": true,
  "message": "Scraping started in background",
  "timestamp": "2025-01-17T12:00:00Z"
}
```

#### 4. Add New Keyword
```
POST /api/admin/scraper/add-keyword
Auth: Required (admin)
Body: {
  "keyword": "blockchain developer"
}

Response:
{
  "success": true,
  "keyword": "blockchain developer",
  "jobsAdded": 180,
  "budgetRemaining": 154
}
```

#### 5. Get Keywords
```
GET /api/admin/scraper/keywords
Auth: Required (admin)

Response:
{
  "success": true,
  "keywords": [
    {
      "keyword": "python developer bangalore",
      "fetchedAt": "2025-01-17T10:30:00Z",
      "nextRefreshDate": "2025-01-24T10:30:00Z",
      "isFresh": true,
      "jobsReturned": 245
    }
  ]
}
```

#### 6. Get Logs
```
GET /api/admin/scraper/logs
Query: page, limit
Auth: Required (admin)

Response:
{
  "success": true,
  "logs": [
    {
      "id": "log_...",
      "timestamp": "2025-01-17T10:30:00Z",
      "status": "success",
      "keyword": "python developer",
      "jobsAdded": 200
    }
  ],
  "pagination": { ... }
}
```

#### 7. Get Queue Status
```
GET /api/admin/scraper/queue
Auth: Required (admin)

Response:
{
  "success": true,
  "queue": {
    "active": 10,
    "waiting": 50,
    "completed": 1000,
    "failed": 2
  }
}
```

---

## 7️⃣ FRONTEND PAGES

### User Pages

#### Page 1: SearchPage
```
URL: /search
Description: Main job search interface

Components:
  ├─ Header with logo & navigation
  ├─ SearchBar (input + filters)
  ├─ FilterPanel
  │   ├─ Salary range slider
  │   ├─ Location dropdown
  │   ├─ Skills multi-select
  │   └─ Employment type checkbox
  ├─ ResultsList
  │   └─ JobCard (title, company, salary, location)
  ├─ Pagination
  └─ Footer

Features:
  ✅ Real-time search (~50ms)
  ✅ Filter & sort results
  ✅ Show result count
  ✅ Show "last cached" timestamp
  ✅ Save jobs to favorites
  ✅ Click to view details
```

#### Page 2: JobDetailsPage
```
URL: /jobs/:jobId
Description: Detailed job information

Components:
  ├─ Job header (title, company, location)
  ├─ Summary section (salary, type, remote)
  ├─ Description section (full job text)
  ├─ Requirements section
  ├─ Skills section (with proficiency levels)
  ├─ Company info
  ├─ CTA buttons
  │   ├─ "Apply Now" button → external link
  │   ├─ "Save Job" button
  │   └─ "Share" button
  └─ Related jobs section

Features:
  ✅ Show job freshness ("cached 3 days ago")
  ✅ Save job to favorites
  ✅ Direct apply link
  ✅ Share via email/social
```

#### Page 3: SavedJobsPage
```
URL: /saved-jobs
Description: User's bookmarked jobs

Components:
  ├─ Header with count
  ├─ Filter & sort controls
  ├─ JobCard list
  └─ Empty state (if no saved jobs)

Features:
  ✅ Show saved job count
  ✅ Sort by: date saved, salary, relevance
  ✅ Remove from saved
  ✅ Quick actions (apply, view)
```

#### Page 4: AppliedJobsPage
```
URL: /applied-jobs
Description: Jobs user has applied to

Components:
  ├─ Status column (applied, interviewing, rejected, offered)
  ├─ Date applied column
  ├─ Follow-up actions

Features:
  ✅ Track application status
  ✅ Add notes
  ✅ Reminder notifications
```

---

### Admin Pages

#### Page 1: ScraperDashboard
```
URL: /admin/dashboard
Description: Real-time scraper statistics

Layout:
  ┌─────────────────────────────────┐
  │  STATS CARDS (Top)              │
  │  ├─ API Usage: 45/200 (22%)    │
  │  ├─ Jobs Cached: 10,234        │
  │  ├─ Keywords: 10 active        │
  │  └─ Last Refresh: 2 hours ago  │
  ├─────────────────────────────────┤
  │  BUDGET GAUGE (Middle)          │
  │  ├─ Visual progress bar        │
  │  ├─ Color coding (green/yellow │
  │  ├─ Action buttons:             │
  │  │   ├─ "Refresh Now"           │
  │  │   ├─ "Add Keyword"           │
  │  │   └─ "View Logs"             │
  ├─────────────────────────────────┤
  │  RECENT ACTIVITY (Bottom)       │
  │  ├─ Last 5 scrapes             │
  │  ├─ Jobs added per scrape      │
  │  └─ Errors (if any)            │
  └─────────────────────────────────┘

Real-time Updates:
  ✅ Refresh every 30 seconds
  ✅ Show live queue status
  ✅ WebSocket alerts on budget warnings
```

#### Page 2: BudgetMonitorPage
```
URL: /admin/budget
Description: Detailed budget tracking

Sections:
  1. Current Month Status
     ├─ Usage: 45/200
     ├─ Remaining: 155
     ├─ % Used: 22%
     └─ Days left: 14 days

  2. Daily Breakdown
     ├─ Chart: Requests per day
     ├─ Table: Date | Count | Keywords
     └─ Trend analysis

  3. Keyword Breakdown
     ├─ Chart: Requests per keyword
     ├─ Table: Keyword | Count | Last Fetch
     └─ Recommendations

  4. Historical Data
     ├─ Previous months
     ├─ Trend analysis
     └─ Projections

Features:
  ✅ Export to CSV
  ✅ Alert when >= 80%
  ✅ Alert when >= 180 (hard stop)
  ✅ Recommendation engine
```

#### Page 3: KeywordManagerPage
```
URL: /admin/keywords
Description: Manage scraping keywords

Layout:
  ┌─────────────────────────────┐
  │  ADD NEW KEYWORD (Top)      │
  │  ├─ Input field             │
  │  ├─ "Add Keyword" button    │
  │  └─ Budget check notification
  ├─────────────────────────────┤
  │  KEYWORD LIST (Main)        │
  │  Columns:                   │
  │  ├─ Keyword name            │
  │  ├─ Fetched date            │
  │  ├─ Next refresh date       │
  │  ├─ Jobs returned           │
  │  ├─ Status (fresh/stale)    │
  │  └─ Actions                 │
  │      ├─ Refresh Now         │
  │      └─ Delete              │
  └─────────────────────────────┘

Features:
  ✅ Add new keywords
  ✅ Manual refresh
  ✅ Mark as paused
  ✅ Delete keywords
  ✅ Show refresh schedule
  ✅ Show staleness indicator
```

#### Page 4: LogViewerPage
```
URL: /admin/logs
Description: Audit trail & debugging

Columns:
  ├─ Timestamp
  ├─ Keyword
  ├─ Status (success/failure)
  ├─ Type (manual/scheduled)
  ├─ Jobs Added
  ├─ Duration
  ├─ Errors
  └─ Budget After

Features:
  ✅ Filter by: date, status, keyword
  ✅ Sort by: timestamp, jobs added, duration
  ✅ Search logs
  ✅ Download logs as CSV
  ✅ Show error details
  ✅ Pagination (50 items/page)
```

---

## 8️⃣ USER ROLES & PERMISSIONS

### Role 1: Regular User (End User)

**Capabilities:**
```
✅ Search jobs
✅ View job details
✅ Save jobs to favorites
✅ View saved jobs
✅ Track applications
✅ View job alerts

❌ Cannot: Access admin features
❌ Cannot: Trigger scraping
❌ Cannot: See API budget
❌ Cannot: Manage keywords
```

**Pages accessible:**
- SearchPage
- JobDetailsPage
- SavedJobsPage
- AppliedJobsPage

**API permissions:**
- GET /api/search
- GET /api/jobs/:jobId
- POST /api/jobs/:jobId/save
- GET /api/user/saved-jobs

---

### Role 2: Admin

**Capabilities:**
```
✅ Everything regular user can do
✅ View scraper dashboard
✅ Monitor API budget
✅ Manually trigger scraping
✅ Add/edit/delete keywords
✅ View audit logs
✅ See real-time queue status
✅ Clear job queue (dangerous)

❌ Cannot: Modify user accounts
❌ Cannot: Delete jobs
❌ Cannot: Access production logs (server-only)
```

**Pages accessible:**
- All user pages +
- ScraperDashboard
- BudgetMonitorPage
- KeywordManagerPage
- LogViewerPage

**API permissions:**
- All user endpoints +
- GET /api/admin/scraper/stats
- GET /api/admin/scraper/budget
- POST /api/admin/scraper/run
- POST /api/admin/scraper/add-keyword
- GET /api/admin/scraper/keywords
- GET /api/admin/scraper/logs
- GET /api/admin/scraper/queue

---

### Role 3: System (Background)

**Capabilities:**
```
✅ Run CRON jobs
✅ Update keywords.json
✅ Append to jobs.json
✅ Update usage.json
✅ Create scraping logs

❌ Cannot: Bypass budget limits
❌ Cannot: Delete files
❌ Cannot: Access frontend
```

**Operations:**
- Weekly keyword refresh (Sunday 2 AM)
- Daily log cleanup (2 AM)
- Monthly usage reset (1st of month)

---

## 9️⃣ DATA & USER FLOW

### Typical User Flow:

```
1. User visits /search
   ├─ Page loads
   ├─ Focus on SearchBar
   └─ Show recent searches

2. User types "Python Developer"
   ├─ Backend checks keywords.json
   ├─ Found in cache (yesterday)
   ├─ Query jobs.json (50ms)
   └─ Show 50 results instantly

3. User clicks on a job
   ├─ Navigate to /jobs/:jobId
   ├─ Load job details from cache
   └─ Show full description

4. User clicks "Save Job"
   ├─ Send POST /api/jobs/:jobId/save
   ├─ Save to user's saved list
   └─ Show confirmation

5. User clicks "Apply Now"
   ├─ Open external apply_url
   └─ Redirect to company career page
```

### Typical Admin Flow:

```
1. Admin visits /admin/dashboard
   ├─ See real-time stats
   ├─ Usage: 45/200 (safe)
   └─ See recent activity

2. Admin wants to add new keyword
   ├─ Click "Add Keyword"
   ├─ Type "Blockchain Developer"
   ├─ System checks budget (OK)
   ├─ Trigger API call
   ├─ Get 180 new jobs
   ├─ Show success message
   └─ Budget now: 46/200

3. Admin checks budget page
   ├─ See daily breakdown chart
   ├─ See keyword breakdown
   ├─ See trends
   └─ Decide if need to pause scraping

4. Admin checks logs
   ├─ Filter by status
   ├─ View error details
   ├─ Export logs
   └─ Find bugs
```

---

## 🔟 IMPLEMENTATION CHECKLIST

### Setup Phase:
- [ ] Create project directory structure
- [ ] Initialize Git repository
- [ ] Create .env.example file
- [ ] Create initial JSON data files

### Backend Services Phase:
- [ ] Implement usageTracker.ts
- [ ] Implement keywordDedup.ts
- [ ] Implement jsonDatabase.ts
- [ ] Write unit tests for each service

### Integration Phase:
- [ ] Modify JSearchClient (add budget check)
- [ ] Modify JobScraperService (add JSON save)
- [ ] Create searchController
- [ ] Create adminScraperController
- [ ] Update scraperScheduler

### Routing Phase:
- [ ] Create search routes
- [ ] Create admin routes
- [ ] Add auth middleware
- [ ] Add error handling

### Automation Phase:
- [ ] Set up CRON scheduler
- [ ] Set up daily cleanup job
- [ ] Test scheduling

### Frontend Phase:
- [ ] Create SearchPage component
- [ ] Create JobDetailsPage component
- [ ] Create SavedJobsPage component
- [ ] Create ScraperDashboard
- [ ] Create BudgetMonitorPage
- [ ] Create KeywordManagerPage
- [ ] Create LogViewerPage

### Testing Phase:
- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests
- [ ] E2E tests
- [ ] Load testing

### Deployment Phase:
- [ ] Deploy to staging
- [ ] Run full test suite
- [ ] Deploy to production
- [ ] Monitor for errors
- [ ] Document runbook

---

## 📚 RELATED FILES

All analysis & requirements in these README files:

1. **DEVELOPMENT_PLAN.md** ← You are here
2. **FILE_STRUCTURE.md** - Detailed folder layout
3. **DATABASE_SCHEMAS.md** - JSON schemas & models
4. **API_ENDPOINTS.md** - All backend routes
5. **FRONTEND_PAGES.md** - UI/UX requirements
6. **DEPENDENCIES.md** - npm packages needed
7. **DEPLOYMENT_GUIDE.md** - Production setup
8. **TESTING_STRATEGY.md** - QA plan

---

## ✅ NEXT STEPS

1. **Read** this entire README
2. **Review** DEEP_ANALYSIS_3COMPONENT_INTEGRATION.md
3. **Check** REQUIRED_CHANGES_SUMMARY.md
4. **Start** with Phase 1 (Setup)
5. **Follow** this development plan week by week

---

**Total Development Time: 3-4 weeks**  
**Team Size: 1-2 developers**  
**Skill Requirements: Node.js, React, TypeScript, REST API**

Ready to start? Begin with the Setup Phase! 🚀
