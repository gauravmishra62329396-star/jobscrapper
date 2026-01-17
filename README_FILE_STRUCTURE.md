# 📁 FILE STRUCTURE & ORGANIZATION README
**Complete Backend & Frontend Layout**

---

## 📋 TABLE OF CONTENTS

1. Backend Structure
2. Frontend Structure
3. Data Directory
4. Configuration Files
5. Environment Setup
6. Directory Creation Commands
7. File Dependencies Graph

---

## 1️⃣ BACKEND STRUCTURE

### Core Services Layer

```
backend/services/
├── usageTracker.ts
│   ├── Exported: UsageTracker class, getUsageTracker()
│   ├── Methods:
│   │   ├── initialize() - Load from usage.json
│   │   ├── canMakeRequest() - Check if budget allows API call
│   │   ├── increment(keyword) - Add 1 to request count
│   │   ├── getUsageStats() - Get current stats
│   │   ├── getRemainingBudget() - Get remaining requests
│   │   └── flush() - Save to disk
│   ├── Dependencies: fs, Logger
│   └── Reads/Writes: data/usage.json
│
├── keywordDedup.ts
│   ├── Exported: KeywordDedup class, getKeywordDedup()
│   ├── Methods:
│   │   ├── initialize() - Load from keywords.json
│   │   ├── isDuplicate(keyword) - Check if fetched recently
│   │   ├── markAsFetched(keyword) - Record fetch
│   │   ├── getAllKeywords() - Get all tracked keywords
│   │   ├── getStaleKeywords() - Get keywords needing refresh
│   │   └── getKeywordStats() - Get stats
│   ├── Dependencies: fs, Logger
│   └── Reads/Writes: data/keywords.json
│
└── jsonDatabase.ts
    ├── Exported: JsonDatabase class, getJsonDatabase()
    ├── Methods:
    │   ├── initialize() - Load jobs.json, build indexes
    │   ├── search(query, filters) - Query in-memory (instant)
    │   ├── appendJobs(newJobs) - Add jobs atomically
    │   ├── jobExists(dedupKey) - Check if job exists
    │   ├── getTotalJobs() - Get job count
    │   ├── getLastRefresh() - Get last update time
    │   └── buildIndexes() - Rebuild search indexes
    ├── Dependencies: fs, Logger
    └── Reads/Writes: data/jobs.json
```

### API Services (MODIFIED)

```
backend/services/
├── jsearchClient.ts (MODIFIED)
│   ├── NEW: Call usageTracker.canMakeRequest() before API
│   ├── NEW: Call keywordDedup.isDuplicate() before API
│   ├── NEW: Call usageTracker.increment() after success
│   ├── NEW: Call jsonDatabase.appendJobs() to save results
│   ├── NEW: Call jsonDatabase.updateKeyword() to mark fetched
│   ├── Existing: Rate limiting (1 req/sec)
│   ├── Existing: Retry logic
│   └── Existing: Error handling
│
└── jobScraperService.ts (MODIFIED)
    ├── NEW: Rename scrapeJobs() → smartScrapeJobs()
    ├── NEW: Add budget check at start
    ├── NEW: Add dedup check at start
    ├── NEW: Save to JSON instead of MongoDB
    ├── NEW: Update keyword metadata
    ├── Existing: Parse job fields
    ├── Existing: Deduplication logic
    ├── Existing: Skill extraction
    └── Existing: Salary parsing
```

### Controllers Layer

```
backend/controllers/
├── searchController.ts (NEW)
│   ├── Exported Functions:
│   │   ├── searchJobs(req, res)
│   │   │   ├─ Query params: q, limit, offset, minSalary, filters
│   │   │   ├─ Call jsonDatabase.search()
│   │   │   └─ Return results instantly (<100ms)
│   │   ├── getJobDetails(req, res)
│   │   │   └─ Get full job from cache
│   │   ├── getSearchSuggestions(req, res)
│   │   │   └─ Return autocomplete suggestions
│   │   └── getSearchFilters(req, res)
│   │       └─ Return available filter options
│   ├── Dependencies: jsonDatabase, Logger
│   └── Error handling: 404, 400
│
└── adminScraperController.ts (MODIFIED)
    ├── MODIFIED: getScraperStats()
    │   ├─ Add budgetStatus object
    │   ├─ Add cacheStatus object
    │   └─ Show JSON-based stats (not MongoDB)
    ├── NEW: getBudgetStatus()
    │   ├─ Return detailed budget breakdown
    │   ├─ Show daily/keyword breakdown
    │   └─ Show recommendations
    ├── MODIFIED: triggerFullScrape()
    │   ├─ Add budget check before start
    │   └─ Block if usage >= 180
    ├── NEW: addKeywordManually()
    │   ├─ Check budget
    │   ├─ Check if duplicate
    │   ├─ Trigger scrape if OK
    │   └─ Return budget remaining
    ├── NEW: getKeywordStatus()
    │   ├─ List all keywords
    │   ├─ Show freshness indicators
    │   └─ Show next refresh dates
    ├── MODIFIED: getQueueStats()
    │   └─ Return queue info (unchanged)
    ├── EXISTING: getJobAnalytics()
    │   └─ Analytics from jobs (unchanged)
    ├── EXISTING: getScrapingLogs()
    │   └─ Return scraping logs (unchanged)
    └── EXISTING: clearJobQueue()
        └─ Clear queue with confirmation
```

### Routes Layer

```
backend/routes/
├── searchRoutes.ts (NEW)
│   ├── GET /api/search
│   │   └─ Call searchController.searchJobs()
│   ├── GET /api/search/suggestions
│   │   └─ Call searchController.getSearchSuggestions()
│   ├── GET /api/jobs/:jobId
│   │   └─ Call searchController.getJobDetails()
│   └── GET /api/search/filters
│       └─ Call searchController.getSearchFilters()
│
└── adminScraperRoutes.ts (MODIFIED)
    ├── GET /api/admin/scraper/stats
    │   └─ Call adminScraperController.getScraperStats()
    ├── NEW: GET /api/admin/scraper/budget
    │   └─ Call adminScraperController.getBudgetStatus()
    ├── POST /api/admin/scraper/run
    │   └─ Call adminScraperController.triggerFullScrape()
    ├── NEW: POST /api/admin/scraper/add-keyword
    │   └─ Call adminScraperController.addKeywordManually()
    ├── NEW: GET /api/admin/scraper/keywords
    │   └─ Call adminScraperController.getKeywordStatus()
    ├── GET /api/admin/scraper/logs
    │   └─ Call adminScraperController.getScrapingLogs()
    ├── GET /api/admin/scraper/queue
    │   └─ Call adminScraperController.getQueueStats()
    ├── GET /api/admin/scraper/analytics
    │   └─ Call adminScraperController.getJobAnalytics()
    └── DELETE /api/admin/scraper/queue
        └─ Call adminScraperController.clearJobQueue()
```

### Scheduler & Jobs

```
backend/jobs/
├── scraperScheduler.ts (MODIFIED)
│   ├── MODIFIED: Use budgetTracker for budget checks
│   ├── MODIFIED: Use keywordDedup to find stale keywords
│   ├── MODIFIED: Save to JSON via jsonDatabase
│   ├── Methods:
│   │   ├── initialize() - Set up CRON jobs
│   │   ├── runFullScrape() - Fetch all 10 core keywords
│   │   ├── runPredefinedSearches() - Fetch subset
│   │   ├── runWeeklyRefresh() - Refresh stale keywords
│   │   └── runDailyCleanup() - Remove old logs
│   ├── CRON schedules:
│   │   ├─ 0 2 * * 0 (Sunday 2 AM) - Weekly full refresh
│   │   ├─ 0 2 * * * (Daily 2 AM) - Log cleanup
│   │   └─ 0 */6 * * * (Every 6 hours) - Predefined refresh
│   └── Dependencies: usageTracker, keywordDedup, jobScraperService
│
└── cleanupJob.ts (NEW)
    ├── Exported: runCleanup()
    ├── Operations:
    │   ├─ Remove logs older than 30 days
    │   ├─ Remove old backups
    │   ├─ Compress old logs
    │   └─ Calculate storage stats
    ├── Dependencies: fs, Logger
    └── Runs: Daily at 2 AM
```

### Middleware Layer

```
backend/middleware/
├── auth.ts
│   ├── authenticateToken(req, res, next)
│   │   └─ Verify JWT from Authorization header
│   ├── requireRole(role)
│   │   └─ Middleware factory for role checking
│   ├── canAccessAdmin(req, res, next)
│   │   └─ Check if user is admin
│   └── logRequest(req, res, next)
│       └─ Log all API calls
│
├── errorHandler.ts
│   ├── handleError(err, req, res, next)
│   │   ├─ Catch all errors
│   │   ├─ Format error response
│   │   └─ Log to logger
│   └── notFound(req, res, next)
│       └─ 404 handler
│
└── rateLimit.ts
    ├── apiRateLimit(req, res, next)
    │   └─ Limit requests per IP
    └── adminRateLimit(req, res, next)
        └─ Stricter limit for admin endpoints
```

### Utilities Layer

```
backend/utils/
├── logger.ts
│   ├── export class Logger
│   ├── Methods: info(), debug(), warn(), error()
│   └── Logs to: console + file (logs/app.log)
│
├── validators.ts
│   ├── validateSearchQuery(query)
│   ├── validateKeyword(keyword)
│   ├── validateFilters(filters)
│   └── validateJobId(id)
│
└── formatters.ts
    ├── formatJob(rawJob)
    ├── formatBudgetResponse(stats)
    ├── formatKeywordResponse(keyword)
    └── formatLogResponse(log)
```

### Configuration

```
backend/config/
└── constants.ts
    ├── API Settings:
    │   ├─ MAX_MONTHLY_BUDGET = 200
    │   ├─ HARD_STOP_THRESHOLD = 180
    │   ├─ WARNING_THRESHOLD = 160
    │   └─ RATE_LIMIT_MS = 1000
    ├─ Database Settings:
    │   ├─ JSON_DB_PATH = ./data
    │   ├─ BACKUP_INTERVAL = 360000 (6 hours)
    │   └─ RETENTION_DAYS = 30
    ├─ Scheduler Settings:
    │   ├─ CRON_FULL_REFRESH = "0 2 * * 0"
    │   ├─ CRON_CLEANUP = "0 2 * * *"
    │   └─ PREDEFINED_KEYWORDS = [...]
    └─ Feature Flags:
        ├─ ENABLE_SCHEDULER = true
        ├─ ENABLE_AUTO_BACKUP = true
        └─ ENABLE_LOGGING = true
```

### Tests

```
backend/__tests__/
├── services/
│   ├── usageTracker.test.ts
│   │   ├─ Test: Load/save usage
│   │   ├─ Test: Budget enforcement
│   │   ├─ Test: Warning triggers
│   │   └─ Test: Month reset
│   ├── keywordDedup.test.ts
│   │   ├─ Test: Duplicate detection
│   │   ├─ Test: Mark as fetched
│   │   ├─ Test: Get stale keywords
│   │   └─ Test: Normalization
│   └── jsonDatabase.test.ts
│       ├─ Test: Search functionality
│       ├─ Test: Append operations
│       ├─ Test: Indexes
│       └─ Test: Persistence
│
├── controllers/
│   ├── searchController.test.ts
│   │   ├─ Test: Search endpoint
│   │   ├─ Test: Filters
│   │   ├─ Test: Pagination
│   │   └─ Test: Response format
│   └── adminScraperController.test.ts
│       ├─ Test: Budget endpoint
│       ├─ Test: Stats endpoint
│       ├─ Test: Keyword management
│       └─ Test: Auth checks
│
└── integration/
    └── scraper.integration.test.ts
        ├─ Test: Full scraping flow
        ├─ Test: Budget enforcement
        ├─ Test: Data persistence
        └─ Test: Scheduler
```

---

## 2️⃣ FRONTEND STRUCTURE

### Pages Layer

```
frontend/pages/
├── user/
│   ├── SearchPage.tsx
│   │   ├── State:
│   │   │   ├─ query (string)
│   │   │   ├─ results (Job[])
│   │   │   ├─ filters (object)
│   │   │   ├─ loading (boolean)
│   │   │   └─ error (string | null)
│   │   ├── Components:
│   │   │   ├─ <SearchBar />
│   │   │   ├─ <FilterPanel />
│   │   │   ├─ <ResultsList />
│   │   │   └─ <Pagination />
│   │   ├── Hooks:
│   │   │   ├─ useSearch(query, filters)
│   │   │   └─ useLocalStorage('recentSearches')
│   │   └── Features:
│   │       ├─ Real-time search
│   │       ├─ Filter & sort
│   │       ├─ Pagination
│   │       └─ Save favorites
│   │
│   ├── JobDetailsPage.tsx
│   │   ├── State:
│   │   │   ├─ job (Job | null)
│   │   │   ├─ loading (boolean)
│   │   │   └─ saved (boolean)
│   │   ├── Components:
│   │   │   ├─ <JobHeader />
│   │   │   ├─ <JobDescription />
│   │   │   ├─ <Requirements />
│   │   │   ├─ <SkillsList />
│   │   │   ├─ <CompanyInfo />
│   │   │   ├─ <CTASection />
│   │   │   └─ <RelatedJobs />
│   │   ├── Hooks:
│   │   │   ├─ useParams() - Get jobId
│   │   │   ├─ useNavigate() - Go back
│   │   │   └─ useAuth() - Check if logged in
│   │   └── Features:
│   │       ├─ Show job details
│   │       ├─ Show freshness
│   │       ├─ Apply button
│   │       └─ Save button
│   │
│   ├── SavedJobsPage.tsx
│   │   ├── State:
│   │   │   ├─ jobs (Job[])
│   │   │   ├─ loading (boolean)
│   │   │   └─ sortBy (string)
│   │   ├── Components:
│   │   │   ├─ <Header />
│   │   │   ├─ <SortControls />
│   │   │   ├─ <JobsList />
│   │   │   └─ <EmptyState />
│   │   ├── Hooks:
│   │   │   ├─ useAuth() - Check logged in
│   │   │   └─ useQuery() - Fetch saved
│   │   └── Features:
│   │       ├─ Show saved jobs
│   │       ├─ Sort & filter
│   │       └─ Remove from saved
│   │
│   └── AppliedJobsPage.tsx
│       ├── State:
│       │   ├─ applications (Application[])
│       │   └─ loading (boolean)
│       ├── Components:
│       │   ├─ <ApplicationTable />
│       │   ├─ <StatusBadge />
│       │   └─ <ActionButtons />
│       ├── Hooks:
│       │   └─ useApplications() - Fetch user applications
│       └── Features:
│           ├─ Track applications
│           ├─ Show status
│           └─ Add notes
│
└── admin/
    ├── ScraperDashboard.tsx
    │   ├── State:
    │   │   ├─ stats (StatsObject)
    │   │   ├─ loading (boolean)
    │   │   └─ autoRefresh (boolean)
    │   ├── Components:
    │   │   ├─ <StatCards />
    │   │   ├─ <BudgetGauge />
    │   │   ├─ <RecentActivity />
    │   │   └─ <ActionButtons />
    │   ├── Hooks:
    │   │   ├─ useAdmin() - Check admin role
    │   │   ├─ useQuery() - Fetch stats
    │   │   └─ useEffect() - Auto-refresh every 30s
    │   └── Features:
    │       ├─ Real-time stats
    │       ├─ Budget visualization
    │       ├─ Quick actions
    │       └─ Recent activity feed
    │
    ├── BudgetMonitorPage.tsx
    │   ├── State:
    │   │   ├─ budget (BudgetData)
    │   │   ├─ selectedPeriod (string)
    │   │   └─ chart (ChartData)
    │   ├── Components:
    │   │   ├─ <CurrentStatus />
    │   │   ├─ <DailyChart />
    │   │   ├─ <KeywordChart />
    │   │   ├─ <HistoricalData />
    │   │   └─ <ExportButton />
    │   ├── Hooks:
    │   │   ├─ useAdmin() - Check admin
    │   │   └─ useQuery() - Fetch budget data
    │   └── Features:
    │       ├─ Budget breakdown
    │       ├─ Charts & trends
    │       ├─ Export to CSV
    │       └─ Alerts
    │
    ├── KeywordManagerPage.tsx
    │   ├── State:
    │   │   ├─ keywords (Keyword[])
    │   │   ├─ newKeyword (string)
    │   │   └─ loading (boolean)
    │   ├── Components:
    │   │   ├─ <AddKeywordForm />
    │   │   ├─ <KeywordTable />
    │   │   ├─ <RefreshButton />
    │   │   └─ <DeleteButton />
    │   ├── Hooks:
    │   │   ├─ useAdmin()
    │   │   ├─ useQuery() - Fetch keywords
    │   │   └─ useMutation() - Add/delete/refresh
    │   └── Features:
    │       ├─ Add keywords
    │       ├─ Refresh manually
    │       ├─ Delete keywords
    │       └─ Show schedule
    │
    └── LogViewerPage.tsx
        ├── State:
        │   ├─ logs (Log[])
        │   ├─ filters (FilterObject)
        │   ├─ page (number)
        │   └─ loading (boolean)
        ├── Components:
        │   ├─ <FilterBar />
        │   ├─ <LogsTable />
        │   ├─ <Pagination />
        │   └─ <ExportButton />
        ├── Hooks:
        │   ├─ useAdmin()
        │   ├─ useQuery() - Fetch logs
        │   └─ useFilters() - Filter state
        └── Features:
            ├─ Filter by date/status
            ├─ Search logs
            ├─ Export to CSV
            └─ Show details
```

### Components Layer

```
frontend/components/
├── User Components:
│   ├── SearchBar.tsx
│   │   ├─ Props: onSearch(query)
│   │   ├─ Features: Input + autocomplete
│   │   └─ Styling: responsive
│   ├── JobCard.tsx
│   │   ├─ Props: job (Job), onSave()
│   │   ├─ Shows: title, company, salary, location
│   │   └─ Actions: save, apply, view details
│   ├── FilterPanel.tsx
│   │   ├─ Props: onFilter(filters)
│   │   ├─ Filters: salary, location, skills, type
│   │   └─ Styling: collapsible on mobile
│   ├── ResultsList.tsx
│   │   ├─ Props: jobs (Job[]), loading, error
│   │   ├─ Shows: List of JobCards
│   │   └─ Features: infinite scroll or pagination
│   └── Pagination.tsx
│       ├─ Props: current, total, onChange()
│       ├─ Shows: Page numbers
│       └─ Styling: disabled states
│
├── Admin Components:
│   ├── StatCards.tsx
│   │   ├─ Props: stats (object)
│   │   ├─ Shows: 4 stat cards
│   │   └─ Styling: color-coded
│   ├── BudgetGauge.tsx
│   │   ├─ Props: used, total
│   │   ├─ Shows: Progress bar
│   │   └─ Colors: green/yellow/red
│   ├── BudgetWidget.tsx
│   │   ├─ Props: budget (BudgetData)
│   │   ├─ Shows: Remaining budget
│   │   └─ Actions: Refresh button
│   ├── KeywordList.tsx
│   │   ├─ Props: keywords (Keyword[])
│   │   ├─ Shows: Keyword table
│   │   └─ Actions: refresh, delete
│   ├── Charts.tsx
│   │   ├─ Props: data (ChartData)
│   │   ├─ Shows: Line/Bar charts
│   │   └─ Library: Recharts or Chart.js
│   ├── RecentActivity.tsx
│   │   ├─ Props: logs (Log[])
│   │   ├─ Shows: Recent 5 activities
│   │   └─ Styling: timeline format
│   └── AlertBox.tsx
│       ├─ Props: type (error|warning|info), message
│       ├─ Shows: Alert banner
│       └─ Styling: color-coded
│
└── Shared Components:
    ├── Header.tsx
    │   ├─ Shows: Logo, nav, user menu
    │   └─ Features: Responsive navbar
    ├── Layout.tsx
    │   ├─ Shows: Header + Sidebar + Main
    │   └─ Features: Mobile friendly
    ├── LoadingSpinner.tsx
    ├── ErrorMessage.tsx
    └── ConfirmDialog.tsx
```

### Services/API Hooks

```
frontend/services/
├── searchService.ts
│   ├── Functions:
│   │   ├─ searchJobs(query, filters)
│   │   ├─ getJobDetails(jobId)
│   │   ├─ getSuggestions(query)
│   │   └─ getFilters()
│   └── Error handling: retry logic
│
├── adminService.ts
│   ├── Functions:
│   │   ├─ getScraperStats()
│   │   ├─ getBudgetStatus()
│   │   ├─ getKeywords()
│   │   ├─ addKeyword(keyword)
│   │   ├─ triggerScrape()
│   │   └─ getLogs(filters)
│   └── Auth: Include JWT token
│
└── storageService.ts
    ├── Functions:
    │   ├─ saveJob(job)
    │   ├─ getSavedJobs()
    │   ├─ removeSavedJob(jobId)
    │   └─ getSavedApplications()
    └─ Storage: LocalStorage
```

### Hooks

```
frontend/hooks/
├── useSearch.ts
│   ├── Returns: { results, loading, error, search() }
│   └── Calls: searchService.searchJobs()
│
├── useAdmin.ts
│   ├── Returns: { stats, loading, refresh() }
│   └─ Calls: adminService.getScraperStats()
│
├── useBudget.ts
│   ├── Returns: { budget, warning, critical }
│   └─ Calls: adminService.getBudgetStatus()
│
└── useAuth.ts
    ├── Returns: { user, role, isAdmin }
    └─ Calls: authService.getUser()
```

---

## 3️⃣ DATA DIRECTORY

```
data/
├── jobs.json (5-25 MB)
│   ├─ Updated: On API fetch
│   ├─ Accessed: Every search
│   ├─ Format: JSON array
│   └─ Lifecycle: Keep forever
│
├── keywords.json (<100 KB)
│   ├─ Updated: After each fetch
│   ├─ Accessed: Before API call
│   ├─ Format: JSON object
│   └─ Lifecycle: Keep forever
│
├── usage.json (<50 KB)
│   ├─ Updated: After each API call
│   ├─ Accessed: Admin dashboard
│   ├─ Format: JSON object
│   └─ Lifecycle: Keep 12 months
│
├── scraping-logs.json (100-500 KB)
│   ├─ Updated: After each scrape
│   ├─ Accessed: Admin logs
│   ├─ Format: JSON array
│   └─ Lifecycle: Keep 30 days (auto-delete)
│
└── backups/ (Auto-created)
    ├─ jobs.backup.2025-01-17.json
    ├─ jobs.backup.2025-01-18.json
    ├─ keywords.backup.*.json
    └─ Frequency: Every 6 hours
```

---

## 4️⃣ CONFIGURATION FILES

```
backend/
├── .env (GITIGNORE - not committed)
│   ├─ JSEARCH_API_KEY=ak_...
│   ├─ REDIS_URL=redis://...
│   ├─ SCRAPER_ENABLED=true
│   ├─ API_BUDGET_HARD_STOP=180
│   ├─ LOG_LEVEL=info
│   └─ NODE_ENV=development
│
├── .env.example (committed)
│   └─ Template for .env
│
├── .gitignore
│   ├─ node_modules/
│   ├─ .env
│   ├─ data/jobs.json (or committed, depending on preference)
│   ├─ logs/
│   └─ dist/
│
├── package.json
│   ├─ name: "linkedin-scraper-backend"
│   ├─ version: "1.0.0"
│   ├─ dependencies:
│   │   ├─ express
│   │   ├─ axios
│   │   ├─ bull (for queues)
│   │   ├─ redis
│   │   ├─ node-cron
│   │   ├─ typescript
│   │   ├─ dotenv
│   │   ├─ jsonwebtoken
│   │   ├─ bcryptjs
│   │   └─ cors
│   └─ devDependencies:
│       ├─ jest
│       ├─ @types/node
│       ├─ @types/express
│       ├─ ts-node
│       └─ typescript
│
├── tsconfig.json
│   ├─ target: ES2020
│   ├─ module: commonjs
│   ├─ strict: true
│   ├─ rootDir: ./
│   └─ outDir: ./dist
│
└── jest.config.js
    ├─ preset: ts-jest
    ├─ testEnvironment: node
    └─ testMatch: **/__tests__/**/*.test.ts

frontend/
├── .env (GITIGNORE)
│   ├─ REACT_APP_API_URL=http://localhost:4000
│   └─ REACT_APP_ENVIRONMENT=development
│
├── .env.example
│
├── package.json
│   ├─ dependencies:
│   │   ├─ react
│   │   ├─ react-router-dom
│   │   ├─ axios
│   │   ├─ @types/react
│   │   ├─ tailwindcss (or styled-components)
│   │   ├─ recharts (for charts)
│   │   └─ react-query
│   └─ devDependencies:
│       └─ @testing-library/react
│
├── tsconfig.json
│   ├─ target: ES2020
│   ├─ jsx: react
│   └─ lib: [ES2020, DOM]
│
└── vite.config.ts (if using Vite)
```

---

## 5️⃣ ENVIRONMENT SETUP

### .env Template

```bash
# Backend URL
BACKEND_URL=http://localhost:4000

# JSearch API
JSEARCH_API_KEY=ak_58a8asv2uix2dbxls7sitbar9zq647ld0iqbio1phiz29ar
JSEARCH_API_HOST=api.openwebninja.com

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Database
DATABASE_URL=mongodb://localhost:27017/jobscrapper (if using MongoDB for user data)

# JWT
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRY=7d

# Scraper Config
SCRAPER_ENABLED=true
SCRAPER_RATE_LIMIT_PER_SEC=1
API_BUDGET_HARD_STOP=180

# Logging
LOG_LEVEL=info

# Environment
NODE_ENV=development
PORT=4000

# Frontend
REACT_APP_API_URL=http://localhost:4000
REACT_APP_ENVIRONMENT=development
```

---

## 6️⃣ DIRECTORY CREATION COMMANDS

### Create backend structure

```bash
# Core directories
mkdir -p backend/services
mkdir -p backend/controllers
mkdir -p backend/routes
mkdir -p backend/middleware
mkdir -p backend/utils
mkdir -p backend/config
mkdir -p backend/jobs
mkdir -p backend/__tests__/{services,controllers,integration}
mkdir -p backend/logs
mkdir -p data/backups

# Frontend directories
mkdir -p frontend/pages/{user,admin}
mkdir -p frontend/components
mkdir -p frontend/services
mkdir -p frontend/hooks
mkdir -p frontend/styles
mkdir -p frontend/__tests__

# Root
mkdir -p .github/workflows
```

---

## 7️⃣ FILE DEPENDENCIES GRAPH

### Critical Paths:

```
User Search Request:
  frontend/SearchPage.tsx
    → frontend/services/searchService.ts
    → backend/routes/searchRoutes.ts
    → backend/controllers/searchController.ts
    → backend/services/jsonDatabase.ts
    ↓
  data/jobs.json (in-memory, <50ms)

Admin Budget Check:
  frontend/admin/BudgetMonitorPage.tsx
    → frontend/services/adminService.ts
    → backend/routes/adminScraperRoutes.ts
    → backend/controllers/adminScraperController.ts
    → backend/services/usageTracker.ts
    ↓
  data/usage.json (read)

Scraping Flow:
  backend/jobs/scraperScheduler.ts
    → backend/services/jobScraperService.ts
    ├─→ backend/services/usageTracker.ts (check budget)
    ├─→ backend/services/keywordDedup.ts (check duplicate)
    ├─→ backend/services/jsearchClient.ts (call API)
    └─→ backend/services/jsonDatabase.ts (save results)
    ↓
  data/{jobs.json, keywords.json, usage.json, scraping-logs.json}
```

---

## ✅ CHECKLIST: File Creation Order

1. **Create directories**
   - [ ] Backend services
   - [ ] Backend controllers
   - [ ] Backend routes
   - [ ] Frontend pages
   - [ ] Data folders

2. **Create core services**
   - [ ] usageTracker.ts
   - [ ] keywordDedup.ts
   - [ ] jsonDatabase.ts

3. **Create routes & controllers**
   - [ ] searchRoutes.ts
   - [ ] searchController.ts
   - [ ] Update adminScraperRoutes.ts

4. **Create frontend pages**
   - [ ] SearchPage.tsx
   - [ ] JobDetailsPage.tsx
   - [ ] ScraperDashboard.tsx

5. **Create configuration**
   - [ ] .env.example
   - [ ] package.json
   - [ ] tsconfig.json

---

**Next: See DATABASE_SCHEMAS.md for complete model definitions** 📊
