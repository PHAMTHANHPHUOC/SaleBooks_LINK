<template>
  <div v-if="productTypes.length > 0">


    <div class="container-fluid">
    <div v-for="type in productTypes" :key="type.id" class="product-section mb-5">
      <div class="row">
        <div class="col-12">
          <h3 class="section-title text-primary fw-bold mb-4">{{ type.ten_loai }}</h3>
        </div>
      </div>
      
      <draggable 
        v-model="type.products" 
        @end="onDragEnd(type)"
        :options="{ 
          animation: 200, 
          ghostClass: 'ghost',
          chosenClass: 'chosen',
          dragClass: 'drag',
          forceFallback: true,
          fallbackClass: 'fallback'
        }"
        class="row g-3"
        item-key="id"
      >
        <template #item="{ element: product }">
          <div class="col-lg-2 col-md-4 col-sm-6 col-12">
            <div class="product-card h-100">
              <div class="card shadow-sm border-0 product-item h-100" 
                   @click="handleClick(product.id)" 
                   style="cursor: pointer;">
                <div class="card-img-wrapper position-relative overflow-hidden">
                  <img :src="getFullImageUrl(product.anh_dai_dien)" 
                       class="card-img-top product-image" 
                       @error="handleImageError"
                       alt="Product Image" />
                  <div class="overlay position-absolute top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center">
                    <i class=" text-white fs-2"></i>
                  </div>
                </div>
                
                <div class="card-body d-flex flex-column">
                  <h5 class="card-title product-name text-dark mb-3 flex-grow-1 text-center">
                    {{ product.ten_san_pham }}
                  </h5>
                  <div class="mt-auto">
                    <h4 class="product-price text-danger fw-bold mb-0">
                      ${{ formatPrice(product.gia_mac_dinh) }}
                    </h4>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </template>
      </draggable>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="row">
      <div class="col-12 text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Đang tải...</span>
        </div>
        <p class="mt-3 text-muted">Đang tải sản phẩm...</p>
      </div>
    </div>
    
    <!-- Empty State -->
    <div v-if="!loading && productTypes.length === 0" class="row">
      <div class="col-12 text-center py-5">
        <i class="fas fa-box-open text-muted" style="font-size: 4rem;"></i>
        <p class="mt-3 text-muted fs-5">Không có sản phẩm nào để hiển thị</p>
      </div>
    </div>
  </div>

  </div>
  <div v-else class="loading-message">
    <p>Đang tải dữ liệu...</p>
  </div>
  
 
</template>

<script>
import draggable from "vuedraggable";
import baseRequest from '../../../../src/core/baseRequest';

export default {
  components: { draggable },
  props: {
    loai: Object // { id, ten_loai, ... }
  },
  data() {
    return {
      productTypes: [],
      baseUrl: '',
      list_style: {},
      previewImageUrl: '',
      scrollPositions: {},
      maxScrollPositions: {},
    };
  },
  async mounted() {
    this.initializeBaseUrl();
    this.loadStyle();
    await this.loadAllProductTypes();
    // Test API data
    this.testApiData();
    
  },
  methods: {
    async loadAllProductTypes() {
  try {
    const resType = await baseRequest.get('products/type/list/');
    const types = resType.data.filter(type => type.tinh_trang == 1);
    const promises = types.map(async (type) => {
      const resProduct = await baseRequest.get(`products/type/${type.id}/`);
      const products = resProduct.data.status ? resProduct.data.data : [];
      
      // Debug: Log giá của sản phẩm để kiểm tra
    
      
      return {
        ...type,
        products: products
      };
    });
    this.productTypes = await Promise.all(promises);
        
        // Initialize scroll positions for horizontal scroll layouts
        this.$nextTick(() => {
          this.productTypes.forEach(type => {
            if (type.layout === 1) {
              this.scrollPositions[type.id] = 0;
              this.maxScrollPositions[type.id] = 0;
            }
          });
        });
  } catch (err) {
        console.error('Lỗi khi tải danh sách sản phẩm:', err);
    this.productTypes = [];
  }
},
    async onDragEnd(type) {
      try {
      // Lấy danh sách ID sản phẩm theo thứ tự mới
        const product_ids = type.products.map(p => p.id);

      // Gửi API cập nhật thứ tự
        const response = await baseRequest.post("products/update/order/", {
          loai_id: type.id,
        product_ids
      });

        if (response.data.status) {
          // Refresh dữ liệu để đảm bảo đồng bộ
          await this.refreshProductData(type.id);
          // Có thể thêm thông báo thành công ở đây
        } else {
          console.error("Lỗi cập nhật thứ tự:", response.data.message);
        }
      } catch (error) {
        console.error("Lỗi khi cập nhật thứ tự sản phẩm:", error);
        // Có thể thêm thông báo lỗi ở đây
      }
    },
    
    // Các method hỗ trợ
    initializeBaseUrl() {
      this.baseUrl = baseRequest.defaults?.baseURL || 
                    baseRequest.defaults?.url || 
                    baseRequest.config?.baseURL ||
                    'http://localhost:8000';
      this.baseUrl = this.baseUrl.replace(/\/$/, '');
    },
    
    async loadStyle() {
      try {
        const res = await baseRequest.get("api/styles/list/data/");
        if (res.data && res.data.data) {
          this.list_style = res.data.data;
        } else if (Array.isArray(res.data)) {
          this.list_style = res.data;
        } else {
          this.list_style = {};
        }
      } catch (error) {
        this.list_style = {};
      }
    },
    
    getStyle(tag) {
      const style = this.list_style[tag] || {};
      return {
        fontFamily: style.font_family || undefined,
        fontWeight: style.font_weight || undefined,
        color: style.color || undefined,
        background: style.background || undefined,
      };
    },
    
    getFullImageUrl(imagePath) {
      if (!imagePath) return '';
      
      if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
        return imagePath;
      }
      
      if (!imagePath.startsWith('/media/')) {
        imagePath = '/media/' + imagePath.replace(/^\/+/, '');
      }
      
      return this.baseUrl + imagePath;
    },
    
    handleImageError(event) {
      event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0zMCAyMEMyNi42ODYzIDIwIDI0IDIyLjY4NjMgMjQgMjZDMjQgMjkuMzEzNyAyNi42ODYzIDMyIDMwIDMyQzMzLjMxMzcgMzIgMzYgMjkuMzEzNyAzNiAyNkMzNiAyMi42ODYzIDMzLjMxMzcgMjAgMzAgMjBaIiBmaWxsPSIjOUNBM0FGIi8+CjxwYXRoIGQ9Ik0xNiA0MEw0NCA0MEw0MCAzNkwzNiAzMkwyOCAzNkwyMCAzMkwxNiAzNloiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+';
      event.target.alt = 'Không thể tải ảnh';
    },
    
  
    
    
    calcMargin(productCount) {
      // Calculate margin based on product count for responsive design
      if (productCount <= 4) return 20;
      if (productCount <= 8) return 30;
      return 40;
    },
    
    scrollLeft(typeId) {
      const scrollContainer = this.$refs[`scroll-${typeId}`];
      if (scrollContainer && scrollContainer[0]) {
        const container = scrollContainer[0];
        container.scrollLeft -= 300;
        this.updateScrollPosition(typeId, { target: container });
      }
    },
    
    scrollRight(typeId) {
      const scrollContainer = this.$refs[`scroll-${typeId}`];
      if (scrollContainer && scrollContainer[0]) {
        const container = scrollContainer[0];
        container.scrollLeft += 300;
        this.updateScrollPosition(typeId, { target: container });
      }
    },
    
    updateScrollPosition(typeId, event) {
      const container = event.target;
      this.scrollPositions[typeId] = container.scrollLeft;
      this.maxScrollPositions[typeId] = container.scrollWidth - container.clientWidth;
    },
    
    async refreshProductData(typeId) {
      try {
        // Reload sản phẩm cho loại cụ thể
        const resProduct = await baseRequest.get(`products/type/${typeId}/`);
        const updatedProducts = resProduct.data.status ? resProduct.data.data : [];
        
        // Cập nhật dữ liệu trong productTypes
        const typeIndex = this.productTypes.findIndex(type => type.id === typeId);
        if (typeIndex !== -1) {
          this.productTypes[typeIndex].products = updatedProducts;
        }
        
      } catch (error) {
        console.error("Lỗi khi refresh dữ liệu sản phẩm:", error);
      }
    },
    
    formatPrice(price) {
      // Kiểm tra nếu giá không tồn tại hoặc null/undefined
      if (!price && price !== 0) return '0 ₫';
      
      // Chuyển đổi thành chuỗi để xử lý
      let priceStr = String(price).trim();
      
      // Nếu chuỗi rỗng
      if (!priceStr) return '0 ₫';
      
      // Loại bỏ tất cả ký tự không phải số (giữ lại dấu chấm và dấu phẩy)
      let cleanPrice = priceStr.replace(/[^\d.,]/g, '');
      
      // Thay thế dấu phẩy bằng dấu chấm (để parseFloat hiểu đúng)
      cleanPrice = cleanPrice.replace(',', '.');
      
      // Nếu chuỗi rỗng sau khi clean
      if (!cleanPrice) return '0 ₫';
      
      // Chuyển đổi thành số
      const numPrice = parseFloat(cleanPrice);
      
      // Kiểm tra nếu không phải là số hợp lệ
      if (isNaN(numPrice)) {
        console.warn('Invalid price value:', price, '-> cleaned:', cleanPrice);
        return '0 ₫';
      }
      
      // Kiểm tra nếu là số âm
      if (numPrice < 0) return '0 ₫';
      
      // Format với dấu phẩy theo định dạng Việt Nam (không làm tròn)
      const formattedPrice = numPrice.toLocaleString('vi-VN');
      return `${formattedPrice} `;
    },
    
    
  }
};
</script>

<style>
.drag-area {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  min-height: 50px;
  padding: 20px 0;
  width: 100%;
  box-sizing: border-box;
}

.product-card {
  border: none;
  border-radius: 12px;
  background: #ffffff;
  cursor: move;
  transition: all 0.3s ease;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  width: 100%;
  height: auto;
  max-width: 100%;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

/* Drag & Drop Styles */
.ghost {
  opacity: 0.6;
  background: #e3f2fd;
  border: 2px dashed #3498db;
  border-radius: 12px;
}

.chosen {
  background: #f0f8ff;
  border-color: #3498db;
  transform: rotate(1deg);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

.drag {
  background: #e3f2fd;
  border-color: #2980b9;
  transform: rotate(-1deg);
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  z-index: 1000;
}

.fallback {
  background: #f0f8ff;
  border: 2px dashed #3498db;
  opacity: 0.8;
  border-radius: 12px;
}

/* Drag & Drop Styles for Layout 2 (Button Layout) */
.ghost-btn {
  opacity: 0.6;
  background: #e3f2fd;
  border: 2px dashed #3498db;
  border-radius: 12px;
}

.chosen-btn {
  background: #f0f8ff;
  border-color: #3498db;
  transform: rotate(1deg);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

.drag-btn {
  background: #e3f2fd;
  border-color: #2980b9;
  transform: rotate(-1deg);
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  border-radius: 12px;
  z-index: 1000;
}

.fallback-btn {
  background: #f0f8ff;
  border: 2px dashed #3498db;
  opacity: 0.8;
  border-radius: 12px;
}

/* Drag & Drop Styles for Layout 1 (Horizontal Scroll) */
.ghost-horizontal {
  opacity: 0.6;
  background: #e3f2fd;
  border: 2px dashed #3498db;
  border-radius: 12px;
}

.chosen-horizontal {
  background: #f0f8ff;
  border-color: #3498db;
  transform: rotate(1deg);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

.drag-horizontal {
  background: #e3f2fd;
  border-color: #2980b9;
  transform: rotate(-1deg);
  box-shadow: 0 8px 20px rgba(0,0,0,0.15);
  z-index: 1000;
}


.fallback-horizontal {
  background: #f0f8ff;
  border: 2px dashed #3498db;
  opacity: 0.8;
  border-radius: 12px;
}

/* Product list styling */
.product-list {
  padding: 20px 0;
  width: 100%;
  box-sizing: border-box;
}

.product-section {
  margin-bottom: 40px;
  background: #fafbfc;
  border-radius: 16px;
  padding: 25px;
  border: 1px solid #e9ecef;
  width: 100%;
  box-sizing: border-box;
  overflow: hidden;
}

.product-link {
  text-decoration: none;
  color: inherit;
  display: block;
  width: 100%;
  height: 100%;
}

.product-link:hover {
  text-decoration: none;
  color: inherit;
}

.card {
  border: none;
  border-radius: 12px;
  overflow: hidden;
  background: #ffffff;
  transition: all 0.3s ease;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.card-img-top {
  width: 100%;
  height: 200px;
  object-fit: contain;
  object-position: center;
  background: #f8f9fa;
  cursor: pointer;
  border-bottom: 1px solid #e9ecef;
  flex-shrink: 0;
}

.product-name {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #2c3e50;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-price {
  font-size: 18px;
  font-weight: 700;
  color: #e74c3c;
  margin: 0;
  text-align: center;
}

.h3-title {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 25px;
  color: #2c3e50;
  border-bottom: 3px solid #3498db;
  padding-bottom: 10px;
  position: relative;
}

.h3-title::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 50px;
  height: 3px;
  background: #e74c3c;
}

.loading-message {
  text-align: center;
  padding: 60px;
  color: #6c757d;
  font-size: 18px;
  background: #f8f9fa;
  border-radius: 12px;
  margin: 20px 0;
}

/* Layout 2: Button Layout Styles */
.product-list-btn {
  padding: 20px 0;
}

.drag-area-btn {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  min-height: 50px;
}

.btn-layout2 {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  min-width: 280px;
  cursor: move;
  background: #ffffff;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.btn-layout2:hover {
  text-decoration: none;
  color: inherit;
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
  border-color: #3498db;
}

.btn-layout2-img {
  width: 60px;
  height: 60px;
  object-fit: contain;
  object-position: center;
  border-radius: 8px;
  margin-right: 15px;
  cursor: pointer;
  background: #f8f9fa;
  border: 1px solid #e9ecef;
}

.btn-layout2-content {
  flex: 1;
}

.btn-layout2-title {
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  display: block;
  margin-bottom: 5px;
  line-height: 1.4;
}

.btn-layout2-sub {
  font-size: 14px;
  color: #e74c3c;
  font-weight: 600;
}

/* Layout 1: Horizontal Scroll Styles */
.produc-layout-01 {
  margin-bottom: 30px;
}

.horizontal-scroll-container {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
}

.scroll-nav-btn {
  background: #ffffff;
  border: 2px solid #e9ecef;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #6c757d;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.scroll-nav-btn:hover:not(:disabled) {
  background: #3498db;
  color: #ffffff;
  border-color: #3498db;
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.scroll-nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.horizontal-scroll {
  overflow-x: auto;
  padding: 10px 0;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

.drag-area-horizontal {
  display: flex;
  gap: 20px;
  min-height: 50px;
  padding: 10px 0;
}

.horizontal-scroll::-webkit-scrollbar {
  display: none;
}

.horizontal-scroll .product-link {
  flex-shrink: 0;
  width: 280px;
}

/* Shop Now Button Styles */
.shop-now-wrapper {
  text-align: center;
  margin: 20px 0;
}

.shop-now-btn {
  display: inline-block;
  padding: 12px 24px;
  background: #ff6b9d;
  color: white;
  text-decoration: none;
  border-radius: 25px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.shop-now-btn:hover {
  background: #ff5582;
  color: white;
  text-decoration: none;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(255, 107, 157, 0.3);
}

.btn-layout-01 {
  background: #ff6b9d;
}

.btn-layout-01:hover {
  background: #ff5582;
}

/* Responsive Design */
@media (max-width: 768px) {
  .btn-layout2 {
    min-width: 150px;
    padding: 8px 12px;
  }
  
  .btn-layout2-img {
    width: 40px;
    height: 40px;
  }
  
  .horizontal-scroll .product-link {
    width: 150px;
  }
  
  .scroll-nav-btn {
    width: 35px;
    height: 35px;
  }
}
</style>
