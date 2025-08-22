<template>
  <div class="stats-container">
    <!-- Header -->
    <div class="header">
      <h1>📊 Thống kê sản phẩm</h1>
      <p>Theo dõi hiệu suất và xu hướng sản phẩm</p>
    </div>

    <!-- Filter Tabs -->
    <div class="tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.key"
        :class="{ 'active': activeTab === tab.key }"
        @click="loadTop(tab.key)"
      >
        {{ tab.icon }} {{ tab.label }}
      </button>
    </div>

    <!-- Stats Overview -->
    <div class="overview" v-if="topSanPham.length > 0">
      <div class="stat-box">
        <div class="stat-number">{{ topSanPham.length }}</div>
        <div class="stat-label">Sản phẩm</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">{{ totalViews.toLocaleString() }}</div>
        <div class="stat-label">Tổng lượt xem</div>
      </div>
      <div class="stat-box">
        <div class="stat-number">{{ topProduct ? '🏆' : '-' }}</div>
        <div class="stat-label">{{ topProduct?.ten || 'Chưa có dữ liệu' }}</div>
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
    <div v-else-if="topSanPham.length === 0" class="empty">
      <p>📈 Chưa có dữ liệu trong khoảng thời gian này</p>
    </div>

    <!-- Product List -->
    <div v-else class="products">
      <div class="list-header">
        <h2>Top sản phẩm {{ getActiveTabLabel() }}</h2>
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
          v-for="(sp, index) in topSanPham" 
          :key="sp.id"
          class="product-card"
          :class="getRankClass(index)"
        >
          <div class="card">
            <img :src="sp.anh" class="card-img-top" alt="...">
            <div class="card-body">
              <h4 class="product-name">{{ sp.ten }}</h4>
              <div class="views">
              👁️ {{ sp.so_luot.toLocaleString() }} lượt xem
            </div>
            <div class="progress">
              <div 
                class="progress-bar"
                :style="{ width: getProgressWidth(sp.so_luot) + '%' }"
              ></div>
            </div>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="list">
        <div 
          v-for="(sp, index) in topSanPham" 
          :key="sp.id"
          class="product-row"
          :class="getRankClass(index)"
        >
          <div class="rank">{{ index + 1 }}</div>
          <div class="thumbnail">
            <img :src="sp.anh" :alt="sp.ten" @error="handleImageError" />
          </div>
          <div class="details">
            <h4>{{ sp.ten }}</h4>
            <span class="id">ID: {{ sp.id }}</span>
          </div>
          <div class="metrics">
            <div class="metric">
              <strong>{{ sp.so_luot.toLocaleString() }}</strong>
              <span>lượt xem</span>
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
  name: 'ProductStats',
  data() {
    return {
      topSanPham: [],
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
    totalViews() {
      return this.topSanPham.reduce((sum, sp) => sum + sp.so_luot, 0);
    },
    
    topProduct() {
      return this.topSanPham[0] || null;
    }
  },
  
  methods: {
    async loadTop(loai) {
      this.loading = true;
      this.error = null;
      this.activeTab = loai;
      
      try {
        const res = await baseRequest.get(`san-pham/top/`, {
          params: { loai }
        });
        this.topSanPham = res.data || [];
      } catch (error) {
        this.error = "Không thể tải dữ liệu. Vui lòng thử lại.";
        console.error("Lỗi khi load top sản phẩm:", error);
      } finally {
        this.loading = false;
      }
    },
    
    getActiveTabLabel() {
      const tab = this.tabs.find(t => t.key === this.activeTab);
      return tab ? tab.label.toLowerCase() : '';
    },
    
    getProgressWidth(views) {
      const maxViews = Math.max(...this.topSanPham.map(sp => sp.so_luot));
      return maxViews > 0 ? (views / maxViews) * 100 : 0;
    },
    
    getRankClass(index) {
      if (index === 0) return 'rank-1';
      if (index === 1) return 'rank-2';
      if (index === 2) return 'rank-3';
      return '';
    },
    
    handleImageError(event) {
      event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMjAwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik03NSA3NUgxMjVWMTI1SDc1Vjc1WiIgZmlsbD0iI0Q1RDlERCIvPgo8L3N2Zz4K';
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
.stats-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: linear-gradient(135deg, #f8f8f8 0%, #e4e2e9 100%);
  min-height: 100vh;
  color: #1f2937;
}

/* Header */
.header {
  text-align: center;
  margin-bottom: 30px;
  color: rgb(19, 19, 19);
}

.header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin: 0 0 10px 0;
}

.header p {
  font-size: 1.1rem;
  opacity: 0.9;
  margin: 0;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  background: rgba(255, 255, 255, 0.1);
  padding: 10px;
  border-radius: 15px;
  backdrop-filter: blur(10px);
}

.tabs button {
  flex: 1;
  padding: 15px;
  border: none;
  border-radius: 10px;
  background: transparent;
  color: rgb(3, 3, 3);
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.tabs button:hover {
  background: rgba(255, 255, 255, 0.1);
}

.tabs button.active {
  background: white;
  color: #6366f1;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

/* Overview Stats */
.overview {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-box {
  background: white;
  padding: 25px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.stat-number {
  font-size: 2rem;
  font-weight: bold;
  color: #1f2937;
  margin-bottom: 5px;
}

.stat-label {
  color: #6b7280;
  font-weight: 500;
}

/* Loading, Error, Empty States */
.loading, .error, .empty {
  background: white;
  padding: 50px;
  border-radius: 15px;
  text-align: center;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f4f6;
  border-top: 4px solid #6366f1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.btn-retry {
  background: #6366f1;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 15px;
}

.btn-retry:hover {
  background: #5b21b6;
}

/* Product List */
.products {
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding-bottom: 15px;
  border-bottom: 2px solid #f3f4f6;
}

.list-header h2 {
  margin: 0;
  color: #1f2937;
}

.view-controls {
  display: flex;
  gap: 5px;
}

.view-controls button {
  padding: 10px 15px;
  border: 1px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.view-controls button:hover {
  background: #f9fafb;
}

.view-controls button.active {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

/* Grid View */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}

.product-card {
  border: 2px solid #e5e7eb;
  border-radius: 15px;
  overflow: hidden;
  transition: all 0.3s;
  position: relative;
  background: white;
}

.product-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
}

.product-card.rank-1 {
  border-color: #fbbf24;
  box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.2);
}

.product-card.rank-2 {
  border-color: #9ca3af;
  box-shadow: 0 0 0 3px rgba(156, 163, 175, 0.2);
}

.product-card.rank-3 {
  border-color: #f97316;
  box-shadow: 0 0 0 3px rgba(249, 115, 22, 0.2);
}

.rank {
  position: absolute;
  top: 15px;
  right: 15px;
  background: #1f2937;
  color: white;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  z-index: 2;
}

.rank-1 .rank {
  background: linear-gradient(135deg, #fbbf24, #f59e0b);
}

.rank-2 .rank {
  background: linear-gradient(135deg, #9ca3af, #6b7280);
}

.rank-3 .rank {
  background: linear-gradient(135deg, #f97316, #ea580c);
}

.image-container {
  height: 200px;
  overflow: hidden;
  background: #f9fafb;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.product-card:hover .image-container img {
  transform: scale(1.1);
}

.content {
  padding: 20px;
}

.content h3 {
  font-size: 1.2rem;
  font-weight: 600;
  margin: 0 0 15px 0;
  color: #1f2937;
}

.views {
  color: #6b7280;
  margin-bottom: 15px;
  font-size: 0.95rem;
}

.progress {
  width: 100%;
  height: 8px;
  background: #e5e7eb;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #8b5cf6);
  border-radius: 4px;
  transition: width 0.6s ease;
}

/* List View */
.list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.product-row {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  transition: all 0.3s;
}

.product-row:hover {
  background: #f9fafb;
  transform: translateX(5px);
}

.product-row.rank-1 {
  border-color: #fbbf24;
  background: rgba(251, 191, 36, 0.05);
}

.product-row.rank-2 {
  border-color: #9ca3af;
  background: rgba(156, 163, 175, 0.05);
}

.product-row.rank-3 {
  border-color: #f97316;
  background: rgba(249, 115, 22, 0.05);
}

.product-row .rank {
  position: relative;
  top: auto;
  right: auto;
  font-size: 1.3rem;
  min-width: 35px;
}

.thumbnail {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  overflow: hidden;
  background: #f9fafb;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.details {
  flex: 1;
}

.details h4 {
  margin: 0 0 5px 0;
  color: #1f2937;
  font-weight: 600;
}

.details .id {
  color: #6b7280;
  font-size: 0.9rem;
}

.metrics {
  text-align: center;
}

.metric strong {
  display: block;
  font-size: 1.3rem;
  color: #1f2937;
}

.metric span {
  font-size: 0.85rem;
  color: #6b7280;
}

.trend {
  font-size: 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .stats-container {
    padding: 15px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .tabs {
    flex-direction: column;
  }
  
  .overview {
    grid-template-columns: 1fr;
  }
  
  .grid {
    grid-template-columns: 1fr;
  }
  
  .list-header {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
  
  .product-row {
    flex-wrap: wrap;
    gap: 15px;
  }
  
  .metrics {
    order: -1;
    width: 100%;
  }
}
</style>