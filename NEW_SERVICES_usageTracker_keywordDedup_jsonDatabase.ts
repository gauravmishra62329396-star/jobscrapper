/**
 * ============================================
 * NEW SERVICE 1: usageTracker.ts
 * ============================================
 * 
 * File: backend/services/usageTracker.ts
 * 
 * Purpose: Enforce 200 request/month limit
 * - Track every API call
 * - Block at 180 requests (hard stop)
 * - Warn at 160 requests (80%)
 * - Auto-reset on month boundary
 */

import * as fs from 'fs/promises'
import * as path from 'path'
import { Logger } from '../utils/logger'

const logger = new Logger('UsageTracker')

interface UsageData {
  current_month: {
    month: string // "2025-01"
    total_requests: number
    remaining_requests: number
    max_requests: number // 200
    warning_triggered: boolean
    hard_limit_triggered: boolean
    requests_by_date: { [date: string]: number }
    requests_by_keyword: { [keyword: string]: number }
  }
  previous_months: any[]
}

class UsageTracker {
  private usageFile: string = './data/usage.json'
  private usageData: UsageData | null = null
  private isDirty = false

  /**
   * Initialize usage tracker
   */
  async initialize() {
    try {
      await this.load()
      await this.checkMonthBoundary()
      logger.info('✅ Usage tracker initialized')
    } catch (error) {
      logger.error(`Error initializing usage tracker: ${error}`)
      throw error
    }
  }

  /**
   * Load usage data from JSON file
   */
  private async load() {
    try {
      const data = await fs.readFile(this.usageFile, 'utf-8')
      this.usageData = JSON.parse(data)
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        // File doesn't exist, create new
        this.createNew()
      } else {
        throw error
      }
    }
  }

  /**
   * Create new usage file
   */
  private createNew() {
    const now = new Date()
    const month = now.toISOString().substring(0, 7) // "2025-01"

    this.usageData = {
      current_month: {
        month,
        total_requests: 0,
        remaining_requests: 200,
        max_requests: 200,
        warning_triggered: false,
        hard_limit_triggered: false,
        requests_by_date: {},
        requests_by_keyword: {}
      },
      previous_months: []
    }
    this.isDirty = true
  }

  /**
   * Check if month boundary crossed, reset if needed
   */
  private async checkMonthBoundary() {
    if (!this.usageData) return

    const currentMonth = new Date().toISOString().substring(0, 7)
    const dataMonth = this.usageData.current_month.month

    if (currentMonth !== dataMonth) {
      logger.info(`📅 Month changed from ${dataMonth} to ${currentMonth}`)
      logger.info('🔄 Resetting monthly usage counter')

      // Archive previous month
      this.usageData.previous_months.push(this.usageData.current_month)

      // Create new month
      this.usageData.current_month = {
        month: currentMonth,
        total_requests: 0,
        remaining_requests: 200,
        max_requests: 200,
        warning_triggered: false,
        hard_limit_triggered: false,
        requests_by_date: {},
        requests_by_keyword: {}
      }
      this.isDirty = true
      await this.save()
    }
  }

  /**
   * Check if API call is allowed
   * Returns: { allowed: boolean, reason?: string, used: number }
   */
  canMakeRequest(): {
    allowed: boolean
    used: number
    remaining: number
    reason?: string
  } {
    if (!this.usageData) {
      return { allowed: false, used: 0, remaining: 0, reason: 'Usage data not loaded' }
    }

    const used = this.usageData.current_month.total_requests
    const remaining = 200 - used

    // Hard stop at 180
    if (used >= 180) {
      return {
        allowed: false,
        used,
        remaining,
        reason: `Hard limit reached (${used}/200). API calls blocked.`
      }
    }

    // Allow
    return { allowed: true, used, remaining }
  }

  /**
   * Increment usage after successful API call
   */
  async increment(keyword?: string): Promise<void> {
    if (!this.usageData) return

    const today = new Date().toISOString().split('T')[0] // "2025-01-17"

    // Increment total
    this.usageData.current_month.total_requests++
    this.usageData.current_month.remaining_requests = 200 - this.usageData.current_month.total_requests

    // Track by date
    if (!this.usageData.current_month.requests_by_date[today]) {
      this.usageData.current_month.requests_by_date[today] = 0
    }
    this.usageData.current_month.requests_by_date[today]++

    // Track by keyword
    if (keyword) {
      if (!this.usageData.current_month.requests_by_keyword[keyword]) {
        this.usageData.current_month.requests_by_keyword[keyword] = 0
      }
      this.usageData.current_month.requests_by_keyword[keyword]++
    }

    // Check for warnings
    const used = this.usageData.current_month.total_requests
    if (used === 160 && !this.usageData.current_month.warning_triggered) {
      logger.warn('⚠️ WARNING: API usage at 80% (160/200)')
      this.usageData.current_month.warning_triggered = true
    }

    if (used >= 180 && !this.usageData.current_month.hard_limit_triggered) {
      logger.error('🚨 CRITICAL: API usage at 90% (180/200) - Hard stop activated')
      this.usageData.current_month.hard_limit_triggered = true
    }

    this.isDirty = true
    await this.save()
  }

  /**
   * Get usage statistics
   */
  getUsageStats() {
    if (!this.usageData) {
      return {
        used: 0,
        remaining: 200,
        month: 'unknown'
      }
    }

    return {
      used: this.usageData.current_month.total_requests,
      remaining: this.usageData.current_month.remaining_requests,
      month: this.usageData.current_month.month,
      percentUsed: (this.usageData.current_month.total_requests / 200) * 100,
      warnings: {
        at80Percent: this.usageData.current_month.warning_triggered,
        at90Percent: this.usageData.current_month.hard_limit_triggered
      },
      byDate: this.usageData.current_month.requests_by_date,
      byKeyword: this.usageData.current_month.requests_by_keyword,
      current_month: this.usageData.current_month,
      previous_month: this.usageData.previous_months[this.usageData.previous_months.length - 1]
    }
  }

  /**
   * Get remaining budget
   */
  getRemainingBudget(): number {
    if (!this.usageData) return 200
    return this.usageData.current_month.remaining_requests
  }

  /**
   * Save usage data to JSON file (atomic)
   */
  private async save() {
    if (!this.isDirty || !this.usageData) return

    try {
      const tempFile = this.usageFile + '.tmp'

      // Write to temp file
      await fs.writeFile(tempFile, JSON.stringify(this.usageData, null, 2))

      // Atomic rename
      await fs.rename(tempFile, this.usageFile)

      this.isDirty = false
      logger.debug('✅ Usage data saved')
    } catch (error) {
      logger.error(`Error saving usage data: ${error}`)
      throw error
    }
  }

  /**
   * Force save (for shutdown)
   */
  async flush() {
    await this.save()
  }
}

// Singleton instance
let trackerInstance: UsageTracker | null = null

export async function getUsageTracker(): Promise<UsageTracker> {
  if (!trackerInstance) {
    trackerInstance = new UsageTracker()
    await trackerInstance.initialize()
  }
  return trackerInstance
}

export { UsageTracker }

// ============================================
// NEW SERVICE 2: keywordDedup.ts
// ============================================

/**
 * File: backend/services/keywordDedup.ts
 * 
 * Purpose: Prevent re-fetching same keywords
 * - Track keyword fetch timestamps
 * - Check if keyword recently fetched
 * - Update refresh dates
 * - Manage keyword lifecycle
 */

interface KeywordRecord {
  keyword: string
  keyword_normalized: string
  fetched_at: string // ISO timestamp
  next_refresh_date: string // ISO timestamp (7 days later)
  jobs_returned: number
  request_count: number
  status: string // "active" | "paused"
}

interface KeywordsData {
  keywords: KeywordRecord[]
  metadata: {
    total_keywords: number
    active_keywords: number
    last_updated: string
  }
}

class KeywordDedup {
  private keywordsFile: string = './data/keywords.json'
  private keywordsData: KeywordsData | null = null
  private isDirty = false

  /**
   * Initialize keyword tracker
   */
  async initialize() {
    try {
      await this.load()
      logger.info('✅ Keyword deduplication initialized')
    } catch (error) {
      logger.error(`Error initializing keyword dedup: ${error}`)
      throw error
    }
  }

  /**
   * Load keywords from JSON file
   */
  private async load() {
    try {
      const data = await fs.readFile(this.keywordsFile, 'utf-8')
      this.keywordsData = JSON.parse(data)
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        this.keywordsData = {
          keywords: [],
          metadata: {
            total_keywords: 0,
            active_keywords: 0,
            last_updated: new Date().toISOString()
          }
        }
      } else {
        throw error
      }
    }
  }

  /**
   * Normalize keyword for comparison
   */
  private normalize(keyword: string): string {
    return keyword.toLowerCase().trim().replace(/\s+/g, '-')
  }

  /**
   * Check if keyword was recently fetched (within 7 days)
   */
  isDuplicate(keyword: string): boolean {
    if (!this.keywordsData) return false

    const normalized = this.normalize(keyword)
    const now = new Date()

    for (const record of this.keywordsData.keywords) {
      if (record.keyword_normalized === normalized) {
        const nextRefresh = new Date(record.next_refresh_date)
        // If today < nextRefreshDate, it's still fresh
        return now < nextRefresh
      }
    }

    return false // Not found = not duplicate
  }

  /**
   * Mark keyword as fetched
   */
  async markAsFetched(keyword: string, jobsReturned: number): Promise<void> {
    if (!this.keywordsData) return

    const normalized = this.normalize(keyword)
    const now = new Date()
    const nextRefresh = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000) // 7 days later

    // Find existing record
    const existing = this.keywordsData.keywords.find(k => k.keyword_normalized === normalized)

    if (existing) {
      // Update
      existing.fetched_at = now.toISOString()
      existing.next_refresh_date = nextRefresh.toISOString()
      existing.jobs_returned = jobsReturned
      existing.request_count++
    } else {
      // Create new
      this.keywordsData.keywords.push({
        keyword,
        keyword_normalized: normalized,
        fetched_at: now.toISOString(),
        next_refresh_date: nextRefresh.toISOString(),
        jobs_returned: jobsReturned,
        request_count: 1,
        status: 'active'
      })
    }

    // Update metadata
    this.keywordsData.metadata.total_keywords = this.keywordsData.keywords.length
    this.keywordsData.metadata.active_keywords = this.keywordsData.keywords.filter(
      k => k.status === 'active'
    ).length
    this.keywordsData.metadata.last_updated = now.toISOString()

    this.isDirty = true
    await this.save()
  }

  /**
   * Get all keywords
   */
  async getAllKeywords(): Promise<KeywordRecord[]> {
    if (!this.keywordsData) return []
    return this.keywordsData.keywords
  }

  /**
   * Get keywords that need refresh (> 7 days old)
   */
  async getStaleKeywords(): Promise<KeywordRecord[]> {
    if (!this.keywordsData) return []

    const now = new Date()
    return this.keywordsData.keywords.filter(k => {
      const nextRefresh = new Date(k.next_refresh_date)
      return now >= nextRefresh && k.status === 'active'
    })
  }

  /**
   * Get active keyword count
   */
  async getActiveKeywordCount(): Promise<number> {
    if (!this.keywordsData) return 0
    return this.keywordsData.keywords.filter(k => k.status === 'active').length
  }

  /**
   * Get keyword statistics
   */
  async getKeywordStats() {
    if (!this.keywordsData) return {}

    return {
      total: this.keywordsData.keywords.length,
      active: this.keywordsData.keywords.filter(k => k.status === 'active').length,
      stale: (await this.getStaleKeywords()).length,
      totalJobsFetched: this.keywordsData.keywords.reduce((sum, k) => sum + k.jobs_returned, 0)
    }
  }

  /**
   * Save keywords to JSON file (atomic)
   */
  private async save() {
    if (!this.isDirty || !this.keywordsData) return

    try {
      const tempFile = this.keywordsFile + '.tmp'
      await fs.writeFile(tempFile, JSON.stringify(this.keywordsData, null, 2))
      await fs.rename(tempFile, this.keywordsFile)
      this.isDirty = false
    } catch (error) {
      logger.error(`Error saving keywords: ${error}`)
      throw error
    }
  }
}

let dedupInstance: KeywordDedup | null = null

export async function getKeywordDedup(): Promise<KeywordDedup> {
  if (!dedupInstance) {
    dedupInstance = new KeywordDedup()
    await dedupInstance.initialize()
  }
  return dedupInstance
}

export { KeywordDedup }

// ============================================
// NEW SERVICE 3: jsonDatabase.ts
// ============================================

/**
 * File: backend/services/jsonDatabase.ts
 * 
 * Purpose: Atomic read/write of job cache
 * - Load jobs on startup
 * - Append new jobs atomically
 * - Index for fast searching
 * - Backup operations
 */

interface CachedJob {
  id: string
  title: string
  company: string
  location: string
  country: string
  skills: string[]
  salary_min: number | null
  salary_max: number | null
  apply_url: string
  source: string
  keyword: string
  fetched_at: string
  dedup_key: string
}

class JsonDatabase {
  private jobsFile: string = './data/jobs.json'
  private jobs: CachedJob[] = []
  private indexes = {
    bySkill: {} as { [key: string]: string[] },
    byCompany: {} as { [key: string]: string[] },
    byLocation: {} as { [key: string]: string[] }
  }
  private isDirty = false

  /**
   * Initialize database
   */
  async initialize() {
    try {
      await this.load()
      await this.buildIndexes()
      logger.info(`✅ JSON database initialized with ${this.jobs.length} jobs`)
    } catch (error) {
      logger.error(`Error initializing JSON database: ${error}`)
      throw error
    }
  }

  /**
   * Load jobs from JSON file
   */
  private async load() {
    try {
      const data = await fs.readFile(this.jobsFile, 'utf-8')
      const parsed = JSON.parse(data)
      this.jobs = parsed.jobs || []
    } catch (error: any) {
      if (error.code === 'ENOENT') {
        this.jobs = []
      } else {
        throw error
      }
    }
  }

  /**
   * Build in-memory indexes for fast searching
   */
  private async buildIndexes() {
    this.indexes = {
      bySkill: {},
      byCompany: {},
      byLocation: {}
    }

    for (const job of this.jobs) {
      // Index by company
      if (!this.indexes.byCompany[job.company]) {
        this.indexes.byCompany[job.company] = []
      }
      this.indexes.byCompany[job.company].push(job.id)

      // Index by location
      if (!this.indexes.byLocation[job.location]) {
        this.indexes.byLocation[job.location] = []
      }
      this.indexes.byLocation[job.location].push(job.id)

      // Index by skills
      for (const skill of job.skills) {
        const skillLower = skill.toLowerCase()
        if (!this.indexes.bySkill[skillLower]) {
          this.indexes.bySkill[skillLower] = []
        }
        this.indexes.bySkill[skillLower].push(job.id)
      }
    }

    logger.info(`✅ Indexes built (${Object.keys(this.indexes.bySkill).length} skills)`)
  }

  /**
   * Search jobs in-memory (instant, <100ms)
   */
  search(query: string, filters?: any): CachedJob[] {
    const queryLower = query.toLowerCase()
    let results = this.jobs.filter(job =>
      job.title.toLowerCase().includes(queryLower) ||
      job.description?.toLowerCase().includes(queryLower) ||
      job.skills.some(s => s.toLowerCase().includes(queryLower))
    )

    // Apply filters
    if (filters) {
      if (filters.minSalary) {
        results = results.filter(j => j.salary_max === null || j.salary_max >= filters.minSalary)
      }
      if (filters.maxSalary) {
        results = results.filter(j => j.salary_min === null || j.salary_min <= filters.maxSalary)
      }
      if (filters.location) {
        results = results.filter(j =>
          j.location.toLowerCase().includes(filters.location.toLowerCase())
        )
      }
      if (filters.skills) {
        results = results.filter(j =>
          filters.skills.some(s => j.skills.some(jS => jS.toLowerCase() === s.toLowerCase()))
        )
      }
    }

    return results.slice(0, 50) // Return first 50
  }

  /**
   * Append jobs atomically
   */
  async appendJobs(newJobs: CachedJob[]): Promise<void> {
    // Add new jobs
    for (const job of newJobs) {
      // Check if already exists
      if (!this.jobs.some(j => j.dedup_key === job.dedup_key)) {
        this.jobs.push(job)
      }
    }

    // Rebuild indexes
    await this.buildIndexes()

    this.isDirty = true
    await this.save()
  }

  /**
   * Check if job exists
   */
  jobExists(dedupKey: string): boolean {
    return this.jobs.some(j => j.dedup_key === dedupKey)
  }

  /**
   * Get total job count
   */
  getTotalJobs(): number {
    return this.jobs.length
  }

  /**
   * Get last refresh date
   */
  getLastRefresh(): string {
    if (this.jobs.length === 0) return 'Never'
    const sorted = [...this.jobs].sort((a, b) => 
      new Date(b.fetched_at).getTime() - new Date(a.fetched_at).getTime()
    )
    return sorted[0].fetched_at
  }

  /**
   * Save to JSON file (atomic)
   */
  private async save() {
    if (!this.isDirty) return

    try {
      const tempFile = this.jobsFile + '.tmp'

      const data = {
        jobs: this.jobs,
        metadata: {
          total_jobs: this.jobs.length,
          last_updated: new Date().toISOString()
        }
      }

      await fs.writeFile(tempFile, JSON.stringify(data, null, 2))
      await fs.rename(tempFile, this.jobsFile)

      this.isDirty = false
      logger.debug(`✅ Saved ${this.jobs.length} jobs to JSON`)
    } catch (error) {
      logger.error(`Error saving jobs: ${error}`)
      throw error
    }
  }
}

let dbInstance: JsonDatabase | null = null

export async function getJsonDatabase(): Promise<JsonDatabase> {
  if (!dbInstance) {
    dbInstance = new JsonDatabase()
    await dbInstance.initialize()
  }
  return dbInstance
}

export { JsonDatabase }
