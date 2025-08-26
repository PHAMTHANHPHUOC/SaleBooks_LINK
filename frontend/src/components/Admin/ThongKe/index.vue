<template>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <h1>Thống kê lượt truy cập</h1>
      <div class="visitor-info" v-if="currentVisitor.country">
        <span class="visitor-flag">{{ getCountryFlag(currentVisitor.country) }}</span>
        <span class="visitor-text">Bạn đang truy cập từ: {{ currentVisitor.country_name || currentVisitor.country }}</span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>⏳ Đang tải thống kê...</p>
    </div>

    <!-- Main Stats -->
    <div v-show="!loading" class="stats-grid">
      <div class="stat-card">
        <h3>👥 Tổng lượt truy cập</h3>
        <div class="stat-number">{{ stats.total_visits || 0 }}</div>
        <div class="stat-label">Tất cả thời gian</div>
      </div>
      <div class="stat-card">
        <h3>📅 Hôm nay</h3>
        <div class="stat-number">{{ stats.today_visits || 0 }}</div>
        <div class="stat-label">Lượt truy cập</div>
      </div>
      <div class="stat-card">
        <h3>📊 Tuần này</h3>
        <div class="stat-number">{{ stats.week_visits || 0 }}</div>
        <div class="stat-label">Lượt truy cập</div>
      </div>
      <div class="stat-card">
        <h3>📈 Tháng này</h3>
        <div class="stat-number">{{ stats.month_visits || 0 }}</div>
        <div class="stat-label">Lượt truy cập</div>
      </div>
      <div class="stat-card">
        <h3>👤 Người dùng duy nhất</h3>
        <div class="stat-number">{{ stats.unique_today || 0 }}</div>
        <div class="stat-label">Hôm nay</div>
      </div>
      <div class="stat-card">
        <h3>🌍 Quốc gia</h3>
        <div class="stat-number">{{ totalCountries }}</div>
        <div class="stat-label">Đã truy cập</div>
      </div>
      <div class="stat-card">
        <h3>⏰ Cập nhật lần cuối</h3>
        <div class="stat-number" style="font-size: 1.2em;">{{ lastUpdateTime }}</div>
        <div class="stat-label">Thời gian</div>
      </div>
    </div>

    <!-- Country Statistics Section -->
    <div v-show="!loading" class="country-section">
      <div class="country-stats-card">
        <h3>🌍 Thống kê theo quốc gia</h3>
        <div class="country-tabs">
          <button 
            :class="['tab-button', { active: activeTab === 'today' }]" 
            @click="activeTab = 'today'"
          >
            Hôm nay ({{ getTotalVisitsForPeriod('today') }})
          </button>
          <button 
            :class="['tab-button', { active: activeTab === 'week' }]" 
            @click="activeTab = 'week'"
          >
            Tuần này ({{ getTotalVisitsForPeriod('week') }})
          </button>
          <button 
            :class="['tab-button', { active: activeTab === 'month' }]" 
            @click="activeTab = 'month'"
          >
            Tháng này ({{ getTotalVisitsForPeriod('month') }})
          </button>
          <button 
            :class="['tab-button', { active: activeTab === 'all' }]" 
            @click="activeTab = 'all'"
          >
            Tất cả ({{ getTotalVisitsForPeriod('all') }})
          </button>
        </div>
        
        <div class="country-list">
          <div 
            v-for="country in getCurrentCountryData" 
            :key="country.country_code"
            class="country-item"
            :class="{ 'current-visitor': country.country_code === currentVisitor.country }"
          >
            <div class="country-flag">
              {{ getCountryFlag(country.country_code) }}
            </div>
            <div class="country-info">
              <span class="country-name">{{ country.country_name }}</span>
              <span class="country-code">({{ country.country_code }})</span>
              <span v-if="country.country_code === currentVisitor.country" class="current-badge">Bạn ở đây</span>
            </div>
            <div class="country-stats">
              <span class="visit-count">{{ country.visits }} lượt</span>
              <div class="progress-bar">
                <div 
                  class="progress-fill" 
                  :style="{ width: getProgressWidth(country.visits) + '%' }"
                ></div>
              </div>
              <span class="percentage">{{ getPercentage(country.visits) }}%</span>
            </div>
          </div>
          
          <div v-if="getCurrentCountryData.length === 0" class="no-data">
            <p>📊 Chưa có dữ liệu truy cập cho khoảng thời gian này</p>
          </div>
        </div>

        <!-- Country Chart -->
        <div class="chart-container" style="margin-top: 30px;" v-if="getCurrentCountryData.length > 0">
          <canvas ref="countryChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Charts Section -->
    <div v-show="!loading" class="charts-section">
      <div class="chart-card">
        <h3>📊 Thống kê theo giờ (24h qua)</h3>
        <div class="chart-container">
          <canvas ref="hourlyChart"></canvas>
        </div>
      </div>
      <div class="chart-card">
        <h3>📈 Thống kê theo ngày (7 ngày qua)</h3>
        <div class="chart-container">
          <canvas ref="dailyChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Additional Stats -->
    <div v-show="!loading" class="additional-stats">
      <div class="additional-stat-card">
        <h4>📊 Tăng trưởng</h4>
        <p>Hôm nay vs hôm qua: <span :class="getGrowthClass(growth.today_vs_yesterday)">{{ formatGrowth(growth.today_vs_yesterday) }}</span></p>
        <p>Tuần này vs tuần trước: <span :class="getGrowthClass(growth.this_week_vs_last_week)">{{ formatGrowth(growth.this_week_vs_last_week) }}</span></p>
        <p>Tháng này vs tháng trước: <span :class="getGrowthClass(growth.this_month_vs_last_month)">{{ formatGrowth(growth.this_month_vs_last_month) }}</span></p>
      </div>
      <div class="additional-stat-card">
        <h4>🏆 Top quốc gia hôm nay</h4>
        <div v-for="country in topCountriesToday.slice(0, 3)" :key="country.country_code" class="top-country">
          <span>{{ getCountryFlag(country.country_code) }} {{ country.country_name }}</span>
          <strong>{{ country.visits }} lượt</strong>
        </div>
        <div v-if="topCountriesToday.length === 0" class="no-top-countries">
          <p>📊 Chưa có dữ liệu hôm nay</p>
        </div>
      </div>
      <div class="additional-stat-card">
        <h4>⏱️ Thông tin hệ thống</h4>
        <p>Múi giờ: <strong>{{ stats.timezone || 'UTC+7' }}</strong></p>
        <p>Thời gian server: <strong>{{ serverTime }}</strong></p>
        <p>Trang hiện tại: <strong>{{ stats.page_name || 'homepage' }}</strong></p>
        <p>IP của bạn: <strong>{{ currentVisitor.ip || 'Đang lấy...' }}</strong></p>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'
import baseRequest from '../../../../src/core/baseRequest';

export default {
  name: 'ColoringBookDashboard',
  data() {
    return {
      loading: true,
      stats: {},
      growth: {},
      countryStats: {
        today: [],
        week: [],
        month: [],
        all: []
      },
      currentVisitor: {
        ip: null,
        country: null,
        country_code: null,
        country_name: null
      },
      activeTab: 'today',
      hourlyChart: null,
      dailyChart: null,
      countryChart: null,
      refreshInterval: null,
      mockMode: false
    }
  },
  computed: {
    lastUpdateTime() {
      if (this.stats.last_update) {
        const date = new Date(this.stats.last_update)
        return date.toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'})
      }
      return new Date().toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'})
    },
    serverTime() {
      if (this.stats.server_time) {
        const serverTime = new Date(this.stats.server_time)
        return serverTime.toLocaleString('vi-VN')
      }
      return new Date().toLocaleString('vi-VN')
    },
    totalCountries() {
      return this.countryStats.all?.length || 0
    },
    getCurrentCountryData() {
      const data = this.countryStats[this.activeTab] || []
      return data.sort((a, b) => b.visits - a.visits)
    },
    topCountriesToday() {
      return [...(this.countryStats.today || [])].sort((a, b) => b.visits - a.visits)
    }
  },
  watch: {
    activeTab() {
      this.$nextTick(() => {
        this.createCountryChart()
      })
    }
  },
  mounted() {
    this.initializeTracking()
  },
  beforeUnmount() {
    this.stopAutoRefresh()
    this.destroyCharts()
  },
  methods: {
   
    async initializeTracking() {
      try {
        // Dev mock via query string (does not call backend)

        // Bước 1: Lấy thông tin visitor và ghi nhận lượt truy cập
        await this.detectAndTrackVisitor()
        
        // Bước 2: Lấy thống kê
        await this.fetchVisitStats()
        
        // Bước 3: Tự động refresh
        this.startAutoRefresh()
      } catch (error) {
        console.error('Error initializing tracking:', error)
        this.showFallbackData()
      }
    },

    async detectAndTrackVisitor() {
      try {
        // ✅ Gọi API Django để lấy IP + location (không hardcode IP)
        const response = await baseRequest.get("location/")

        const geoData = response.data
        this.currentVisitor = {
          ip: geoData.ip,
          country: geoData.country_code || "VN",
          country_code: geoData.country_code || "VN",
          country_name: geoData.country || geoData.country_name || "Vietnam",
          city: geoData.city,
          region: geoData.region
        }

        // ❌ Không gửi tracking từ trang quản trị để tránh tăng lượt khi F5

      } catch (error) {
        console.error("Error detecting visitor location:", error)
      }
    },
    async trackVisit(visitorData) {
      try {
        const trackingData = {
          ...visitorData,
          page: 'home',
          timestamp: new Date().toISOString(),
          user_agent: navigator.userAgent,
          referrer: document.referrer,
          screen_resolution: `${screen.width}x${screen.height}`,
          language: navigator.language
        }

        // Gửi data tracking về API
        await baseRequest.post('api/visits/track/', trackingData)
        
      } catch (error) {
        console.error('Error tracking visit:', error)
        // Không throw error để không block việc hiển thị dashboard
      }
    },

    async fetchVisitStats() {
      try {
        const response = await baseRequest.get("api/visits/?page=home&include_countries=true")
        const data = response.data
        
        this.stats = data
        this.growth = data.growth || {}
        this.countryStats = data.country_stats || { today: [], week: [], month: [], all: [] }
        this.loading = false
        
        this.$nextTick(() => {
          this.createHourlyChart(data.hourly_stats || [])
          this.createDailyChart(data.daily_stats || [])
          this.createCountryChart()
        })
        
      } catch (error) {
        console.error('Error fetching stats:', error)
        this.showFallbackData()
      }
    },

    getTotalVisitsForPeriod(period) {
      const data = this.countryStats[period] || []
      return data.reduce((sum, country) => sum + country.visits, 0)
    },

    createHourlyChart(hourlyData) {
      if (this.hourlyChart) {
        this.hourlyChart.destroy()
      }
      
      const ctx = this.$refs.hourlyChart?.getContext('2d')
      if (!ctx) return
      
      const labels = hourlyData.map(item => item.hour)
      const data = hourlyData.map(item => item.visits)
      
      this.hourlyChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: 'Lượt truy cập',
            data: data,
            borderColor: '#4ecdc4',
            backgroundColor: 'rgba(78, 205, 196, 0.1)',
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
    },

    createDailyChart(dailyData) {
      if (this.dailyChart) {
        this.dailyChart.destroy()
      }
      
      const ctx = this.$refs.dailyChart?.getContext('2d')
      if (!ctx) return
      
      const labels = dailyData.map(item => item.date)
      const data = dailyData.map(item => item.visits)
      
      this.dailyChart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: labels,
          datasets: [{
            label: 'Lượt truy cập',
            data: data,
            backgroundColor: 'rgba(255, 107, 107, 0.8)',
            borderColor: '#ff6b6b',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                stepSize: 1
              }
            }
          }
        }
      })
    },

    createCountryChart() {
      if (this.countryChart) {
        this.countryChart.destroy()
      }
      
      const ctx = this.$refs.countryChart?.getContext('2d')
      if (!ctx) return
      
      const currentData = this.getCurrentCountryData.slice(0, 10)
      if (currentData.length === 0) return
      
      const labels = currentData.map(item => item.country_name)
      const data = currentData.map(item => item.visits)
      
      const colors = [
        '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#f0932b',
        '#eb4d4b', '#6c5ce7', '#a29bfe', '#fd79a8', '#00b894'
      ]
      
      this.countryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors.slice(0, data.length),
            borderWidth: 2,
            borderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'bottom',
              labels: {
                usePointStyle: true,
                padding: 20
              }
            }
          }
        }
      })
    },

    getCountryFlag(countryCode) {
      const flags = {
        'VN': '🇻🇳', 'US': '🇺🇸', 'JP': '🇯🇵', 'KR': '🇰🇷', 'CN': '🇨🇳',
        'TH': '🇹🇭', 'SG': '🇸🇬', 'MY': '🇲🇾', 'ID': '🇮🇩', 'PH': '🇵🇭',
        'IN': '🇮🇳', 'AU': '🇦🇺', 'GB': '🇬🇧', 'DE': '🇩🇪', 'FR': '🇫🇷',
        'IT': '🇮🇹', 'ES': '🇪🇸', 'BR': '🇧🇷', 'CA': '🇨🇦', 'RU': '🇷🇺',
        'Unknown': '🌐'
      }
      return flags[countryCode] || '🌐'
    },

    getProgressWidth(visits) {
      const maxVisits = Math.max(...this.getCurrentCountryData.map(c => c.visits))
      return maxVisits > 0 ? (visits / maxVisits) * 100 : 0
    },

    getPercentage(visits) {
      const totalVisits = this.getCurrentCountryData.reduce((sum, c) => sum + c.visits, 0)
      return totalVisits > 0 ? Math.round((visits / totalVisits) * 100) : 0
    },

    getGrowthClass(value) {
      const baseClass = 'growth-indicator'
      if (value > 0) return `${baseClass} growth-positive`
      if (value < 0) return `${baseClass} growth-negative`
      return `${baseClass} growth-neutral`
    },

    formatGrowth(value) {
      const num = value || 0
      return `${num > 0 ? '+' : ''}${num}%`
    },

    showFallbackData() {
      // Hiển thị dữ liệu cơ bản khi không có API hoặc lỗi
      this.stats = {
        total_visits: 0,
        today_visits: 0,
        week_visits: 0,
        month_visits: 0,
        unique_today: 0,
        last_update: new Date().toISOString(),
        timezone: "UTC+7",
        server_time: new Date().toISOString(),
        page_name: "homepage"
      }
      
      this.growth = {
        today_vs_yesterday: 0,
        this_week_vs_last_week: 0,
        this_month_vs_last_month: 0
      }
      
      this.countryStats = { today: [], week: [], month: [], all: [] }
      this.loading = false
      
      this.$nextTick(() => {
        this.createHourlyChart([])
        this.createDailyChart([])
        this.createCountryChart()
      })
    },

    startAutoRefresh() {
      this.refreshInterval = setInterval(() => {
        this.fetchVisitStats() // Chỉ refresh stats, không track lại
      }, 5 * 60 * 1000) // 5 phút
    },

    stopAutoRefresh() {
      if (this.refreshInterval) {
        clearInterval(this.refreshInterval)
        this.refreshInterval = null
      }
    },

    destroyCharts() {
      if (this.hourlyChart) {
        this.hourlyChart.destroy()
        this.hourlyChart = null
      }
      if (this.dailyChart) {
        this.dailyChart.destroy()
        this.dailyChart = null
      }
      if (this.countryChart) {
        this.countryChart.destroy()
        this.countryChart = null
      }
    }
  }
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
  background: rgba(255, 255, 255, 0.95);
  padding: 30px;
  border-radius: 20px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.header h1 {
  font-size: 3em;
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 10px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.15);
}

.stat-card h3 {
  font-size: 1.5em;
  margin-bottom: 15px;
  color: #333;
}

.stat-number {
  font-size: 3em;
  font-weight: bold;
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 1.1em;
  color: #666;
  margin-top: 10px;
}

/* Country Statistics Styles */
.country-section {
  margin-bottom: 40px;
}

.country-stats-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.country-stats-card h3 {
  text-align: center;
  margin-bottom: 25px;
  font-size: 1.5em;
  color: #333;
}

.country-tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
  gap: 10px;
  flex-wrap: wrap;
}

.tab-button {
  padding: 10px 20px;
  border: 2px solid #e0e6ed;
  background: white;
  border-radius: 25px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.tab-button:hover {
  border-color: #4ecdc4;
  color: #4ecdc4;
}

.tab-button.active {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  border-color: transparent;
  color: white;
}

.country-list {
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.country-item {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background: rgba(248, 249, 250, 0.8);
  border-radius: 15px;
  transition: transform 0.2s ease;
}

.country-item:hover {
  transform: translateX(5px);
  background: rgba(240, 242, 245, 0.9);
}

.country-flag {
  font-size: 2em;
  margin-right: 15px;
}

.country-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.country-name {
  font-weight: bold;
  color: #333;
}

.country-code {
  font-size: 0.9em;
  color: #666;
}

.country-stats {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  min-width: 120px;
}

.visit-count {
  font-weight: bold;
  color: #4ecdc4;
  margin-bottom: 5px;
}

.progress-bar {
  width: 80px;
  height: 6px;
  background: #e0e6ed;
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 2px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  border-radius: 3px;
  transition: width 0.3s ease;
}

.percentage {
  font-size: 0.8em;
  color: #666;
}

.charts-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.chart-card h3 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
  font-size: 1.3em;
}

.chart-container {
  position: relative;
  height: 300px;
}

.additional-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.additional-stat-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 20px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.additional-stat-card h4 {
  margin-bottom: 15px;
  color: #333;
  text-align: center;
}

.top-country {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #eee;
}

.top-country:last-child {
  border-bottom: none;
}

.growth-indicator {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: bold;
}

.growth-positive {
  background: #4ecdc4;
  color: white;
}

.growth-negative {
  background: #ff6b6b;
  color: white;
}

.growth-neutral {
  background: #95a5a6;
  color: white;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 1.2em;
  color: white;
}

/* Continuation from the existing styles */

@media (max-width: 768px) {
  .container {
    padding: 15px;
  }
  
  .header {
    padding: 20px;
    margin-bottom: 20px;
  }
  
  .header h1 {
    font-size: 2em;
  }
  
  .stats-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .stat-card {
    padding: 20px;
  }
  
  .stat-number {
    font-size: 2.5em;
  }
  
  .country-tabs {
    gap: 5px;
  }
  
  .tab-button {
    padding: 8px 15px;
    font-size: 0.9em;
  }
  
  .country-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .country-info {
    flex-direction: row;
    gap: 10px;
    width: 100%;
  }
  
  .country-stats {
    align-items: flex-start;
    width: 100%;
  }
  
  .charts-section {
    grid-template-columns: 1fr;
    gap: 15px;
    margin-bottom: 20px;
  }
  
  .chart-card {
    padding: 20px;
  }
  
  .chart-container {
    height: 250px;
  }
  
  .additional-stats {
    grid-template-columns: 1fr;
    gap: 15px;
  }
}

@media (max-width: 480px) {
  .header h1 {
    font-size: 1.8em;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 15px;
  }
  
  .stat-number {
    font-size: 2em;
  }
  
  .country-tabs {
    flex-direction: column;
  }
  
  .tab-button {
    width: 100%;
    text-align: center;
  }
  
  .country-flag {
    font-size: 1.5em;
    margin-right: 10px;
  }
  
  .chart-container {
    height: 200px;
  }
}

/* Scrollbar Styles */
.country-list::-webkit-scrollbar {
  width: 6px;
}

.country-list::-webkit-scrollbar-track {
  background: rgba(240, 242, 245, 0.5);
  border-radius: 3px;
}

.country-list::-webkit-scrollbar-thumb {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  border-radius: 3px;
}

.country-list::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(45deg, #ff5252, #26a69a);
}

/* Animation Classes */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* Apply animations */
.stat-card {
  animation: fadeInUp 0.6s ease-out;
}

.country-item {
  animation: slideInLeft 0.4s ease-out;
}

.loading p {
  animation: pulse 2s infinite;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  body {
    background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
  }
  
  .stat-card,
  .country-stats-card,
  .chart-card,
  .additional-stat-card {
    background: rgba(45, 55, 72, 0.95);
    color: #e2e8f0;
  }
  
  .header {
    background: rgba(45, 55, 72, 0.95);
  }
  
  .stat-card h3,
  .country-stats-card h3,
  .chart-card h3,
  .additional-stat-card h4 {
    color: #e2e8f0;
  }
  
  .stat-label {
    color: #a0aec0;
  }
  
  .country-name {
    color: #e2e8f0;
  }
  
  .country-code {
    color: #a0aec0;
  }
  
  .country-item {
    background: rgba(26, 32, 44, 0.6);
  }
  
  .country-item:hover {
    background: rgba(26, 32, 44, 0.8);
  }
  
  .tab-button {
    background: rgba(26, 32, 44, 0.8);
    border-color: #4a5568;
    color: #e2e8f0;
  }
  
  .tab-button:hover {
    border-color: #4ecdc4;
    color: #4ecdc4;
  }
  
  .progress-bar {
    background: #4a5568;
  }
  
  .percentage {
    color: #a0aec0;
  }
  
  .loading {
    color: #e2e8f0;
  }
  
  .top-country {
    border-bottom-color: #4a5568;
  }
}

/* Print Styles */
@media print {
  body {
    background: white;
    color: black;
  }
  
  .container {
    max-width: none;
    padding: 0;
  }
  
  .stat-card,
  .country-stats-card,
  .chart-card,
  .additional-stat-card {
    background: white;
    box-shadow: none;
    border: 1px solid #ddd;
    page-break-inside: avoid;
  }
  
  .charts-section {
    page-break-inside: avoid;
  }
  
  .chart-container {
    height: 200px;
  }
}

/* Focus Styles for Accessibility */
.tab-button:focus {
  outline: 2px solid #4ecdc4;
  outline-offset: 2px;
}

/* High Contrast Mode Support */
@media (prefers-contrast: high) {
  .stat-card,
  .country-stats-card,
  .chart-card,
  .additional-stat-card {
    border: 2px solid #333;
  }
  
  .tab-button {
    border-width: 3px;
  }
  
  .progress-fill {
    background: #000;
  }
}

/* Reduced Motion Support */
@media (prefers-reduced-motion: reduce) {
  .stat-card,
  .country-item,
  .tab-button,
  .progress-fill {
    transition: none;
    animation: none;
  }
  
  .stat-card:hover {
    transform: none;
  }
  
  .country-item:hover {
    transform: none;
  }
}

/* Additional Utility Classes */
.text-gradient {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.glass-effect {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.shadow-soft {
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
}

.shadow-hover {
  transition: box-shadow 0.3s ease;
}

.shadow-hover:hover {
  box-shadow: 0 25px 45px rgba(0, 0, 0, 0.15);
}

/* Loading Animation */
.loading-spinner {
  display: inline-block;
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #4ecdc4;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Error State */
.error-message {
  background: rgba(255, 107, 107, 0.1);
  border: 1px solid #ff6b6b;
  color: #ff6b6b;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  margin: 20px 0;
}

/* Success State */
.success-message {
  background: rgba(78, 205, 196, 0.1);
  border: 1px solid #4ecdc4;
  color: #4ecdc4;
  padding: 15px;
  border-radius: 10px;
  text-align: center;
  margin: 20px 0;
}
</style>
