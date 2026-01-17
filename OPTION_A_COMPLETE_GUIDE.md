# 🚀 OPTION A: COMPLETE INTEGRATION GUIDE
**LinkedIn Scraper → JobIntel Platform**

---

## 📋 OVERVIEW

This guide provides **ready-to-use TypeScript code** to integrate the Python LinkedIn scraper directly into your Node.js/Express backend.

**Timeline**: 2-3 weeks  
**Files to Create**: 7 new files  
**Complexity**: Medium  
**Payoff**: 10x more jobs, zero maintenance

---

## 📦 FILES PROVIDED

All code is in reference files. Copy the TypeScript code from:

| Step | File | Purpose |
|------|------|---------|
| 1 | `INTEGRATION_OPTION_A_STEP1.ts` | JSearch API Client |
| 2 | `INTEGRATION_OPTION_A_STEP2.ts` | Job Scraper Service |
| 3 | `INTEGRATION_OPTION_A_STEP3.ts` | Job Ingestion Queue (BullMQ) |
| 4 | `INTEGRATION_OPTION_A_STEP4.ts` | Scheduler (Cron) |
| 5 | `INTEGRATION_OPTION_A_STEP5.ts` | Admin Controller & Routes |
| Setup | `INTEGRATION_OPTION_A_SETUP.ts` | Environment & Models |

---

## 🎯 QUICK START (5 Minutes)

### Step 1: Install Dependencies
```bash
cd your-jobintel-backend
npm install axios bull redis node-cron
npm install --save-dev @types/node-cron
```

### Step 2: Update `.env`
```bash
# Add to backend/.env
JSEARCH_API_KEY=ak_58a8asv2uix2dbxls7sitbar9zq647ld0iqbio1phiz29ar
REDIS_URL=redis://localhost:6379
SCRAPER_ENABLED=true
```

### Step 3: Start Redis (in another terminal)
```bash
redis-server
```

### Step 4: Copy Code Files
Create these files in your backend with code from reference files:
- `backend/services/jsearchClient.ts`
- `backend/services/jobScraperService.ts`
- `backend/queues/jobIngestionQueue.ts`
- `backend/jobs/scraperScheduler.ts`
- `backend/controllers/adminScraperController.ts`
- `backend/routes/adminScraperRoutes.ts`

### Step 5: Update Models
```bash
# In backend/models/Job.ts, add these fields:
source: { type: String, enum: ['jsearch', 'manual'], index: true }
source_metadata: { ... }
is_duplicate: { type: Boolean, default: false }
embedding: [Number]

# Create backend/models/ScrapingLog.ts (see INTEGRATION_OPTION_A_SETUP.ts)
```

### Step 6: Initialize Scheduler
```typescript
// In backend/server.ts
import { initializeScheduler } from './jobs/scraperScheduler'

if (process.env.SCRAPER_ENABLED === 'true') {
  initializeScheduler(process.env.JSEARCH_API_KEY!)
}

app.use('/api/admin/scraper', adminScraperRoutes)
```

### Step 7: Start Server
```bash
npm run dev
```

**That's it! ✅ Scraper is now running!**

---

## 🔄 DATA FLOW

```
┌─────────────────────────┐
│  OpenWeb Ninja API      │  (Real job data)
│  1 request/second       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  JSearchClient Service  │  (Parse & validate)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  JobScraperService      │  (Deduplicate)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  BullMQ Job Queue       │  (Reliable delivery)
│  Redis-backed           │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Save to MongoDB        │  (Job collection)
│  Generate Embedding     │  (OpenAI)
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  Trigger Matching       │  (Compare with resumes)
│  Send Notifications     │  (Email users)
└─────────────────────────┘
```

---

## 📊 WHAT HAPPENS AUTOMATICALLY

### Every 3 Hours:
- Searches: "software engineer", "data scientist", "frontend developer", etc.
- Results: ~50-100 new jobs
- Processing: Auto-queued, deduplicated, matched, stored

### Every 6 Hours:
- Full scrape of all 10 predefined searches
- Results: ~100-200 new unique jobs
- Storage: Saved to MongoDB with embeddings

### Daily at 2 AM:
- Cleanup old scraping logs (keep 30 days)
- Remove old queue entries

---

## 🎛️ ADMIN ENDPOINTS

### 1. **Get Scraper Statistics**
```bash
GET /api/admin/scraper/stats
```
Response:
```json
{
  "success": true,
  "stats": {
    "scrapedToday": 45,
    "canonicalCount": 1250,
    "duplicateCount": 120,
    "queueStatus": {
      "active": 8,
      "waiting": 45,
      "completed": 1200,
      "failed": 2
    }
  }
}
```

### 2. **Manually Trigger Scrape**
```bash
POST /api/admin/scraper/run
```
Response:
```json
{
  "success": true,
  "message": "Scraping started in background"
}
```

### 3. **Get Scraping Logs**
```bash
GET /api/admin/scraper/logs?page=1&limit=50
```

### 4. **Get Job Analytics**
```bash
GET /api/admin/scraper/analytics
```
Shows: Status breakdown, source breakdown, top companies, top locations

### 5. **Get Queue Status**
```bash
GET /api/admin/scraper/queue
```
Shows: Active jobs, failed jobs, waiting jobs

---

## 🧪 TESTING

### Test 1: API Connection
```bash
curl http://localhost:4000/api/admin/scraper/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Test 2: Manual Scrape
```bash
curl -X POST http://localhost:4000/api/admin/scraper/run \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Then check results after 2-3 minutes
curl http://localhost:4000/api/admin/scraper/queue \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Test 3: Database Query
```bash
# In MongoDB
db.jobs.find({ source: "jsearch" }).count()
# Should see increasing number of jobs
```

---

## 🚨 TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| "JSEARCH_API_KEY not set" | Add to `.env`: `JSEARCH_API_KEY=ak_...` |
| "Redis connection refused" | Start Redis: `redis-server` or install with `brew install redis` |
| "No jobs being scraped" | Check logs for errors, verify API key is valid |
| "Duplicates showing up" | Check deduplication logic, may need to rebuild indexes |
| "Embeddings not generated" | Verify `OPENAI_API_KEY` is set and has credit |
| "Scheduler not running" | Set `SCRAPER_ENABLED=true` in `.env` |

---

## 📈 EXPECTED RESULTS

**After 24 hours:**
- ✅ 400-600 new jobs in database
- ✅ All jobs have embeddings
- ✅ Job matches created for users
- ✅ Notifications sent to matched users
- ✅ Scraping logs available
- ✅ Queue processing jobs smoothly

**After 1 week:**
- ✅ 2,000-3,000 total jobs
- ✅ Duplicate detection working
- ✅ User matches improving
- ✅ System stable and scalable

---

## 💰 COST & LIMITS

**API Plan:**
- Free tier: 200 requests/month ⚠️ **NOT ENOUGH**
- Professional: 10,000 requests/month ✅ **$50/month**
- Business: 100,000 requests/month = $250/month

**Current Load:**
- Requests/day: 60 (10 searches × 6 times)
- Requests/month: 1,800
- **Need: Professional plan ($50/month)**

---

## 🛠️ INTEGRATION CHECKLIST

### Week 1:
- [ ] Day 1: Install dependencies
- [ ] Day 2: Create JSearchClient service
- [ ] Day 3: Create JobScraperService
- [ ] Day 4: Set up BullMQ queue
- [ ] Day 5: Test queue processing
- [ ] Day 6-7: Debugging & fixes

### Week 2:
- [ ] Create scheduler with cron
- [ ] Create admin controller & routes
- [ ] Update Job model
- [ ] Update database indexes
- [ ] Test manual scraping
- [ ] Test automatic scheduling
- [ ] Integration testing

### Week 3:
- [ ] Migrate existing jobs
- [ ] Deploy to staging
- [ ] 24-hour staging test
- [ ] Deploy to production
- [ ] Monitor for errors
- [ ] Fine-tune parameters

---

## 📱 FRONTEND INTEGRATION (Optional)

**Show scraper status in admin dashboard:**

```typescript
// frontend/pages/admin/ScraperDashboard.tsx

export function ScraperDashboard() {
  const [stats, setStats] = useState(null)
  
  useEffect(() => {
    // Poll every 10 seconds
    const interval = setInterval(async () => {
      const res = await fetch('/api/admin/scraper/stats')
      const data = await res.json()
      setStats(data.stats)
    }, 10000)
    
    return () => clearInterval(interval)
  }, [])
  
  return (
    <div>
      <h1>Job Scraper Dashboard</h1>
      <div className="grid grid-cols-4 gap-4">
        <StatCard 
          label="Jobs Today"
          value={stats?.scrapedToday}
          icon="📊"
        />
        <StatCard 
          label="Queue"
          value={`${stats?.queueStatus.active} active`}
          icon="⏳"
        />
        <StatCard 
          label="Duplicates"
          value={stats?.duplicateCount}
          icon="🔄"
        />
        <StatCard 
          label="Total Jobs"
          value={stats?.canonicalCount}
          icon="💼"
        />
      </div>
      
      <button onClick={() => fetch('/api/admin/scraper/run', {method: 'POST'})}>
        Run Scraper Now
      </button>
    </div>
  )
}
```

---

## 🎓 NEXT STEPS

1. **Immediate** (Today):
   - Read this guide completely
   - Review code files
   - Install dependencies

2. **This Week**:
   - Implement services (Steps 1-4)
   - Set up database models
   - Test API connection

3. **Next Week**:
   - Create admin routes
   - Deploy to staging
   - Run full integration test

4. **Production** (Week 3):
   - Deploy to production
   - Monitor 24/7
   - Adjust parameters as needed

---

## 📞 SUPPORT

**If you get stuck:**

1. Check `Troubleshooting` section above
2. Review logs in MongoDB (ScrapingLog collection)
3. Check queue status with `/api/admin/scraper/queue`
4. Test API directly with JSearchClient test script
5. Review error messages in server logs

---

## ✅ SUCCESS CRITERIA

Your integration is **COMPLETE** when:

✅ Jobs are being scraped automatically  
✅ Queue is processing jobs without errors  
✅ New jobs appear in MongoDB every 3-6 hours  
✅ Admin endpoints return data  
✅ Job embeddings are generated  
✅ User matches are created  
✅ Notifications are sent  
✅ Zero errors in production logs  

---

## 🚀 DEPLOYMENT

Once working locally:

```bash
# Build for production
npm run build

# Deploy to your hosting (Render, Heroku, etc.)
git push heroku main

# Verify in production
curl https://your-api.com/api/admin/scraper/stats
```

Redis options:
- **Free**: Self-hosted Redis (complex)
- **Easy**: Redis Cloud ($15/month)
- **Cloud**: AWS ElastiCache ($20+/month)

---

**You're ready to integrate! Start with Step 1 today. 🚀**
