#!/bin/bash

################################################################################
# 🚀 AUTOMATED SETUP SCRIPT FOR JOB SCRAPPER INTEGRATION
# 
# This script sets up your entire project structure with all reference files
# Run: bash quick-setup.sh
################################################################################

set -e  # Exit on any error

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         🚀 JOB SCRAPPER INTEGRATION SETUP                      ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Get project name
PROJECT_NAME="${1:-.}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "📍 Project location: $PROJECT_NAME"
echo ""

# Step 1: Create directory structure
echo "📁 Step 1/6: Creating directory structure..."
mkdir -p "$PROJECT_NAME"/{src/{services,controllers,routes,jobs,types,middleware,__tests__/{services,controllers}},src/{pages/user,pages/admin,components,hooks,services},data,config,.github/workflows}
echo "✅ Directories created"

# Step 2: Create JSON data files
echo ""
echo "📄 Step 2/6: Creating data files..."

cat > "$PROJECT_NAME/data/jobs.json" << 'EOF'
{
  "jobs": [],
  "totalJobs": 0,
  "lastUpdated": "2026-01-17T00:00:00Z"
}
EOF

cat > "$PROJECT_NAME/data/keywords.json" << 'EOF'
{
  "keywords": [
    { "keyword": "React Developer", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "Node.js Developer", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "Full Stack Developer", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "Python Developer", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "DevOps Engineer", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "Frontend Developer", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "Backend Developer", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "Data Scientist", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "Mobile Developer", "lastFetched": null, "fetchCount": 0, "isActive": true },
    { "keyword": "QA Engineer", "lastFetched": null, "fetchCount": 0, "isActive": true }
  ],
  "totalKeywords": 10
}
EOF

cat > "$PROJECT_NAME/data/usage.json" << 'EOF'
{
  "month": "2026-01",
  "requestsUsed": 0,
  "requestsLimit": 200,
  "warningThreshold": 160,
  "hardStopThreshold": 180,
  "createdAt": "2026-01-17T00:00:00Z",
  "resetAt": "2026-02-01T00:00:00Z"
}
EOF

cat > "$PROJECT_NAME/data/scraping-logs.json" << 'EOF'
{
  "logs": [],
  "totalLogs": 0
}
EOF

echo "✅ Data files created"

# Step 3: Create .env file
echo ""
echo "⚙️  Step 3/6: Creating .env configuration..."

cat > "$PROJECT_NAME/.env" << 'EOF'
# Free-Tier API Configuration
JSERCH_API_KEY=your_api_key_here
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
EOF

echo "✅ .env file created"

# Step 4: Create .env.example
echo ""
echo "📝 Step 4/6: Creating .env.example..."

cat > "$PROJECT_NAME/.env.example" << 'EOF'
# Copy this to .env and fill in your values

JSERCH_API_KEY=your_api_key_here
JSERCH_API_URL=https://api.openwebninja.com/api/jserch

API_REQUEST_LIMIT=200
API_MONTHLY_BUDGET=100
API_WARNING_THRESHOLD=160
API_HARD_STOP_THRESHOLD=180

CACHE_TTL_MINUTES=1440
CACHE_REFRESH_DAYS=7
CACHE_HIT_TARGET=0.9

DATA_DIR=./data
JOBS_FILE=./data/jobs.json
KEYWORDS_FILE=./data/keywords.json
USAGE_FILE=./data/usage.json
LOGS_FILE=./data/scraping-logs.json

ENABLE_SCHEDULER=true
SCRAPER_CRON_TIME=0 0 * * 0
CLEANUP_CRON_TIME=0 0 * * *

ENABLE_BUDGET_ENFORCEMENT=true
ENABLE_KEYWORD_DEDUP=true
ENABLE_JSON_CACHE=true
EOF

echo "✅ .env.example created"

# Step 5: Create .gitignore additions
echo ""
echo "🔐 Step 5/6: Creating .gitignore..."

cat > "$PROJECT_NAME/.gitignore" << 'EOF'
# Environment
.env
.env.local
.env.*.local

# Dependencies
node_modules/
venv/
__pycache__/

# Build outputs
dist/
build/
*.js
*.js.map

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
logs/
*.log
npm-debug.log*

# Testing
coverage/
.nyc_output/

# OS
.DS_Store
Thumbs.db

# Project specific
data/*.backup
output/
temp/
EOF

echo "✅ .gitignore created"

# Step 6: Create README setup guide
echo ""
echo "📖 Step 6/6: Creating setup documentation..."

cat > "$PROJECT_NAME/SETUP_GUIDE.md" << 'EOF'
# 🚀 Setup Guide

## Quick Start

1. **Environment Setup:**
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

2. **Install Dependencies:**
   ```bash
   npm install
   ```

3. **Run Setup Script:**
   ```bash
   npm run setup
   ```

4. **Start Development:**
   ```bash
   npm run dev
   ```

## Reference Files

See SETUP_CLONE_AND_RUN.md for all reference files and documentation.

## Project Structure

```
src/
├── services/          # Business logic (usageTracker, keywordDedup, jsonDatabase)
├── controllers/       # API handlers (searchController, adminScraperController)
├── routes/           # Route definitions
├── jobs/             # Scheduled jobs (scraperScheduler, cleanupJob)
├── pages/            # React pages (user & admin)
└── components/       # React components

data/
├── jobs.json         # Cached job listings
├── keywords.json     # Keyword tracking
├── usage.json        # API budget tracking
└── scraping-logs.json # Audit logs
```

## Read Documentation

1. Start: `prompt.md`
2. Master guide: `README_INDEX.md`
3. Timeline: `README_DEVELOPMENT_PLAN.md`
4. Implementation: `REQUIRED_CHANGES_SUMMARY.md`

## Next Steps

Follow the 5 phases in `prompt.md`
EOF

echo "✅ Setup documentation created"

# Create completion summary
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ SETUP COMPLETE!                          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📍 Location: $PROJECT_NAME"
echo ""
echo "📋 Created:"
echo "   ✅ Directory structure"
echo "   ✅ JSON data files (jobs, keywords, usage, logs)"
echo "   ✅ .env configuration"
echo "   ✅ .env.example template"
echo "   ✅ .gitignore"
echo "   ✅ Setup documentation"
echo ""
echo "📚 Reference Files Available:"
echo "   • prompt.md - AI agent implementation guide"
echo "   • README_INDEX.md - Master navigation"
echo "   • README_DEVELOPMENT_PLAN.md - Full timeline"
echo "   • NEW_SERVICES_*.ts - Service templates"
echo "   • JSON_DATABASE_SCHEMA.ts - TypeScript types"
echo ""
echo "🚀 Next Steps:"
echo "   1. cd $PROJECT_NAME"
echo "   2. code prompt.md                    # Read implementation guide"
echo "   3. code README_DEVELOPMENT_PLAN.md   # Read timeline"
echo "   4. Follow Phase 1 in prompt.md"
echo ""
echo "📖 To view all documentation:"
echo "   code *.md *.ts"
echo ""
echo "💡 Quick Commands:"
echo "   • setup-dirs       # Create directories"
echo "   • setup-env        # Create .env"
echo "   • view-all-refs    # Open all reference files"
echo ""
echo "✨ Ready to start development!"
echo ""
