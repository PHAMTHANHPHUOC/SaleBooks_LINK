<!-- filepath: c:\SaleBooks_link_KDP\frontend\src\components\Admin\ThongKeMangXaHoi\index.vue -->
<template>
  <div class="stats-container">
    <!-- Header -->
    <div class="header">
      <h1>📊 Thống kê mạng xã hội</h1>
      <p>Theo dõi lượt click các link mạng xã hội</p>
      <div class="time-range-info" v-if="!loading">
        <span class="time-range-badge">{{ getTimeRangeInfo() }}</span>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="tabs">
      <button 
        v-for="(tab, index) in tabs" 
        :key="`tab-${index}`"
        :class="{ 'active': activeTab === tab.key }"
        @click="handleTabClick(tab.key)"
        :data-key="tab.key"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>

    <!-- Stats Overview -->
    <div class="overview" v-if="topLinks.length > 0">
      <div class="stat-box">
        <div class="stat-number">{{ topLinks.length }}</div>
        <div class="stat-label">Link mạng xã hội</div>
        <div class="stat-period">{{ getActiveTabLabel() }}</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">{{ totalClicks.toLocaleString() }}</div>
        <div class="stat-label">Tổng lượt click</div>
        <div class="stat-period">{{ getActiveTabLabel() }}</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">{{ topLink ? '🏆' : '-' }}</div>
        <div class="stat-label">{{ topLink?.name || 'Chưa có dữ liệu' }}</div>
        <div class="stat-period">{{ getActiveTabLabel() }}</div>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Đang tải dữ liệu...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error">
      <p>⚠️ {{ error }}</p>
      <button @click="retry" class="btn-retry">Thử lại</button>
    </div>

    <!-- Empty -->
    <div v-else-if="topLinks.length === 0" class="empty">
      <p>📈 Chưa có dữ liệu {{ getActiveTabLabel() }}</p>
      <p class="empty-subtitle">Dữ liệu sẽ được cập nhật khi có lượt click</p>
    </div>

    <!-- Link List -->
    <div v-else class="links">
      <div class="list-header">
        <h2>Top link mạng xã hội {{ getActiveTabLabel() }}</h2>
        <div class="view-controls">
          <button 
            :class="{ 'active': viewMode === 'grid' }"
            @click="viewMode = 'grid'"
          >▦</button>
          <button 
            :class="{ 'active': viewMode === 'list' }"
            @click="viewMode = 'list'"
          >☰</button>
        </div>
      </div>

      <!-- Grid View -->
      <div v-if="viewMode === 'grid'" class="grid">
        <div 
          v-for="(link, index) in topLinks" 
          :key="`${activeTab}-${link.id}`"
          class="link-card"
          :class="getRankClass(index)"
        >
          <div class="rank">{{ index + 1 }}</div>
          <div class="card">
            <div class="card-body">
             <h4 class="link-name">{{ link.link__name }}</h4>
              <div class="url">{{ link.url }}</div>
              <div class="clicks">
                👆 {{ link.luot_click.toLocaleString() }} lượt click
              </div>
              <div class="progress">
                <div 
                  class="progress-bar"
                  :style="{ width: getProgressWidth(link.luot_click) + '%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="list">
        <div 
          v-for="(link, index) in topLinks" 
          :key="`${activeTab}-${link.id}`"
          class="link-row"
          :class="getRankClass(index)"
        >
          <div class="rank">{{ index + 1 }}</div>
          <div class="details">
            <h4>{{ link.link__name }}</h4>
            <!-- <span class="id">ID: {{ link.id }}</span> -->
            <div class="url">{{ link.url }}</div>
          </div>
          <div class="metrics">
            <div class="metric">
              <strong>{{ link.luot_click.toLocaleString() }}</strong>
              <span>lượt click</span>
            </div>
          </div>
          <div class="trend">📈</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import baseRequest from '../../../../src/core/baseRequest';

export default {
  name: 'SocialStats',
  data() {
    return {
      topLinks: [],
      loading: false,
      error: null,
      activeTab: 'ngay',
      viewMode: 'grid',
      tabs: [
        { key: 'ngay', label: 'Hôm nay', icon: '📅' },
        { key: 'tuan', label: 'Tuần này', icon: '🗓️' }, 
        { key: 'thang', label: 'Tháng này', icon: '🗓️' },
        { key: 'nam', label: 'Năm nay', icon: '📆' }
      ]
    };
  },
  computed: {
    totalClicks() {
      return this.topLinks.reduce((sum, link) => sum + link.luot_click, 0);
    },
    topLink() {
      return this.topLinks[0] || null;
    }
  },
  methods: {
    handleTabClick(tabKey) {
      if (!tabKey) return;
      this.loadTop(tabKey);
    },
    async loadTop(loai) {
    this.topLinks = [];
    this.loading = true;
    this.error = null;
    this.activeTab = loai;
    try {
      // Gọi API thống kê theo thời gian
      let res = await baseRequest.get(`api/links/click-stats/?loai=${loai}`);
      this.topLinks = res.data.data || [];
      // Nếu không có dữ liệu, thử gọi API top tổng
      if (this.topLinks.length === 0 && loai === 'nam') {
        let resTop = await baseRequest.get(`api/links/top/`);
        this.topLinks = resTop.data.data || [];
      }
    } catch (error) {
      this.error = "Không thể tải dữ liệu. Vui lòng thử lại.";
    } finally {
      this.loading = false;
    }
  },
    getActiveTabLabel() {
      const tab = this.tabs.find(t => t.key === this.activeTab);
      return tab ? tab.label.toLowerCase() : '';
    },
    getTimeRangeInfo() {
      const today = new Date();
      switch(this.activeTab) {
        case 'ngay':
          return `Hôm nay (${today.toLocaleDateString('vi-VN')})`;
        case 'tuan':
          const startOfWeek = new Date(today);
          startOfWeek.setDate(today.getDate() - today.getDay() + 1);
          const endOfWeek = new Date(startOfWeek);
          endOfWeek.setDate(startOfWeek.getDate() + 6);
          return `Tuần này (${startOfWeek.toLocaleDateString('vi-VN')} - ${endOfWeek.toLocaleDateString('vi-VN')})`;
        case 'thang':
          return `Tháng ${today.getMonth() + 1}/${today.getFullYear()}`;
        case 'nam':
          return `Năm ${today.getFullYear()}`;
        default:
          return '';
      }
    },
    getProgressWidth(clicks) {
      if (this.topLinks.length === 0) return 0;
      const maxClicks = Math.max(...this.topLinks.map(link => link.luot_click));
      return maxClicks > 0 ? (clicks / maxClicks) * 100 : 0;
    },
    getRankClass(index) {
      if (index === 0) return 'rank-1';
      if (index === 1) return 'rank-2';
      if (index === 2) return 'rank-3';
      return '';
    },
    retry() {
      this.loadTop(this.activeTab);
    }
  },
  mounted() {
    this.loadTop("ngay");
  }
};
</script>

<style scoped>
/* Copy style từ ThongKeSanPham/index.vue và đổi tên class cho phù hợp */
.stats-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, #f8f8f8 0%, #e4e2e9 100%);
  min-height: 100vh;
  color: #1f2937;
}
.header { text-align: center; margin-bottom: 30px; }
.header h1 { font-size: 2.5rem; font-weight: bold; margin: 0 0 10px 0; }
.header p { font-size: 1.1rem; opacity: 0.9; margin: 0; }
.time-range-info { margin: 15px 0; }
.time-range-badge { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 8px 16px; border-radius: 20px; font-size: 0.9rem; font-weight: 500; box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);}
.header-actions { display: flex; gap: 15px; justify-content: center; margin-top: 20px; flex-wrap: wrap;}
.tabs { display: flex; gap: 10px; margin-bottom: 30px; background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 15px; backdrop-filter: blur(10px);}
.tabs button { flex: 1; padding: 15px; border: none; border-radius: 10px; background: transparent; color: rgb(3, 3, 3); font-weight: 500; cursor: pointer; transition: all 0.3s;}
.tabs button:hover { background: rgba(255, 255, 255, 0.1);}
.tabs button.active { background: white; color: #6366f1; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);}
.overview { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px;}
.stat-box { background: white; padding: 25px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);}
.stat-number { font-size: 2rem; font-weight: bold; color: #1f2937; margin-bottom: 5px;}
.stat-label { color: #6b7280; font-weight: 500;}
.stat-period { color: #9ca3af; font-size: 0.8rem; margin-top: 5px; font-style: italic;}
.loading, .error, .empty { background: white; padding: 50px; border-radius: 15px; text-align: center; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);}
.empty-subtitle { color: #6b7280; font-size: 0.9rem; margin-top: 10px; opacity: 0.8;}
.spinner { width: 40px; height: 40px; border: 4px solid #f3f4f6; border-top: 4px solid #6366f1; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 20px;}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.btn-retry { background: #6366f1; color: white; border: none; padding: 12px 25px; border-radius: 8px; font-weight: 600; cursor: pointer; margin-top: 15px;}
.btn-retry:hover { background: #5b21b6; }
.links { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);}
.list-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px solid #f3f4f6;}
.list-header h2 { margin: 0; color: #1f2937;}
.view-controls { display: flex; gap: 5px;}
.view-controls button { padding: 10px 15px; border: 1px solid #e5e7eb; background: white; border-radius: 8px; cursor: pointer; transition: all 0.2s;}
.view-controls button:hover { background: #f9fafb;}
.view-controls button.active { background: #6366f1; color: white; border-color: #6366f1;}
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 25px;}
.link-card { border: 2px solid #e5e7eb; border-radius: 15px; overflow: hidden; transition: all 0.3s; position: relative; background: white;}
.link-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);}
.link-card.rank-1 { border-color: #fbbf24; box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.2);}
.link-card.rank-2 { border-color: #9ca3af; box-shadow: 0 0 0 3px rgba(156, 163, 175, 0.2);}
.link-card.rank-3 { border-color: #f97316; box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.2);}
.rank { position: absolute; top: 15px; right: 15px; background: #1f2937; color: white; width: 35px; height: 35px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; z-index: 2;}
.rank-1 .rank { background: linear-gradient(135deg, #fbbf24, #f59e0b);}
.rank-2 .rank { background: linear-gradient(135deg, #9ca3af, #6b7280);}
.rank-3 .rank { background: linear-gradient(135deg, #f97316, #ea580c);}
.card-body { padding: 20px;}
.link-name { font-size: 1.2rem; font-weight: 600; margin: 0 0 15px 0; color: #1f2937;}
.url { color: #6366f1; font-size: 0.95rem; margin-bottom: 10px;}
.clicks { color: #6b7280; margin-bottom: 15px; font-size: 0.95rem;}
.progress { width: 100%; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;}
.progress-bar { height: 100%; background: linear-gradient(90deg, #6366f1, #8b5cf6); border-radius: 4px; transition: width 0.6s ease;}
.list { display: flex; flex-direction: column; gap: 15px;}
.link-row { display: flex; align-items: center; gap: 20px; padding: 20px; border: 2px solid #e5e7eb; border-radius: 10px; transition: all 0.3s;}
.link-row:hover { background: #f9fafb; transform: translateX(5px);}
.link-row.rank-1 { border-color: #fbbf24; background: rgba(251, 191, 36, 0.05);}
.link-row.rank-2 { border-color: #9ca3af; background: rgba(156, 163, 175, 0.05);}
.link-row.rank-3 { border-color: #f97316; background: rgba(249, 115, 22, 0.05);}
.link-row .rank { font-size: 1.3rem; min-width: 35px;}
.details { flex: 1;}
.details h4 { margin: 0 0 5px 0; color: #1f2937; font-weight: 600;}
.details .id { color: #6b7280; font-size: 0.9rem;}
.details .url { color: #6366f1; font-size: 0.95rem; margin-top: 5px;}
.metrics { text-align: center;}
.metric strong { display: block; font-size: 1.3rem; color: #1f2937;}
.metric span { font-size: 0.85rem; color: #6b7280;}
.trend { font-size: 1.5rem; }
@media (max-width: 768px) {
  .stats-container { padding: 15px; }
  .header h1 { font-size: 2rem; }
  .tabs { flex-direction: column; }
  .overview { grid-template-columns: 1fr; }
  .grid { grid-template-columns: 1fr; }
  .list-header { flex-direction: column; gap: 15px; align-items: stretch; }
  .link-row { flex-wrap: wrap; gap: 15px; }
  .metrics { order: -1; width: 100%; }
}
</style>