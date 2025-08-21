<template>
  <div class="container">
    <!-- Header -->
    <div class="header">
      <h1>🎨 Coloring Book Store</h1>
      <p>Khám phá thế giới màu sắc với những cuốn sách tô màu tuyệt vời</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
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
        <h3>⏰ Cập nhật lần cuối</h3>
        <div class="stat-number" style="font-size: 1.2em;">{{ lastUpdateTime }}</div>
        <div class="stat-label">Thời gian</div>
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
        <h4>⏱️ Thông tin hệ thống</h4>
        <p>Múi giờ: <strong>{{ stats.timezone || 'UTC+7' }}</strong></p>
        <p>Thời gian server: <strong>{{ serverTime }}</strong></p>
        <p>Trang hiện tại: <strong>{{ stats.page_name || 'homepage' }}</strong></p>
      </div>
    </div>


  </div>
</template>

<script>
import axios from 'axios'
import Chart from 'chart.js/auto'

export default {
  name: 'ColoringBookDashboard',
  data() {
    return {
      loading: true,
      stats: {},
      growth: {},
      hourlyChart: null,
      dailyChart: null,
      refreshInterval: null
    }
  },
  computed: {
    lastUpdateTime() {
      if (this.stats.last_update) {
        const date = new Date(this.stats.last_update)
        return date.toLocaleTimeString('vi-VN', {hour: '2-digit', minute: '2-digit'})
      }
      return '--:--'
    },
    serverTime() {
      if (this.stats.server_time) {
        const serverTime = new Date(this.stats.server_time)
        return serverTime.toLocaleString('vi-VN')
      }
      return '--'
    }
  },
  mounted() {
    this.fetchVisitStats()
    this.startAutoRefresh()
  },
  beforeUnmount() {
    this.stopAutoRefresh()
    this.destroyCharts()
  },
  methods: {
    async fetchVisitStats() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/api/visits/?page=home")
        const data = response.data
        
        this.stats = data
        this.growth = data.growth || {}
        this.loading = false
        
        this.$nextTick(() => {
          this.createHourlyChart(data.hourly_stats || [])
          this.createDailyChart(data.daily_stats || [])
        })
        
      } catch (error) {
        console.error('Error fetching stats:', error)
        this.showSampleData()
      }
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

    showSampleData() {
      const sampleData = {
        total_visits: 1247,
        today_visits: 45,
        week_visits: 312,
        month_visits: 1089,
        unique_today: 32,
        last_update: new Date().toISOString(),
        hourly_stats: [
          {hour: "00:00", visits: 2},
          {hour: "01:00", visits: 1},
          {hour: "02:00", visits: 0},
          {hour: "03:00", visits: 1},
          {hour: "04:00", visits: 3},
          {hour: "05:00", visits: 5},
          {hour: "06:00", visits: 8},
          {hour: "07:00", visits: 12},
          {hour: "08:00", visits: 15},
          {hour: "09:00", visits: 18},
          {hour: "10:00", visits: 14},
          {hour: "11:00", visits: 11}
        ],
        daily_stats: [
          {date: "15/08", visits: 42},
          {date: "16/08", visits: 38},
          {date: "17/08", visits: 55},
          {date: "18/08", visits: 47},
          {date: "19/08", visits: 61},
          {date: "20/08", visits: 39},
          {date: "21/08", visits: 45}
        ],
        growth: {
          today_vs_yesterday: 15,
          this_week_vs_last_week: -5,
          this_month_vs_last_month: 23
        },
        timezone: "UTC+7",
        server_time: new Date().toISOString(),
        page_name: "homepage"
      }

      this.stats = sampleData
      this.growth = sampleData.growth
      this.loading = false
      
      this.$nextTick(() => {
        this.createHourlyChart(sampleData.hourly_stats)
        this.createDailyChart(sampleData.daily_stats)
      })
    },

    startAutoRefresh() {
      // Refresh data every 5 minutes
      this.refreshInterval = setInterval(() => {
        this.fetchVisitStats()
      }, 5 * 60 * 1000)
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

.header p {
  font-size: 1.2em;
  color: #666;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
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

.books-section {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  margin-bottom: 30px;
}

.books-section h2 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2em;
  color: #333;
}

.books-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

.book-card {
  background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  transition: transform 0.3s ease;
  color: white;
  text-decoration: none;
}

.book-card:hover {
  transform: translateY(-5px);
  text-decoration: none;
  color: white;
}

.book-card h3 {
  font-size: 1.3em;
  margin-bottom: 10px;
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

.footer {
  text-align: center;
  padding: 20px;
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9em;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 1.2em;
  color: white;
}

@media (max-width: 768px) {
  .container {
    padding: 10px;
  }
  
  .header h1 {
    font-size: 2em;
  }
  
  .stat-number {
    font-size: 2em;
  }
  
  .charts-section {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 250px;
  }
}
</style>