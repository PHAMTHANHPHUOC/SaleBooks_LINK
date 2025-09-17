<template>
<div class="bogiki-linktree">
    <!-- Avatar & Name -->
    <div class="profile ">
      <h1 class="avatar-circle">
        <img class="avatar-img" src="../../../assets/images/TINY.jpg" alt="Avatar" />
      </h1>
      <h1 :style="getStyle('tinydaisy')" class="brand">@tinydaisy.coloring</h1>
    </div>

    <!-- Social Icons -->
    <h2 class="h2-title"  :style="getStyle('tieude')"  >Relaxing Coloring Books </h2>
    <div class="social-list">
        <a
          v-for="item in Array_link.filter(link => link.loai === 0 && link.tinh_trang === 1)"
          :key="item.id"
          :href="item.links"
          target="_blank"
          rel="noopener"
          class="social-btn"
          :aria-label="item.name"
          @click="handleLinkClick(item.id)"
        >
          <img
            :src="getFullImageUrl(item.anh_dai_dien)"
            class="icon-connect"
            @error="handleImageError"
            @click="showImagePreview(getFullImageUrl(item.anh_dai_dien))"
          />
        </a>
</div>
    <div class="button-list ">
  <a
    v-for="item in Array_link.filter(link => link.loai === 1 && link.tinh_trang === 1)"
    :key="item.id"
    :style="getStyle('button')"
    class="main-btn"
    :href="item.links"
    target="_blank"
    rel="noopener"
    @click="handleLinkClick(item.id)"
  >
    <span class="website-btn-content name-socal">
      <img
        :src="getFullImageUrl(item.anh_dai_dien)"
        class="btn-icon"
        @error="handleImageError"
        @click="showImagePreview(getFullImageUrl(item.anh_dai_dien))"
      />
    {{ item.name }}<br>
      <span class="sub-title" >{{ item.subtitle }}</span> <br>
        </span>
  </a>
</div>


    <!-- Community -->
    <!-- <h2 class="h2-title" :style="getStyle('tieude')" >Connect with me</h2> -->
   <div class="button-list link-icon">
  <a
    v-for="item in Array_link.filter(link => link.loai === 2 && link.tinh_trang === 1)"
    :key="item.id"
    :style="getStyle('button')"
    class="main-btn"
    :href="item.links"
    target="_blank"
    rel="noopener"
    @click="handleLinkClick(item.id)"
  >
  <span class="website-btn-content name-socal">{{ item.name }}<br>
  <span class="sub-title" >{{ item.subtitle }}</span> <br>
  </span>
  </a>
</div>

    <div v-for="type in productTypes.filter(link => link.layout === 2)" :key="type.id" class="product-section">
  <h3 :style="getStyle('loai-san-pham')" class="h3-title">{{ type.ten_loai }}</h3>
  <div class="product-list-btn">
    <a
      v-for="product in type.products"
      :key="product.id"
      :href="product.duong_dan_ngoai"
      @click="handleClick(product.id)"
      target="_blank"
      class="btn-layout2"
    >
      <img
        :src="getFullImageUrl(product.anh_dai_dien)"
        class="btn-layout2-img"
        @error="handleImageError"
        @click.stop="showImagePreview(getFullImageUrl(product.anh_dai_dien))"
      />
      <span class="btn-layout2-content">
        <span :style="getStyle('collapse-title')" class="btn-layout2-title">{{ product.ten_san_pham }}</span><br>
        <span :style="getStyle('collapse-sub')" class="btn-layout2-sub">{{ product.gia_mac_dinh }}</span>
      </span>
    </a>
  </div>
  <!-- <div class="shop-now-wrapper" :style="{ marginTop: '20px' }">
    <a
      v-if="type.link_danh_muc"
      target="_blank"
      rel="noopener"
      :href="type.link_danh_muc"
      :style="getStyle('button-shop-now')"
      class="shop-now-btn"
    >SHOP NOW</a>
  </div> -->
</div>
    <!-- Product Section: For từng loại sản phẩm -->
    <div  v-for="type in productTypes.filter(link => link.layout === 0)" :key="type.id" class="product-section">
      <h3 :style="getStyle('loai-san-pham')" class="h3-title ">{{ type.ten_loai }}</h3>
      <div class="product-list ">
        <a v-for="product in type.products" :key="product.id" :href="product.duong_dan_ngoai"  @click="handleClick(product.id)" target="_blank" class="product-link">
          <div class="card">
            <img :src="getFullImageUrl(product.anh_dai_dien)" 
                 class="card-img-top" 
                 @error="handleImageError"
                 @click="showImagePreview(getFullImageUrl(product.anh_dai_dien))" />
            <div class="card-body">
              <h4 :style="getStyle('san-pham')" class="product-name">{{ product.ten_san_pham }}</h4>
              <h4 :style="getStyle('price')" class="product-price">{{ product.gia_mac_dinh }}</h4>
            </div>
          </div>
        </a>
      </div>
      <!-- Enhanced calcMargin for multiple devices -->
      <h4 :style="{ marginTop: calcMargin(type.products.length) + 'px' }" class="shop-now-wrapper">
        <a v-if="type.link_danh_muc" target="_blank" rel="noopener" :href="type.link_danh_muc" :style="getStyle('button-shop-now')" class="shop-now-btn">SHOP NOW</a>
      </h4>
    </div>
    <div v-for="type in productTypes.filter(link => link.layout === 1)" :key="type.id" class="product-section">
  <h3 :style="getStyle('loai-san-pham')" class="h3-title ">{{ type.ten_loai }}</h3>
  <div class="product-list horizontal-scroll">
    <a v-for="product in type.products" :key="product.id" :href="product.duong_dan_ngoai" @click="handleClick(product.id)" target="_blank" class="product-link">
      <div class="card">
        <img :src="getFullImageUrl(product.anh_dai_dien)" 
             class="card-img-top" 
             @error="handleImageError"
             @click="showImagePreview(getFullImageUrl(product.anh_dai_dien))" />
        <div class="card-body">
          <h4 :style="getStyle('san-pham')" class="product-name">{{ product.ten_san_pham }}</h4>
          <h4 :style="getStyle('price')" class="product-price">{{ product.gia_mac_dinh }}</h4>
        </div>
      </div>
    </a>
  </div>

    </div>
   



    
  </div>
  
  <footer class="footer">
    <div class="footer-inner">
      <img src="../../../assets/images/TINY.jpg" alt="Tiny Logo" class="avatar-footer" />
      <h4 :style="getStyle('email')"v-if="list_link.Email" class="email-footer text-decoration-none ">{{ list_link.Email.link }}</h4>
    </div>
  </footer>
</template>

<script>
import baseRequest from '../../../../src/core/baseRequest';

export default {
  data() {
    return {
      productTypes: [], // [{id, ten_loai, products: []}]
      windowWidth: window.innerWidth,
      list_link : {},
      windowHeight: window.innerHeight,
      baseUrl: '',
      list_style: {},
      resizeKey : 0,
      Array_link : [],
      api_response: null,
      loading: false,

    };
  },
  computed: {
    isMobile() {
      return this.windowWidth <= 820;
    },
    deviceType() {
      const width = this.windowWidth;
      const height = this.windowHeight;
      const aspectRatio = width / height;
      
      // Phân loại thiết bị chi tiết
      if (width <= 375) return 'small-phone';      // iPhone SE, iPhone 12 mini
      if (width <= 390) return 'pro-phone';      // iPhone SE, iPhone 12 mini
      if (width <= 414) return 'medium-phone';     // iPhone XR, iPhone 12/13/14
      if (width <= 480) return 'large-phone';      // iPhone 14 Pro Max, Pixel 7
      if (width <= 768) return 'tablet-portrait';  // iPad portrait
      if (width <= 820) return 'tablet-landscape'; // iPad landscape
      if (width <= 1024) return 'small-tablet';    // iPad Air
      if (width <= 1366) return 'laptop';          // Small laptops
      return 'desktop';
    }
  },
  async mounted() {
    console.log("layout",this.productTypes);

    this.initializeBaseUrl();
    this.loadlink();
    this.loadAllProductTypes();
    this.loadBackground();
    this.loadlink_Array();
    
    await this.loadStyle();
    // this.loadFonts();
  try {
    const res = await baseRequest.get('api/frontend-page-visit/?page=home');
  } catch (err) {
    console.error(err);
  }
  window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  watch: {
    windowWidth() {
      this.resizeKey++;
    },
    windowHeight() {
      this.resizeKey++;
    }
  },
  methods: {
    handleResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
      this.$forceUpdate();
    },
   
    // Enhanced calcMargin for multiple devices
    calcMargin(cardCount) {
      const deviceType = this.deviceType;
      const width = this.windowWidth;
     
     switch (deviceType) {
  case 'small-phone': // iPhone SE (375px)
    if (cardCount <= 2) return -110;
    if (cardCount <= 4) return 160;
    if (cardCount <= 6) return 440;
    if (cardCount <= 8) return 700;
    if (cardCount <= 10) return 980;
    if (cardCount <= 12) return 1250;
    if (cardCount <= 14) return 1520;
    if (cardCount <= 16) return 1790;
    if (cardCount <= 18) return 2060;
    if (cardCount <= 20) return 2330;
  case 'pro-phone': // iPhone 12pro (390px)
    if (cardCount <= 2) return -110;
    if (cardCount <= 4) return 180;
    if (cardCount <= 6) return 450;
    if (cardCount <= 8) return 730;
    if (cardCount <= 10) return 1000;
    if (cardCount <= 12) return 1280 ;
    if (cardCount <= 14) return 1560;
    if (cardCount <= 16) return 1835;
    if (cardCount <= 18) return 2120;
    if (cardCount <= 20) return 2400;

  case 'medium-phone': // iPhone XR, 12/13/14 (414px)
    if (cardCount <= 2) return -90;
    if (cardCount <= 4) return 200;
    if (cardCount <= 6) return 480;
    if (cardCount <= 8) return 770;
    if (cardCount <= 10) return 1070;
    if (cardCount <= 12) return 1350;
    if (cardCount <= 14) return 1640;
    if (cardCount <= 16) return 1920;
    if (cardCount <= 18) return 2210;
    if (cardCount <= 20) return 2500;

  case 'large-phone': // iPhone 14 Pro Max, Pixel 7 (428-480px)
    if (cardCount <= 2) return -88;
    if (cardCount <= 4) return 220;
    if (cardCount <= 6) return 520;
    if (cardCount <= 8) return 820;
    if (cardCount <= 10) return 1120;
    if (cardCount <= 12) return 1420;
    if (cardCount <= 14) return 1720;
    if (cardCount <= 16) return 2020;
    if (cardCount <= 18) return 2320;
    if (cardCount <= 20) return 2620;

  case 'tablet-portrait': // iPad portrait (768px)
    if (cardCount <= 2) return 90;
    if (cardCount <= 4) return 590;
    if (cardCount <= 6) return 1080;
    if (cardCount <= 8) return 1560;
    if (cardCount <= 10) return 2070;
    if (cardCount <= 12) return 2550;
    if (cardCount <= 14) return 3040;
    if (cardCount <= 16) return 3530;
    if (cardCount <= 18) return 4020;
    if (cardCount <= 20) return 4510;

  case 'tablet-landscape': // iPad landscape (820px)
    if (cardCount <= 2) return 110;
    if (cardCount <= 4) return 630;
    if (cardCount <= 6) return 1160;
    if (cardCount <= 8) return 1670;
    if (cardCount <= 10) return 2170;
    if (cardCount <= 12) return 2680;
    if (cardCount <= 14) return 3190;
    if (cardCount <= 16) return 3700;
    if (cardCount <= 18) return 4210;
    if (cardCount <= 20) return 4720;

  case 'small-tablet': // iPad Air (1024px)
    if (cardCount <= 3) return 90;
    if (cardCount <= 6) return 1070;
    if (cardCount <= 9) return 1550;
    if (cardCount <= 12) return 2050;
    if (cardCount <= 15) return 2530;
    if (cardCount <= 18) return 3010;
    if (cardCount <= 21) return 3490;

  default: // Desktop (1920px+)
    if (cardCount <= 2) return 90;     // 1–2 card
    if (cardCount <= 4) return 555;    // 3–4 card
    if (cardCount <= 6) return 1050;   // 5–6 card
    if (cardCount <= 8) return 1530;   // 7–8 card
    if (cardCount <= 10) return 2010;  // 9–10 card
    if (cardCount <= 12) return 2490;  // 11–12 card
    if (cardCount <= 14) return 2980;  // 13–14 card
    if (cardCount <= 16) return 3460;  // 15–16 card
    if (cardCount <= 18) return 3950;  // 17–18 card
    if (cardCount <= 20) return 4440;  // 19–20 card
}
     
      
    },

    // Alternative method: calcMargin with aspect ratio consideration
    calcMarginWithAspectRatio(cardCount) {
      const width = this.windowWidth;
      const height = this.windowHeight;
      const aspectRatio = width / height;
      const isPortrait = aspectRatio < 1;
      const isSquareish = aspectRatio >= 1 && aspectRatio <= 1.3;
      const isWide = aspectRatio > 1.3;

      // Base margin calculation
      let baseMargin;
      if (width <= 375) baseMargin = 80;
      else if (width <= 414) baseMargin = 90;
      else if (width <= 480) baseMargin = 100;
      else if (width <= 768) baseMargin = 140;
      else if (width <= 1024) baseMargin = 170;
      else baseMargin = 200;

      // Adjust based on aspect ratio
      let aspectMultiplier = 1;
      if (isPortrait) aspectMultiplier = 0.9;  // Tighter spacing for portrait
      else if (isWide) aspectMultiplier = 1.2; // More spacing for wide screens

      const rows = Math.ceil(cardCount / 2);
      return Math.round(baseMargin * aspectMultiplier * (rows - 0.5));
    },
    async loadBackground() {
    try {
      const res = await baseRequest.get("api/styles/background/");
      document.body.style.background = res.data.background || "#fffef3";
    } catch (e) {
      document.body.style.background = "#fffef3";
    }
  },

    // Method with device pixel ratio consideration
    calcMarginWithDPR(cardCount) {
      const width = this.windowWidth;
      const dpr = window.devicePixelRatio || 1;
      
      // Adjust for high-DPI displays
      let dpiMultiplier = 1;
      if (dpr >= 3) dpiMultiplier = 0.85;      // iPhone retina
      else if (dpr >= 2) dpiMultiplier = 0.9; // Most modern phones
      
      // Base calculation
      let margin;
      if (width <= 414) {
        margin = Math.ceil(cardCount / 2) * 95 * dpiMultiplier;
      } else if (width <= 768) {
        margin = Math.ceil(cardCount / 2) * 140 * dpiMultiplier;
      } else {
        margin = Math.ceil(cardCount / 4) * 170 * dpiMultiplier;
      }
      
      return Math.round(margin);
    },

    async loadAllProductTypes() {
      try {
        const resType = await baseRequest.get('products/type/list/');
        const types = resType.data.filter(type => type.tinh_trang == 1);
        const promises = types.map(async (type) => {
          const resProduct = await baseRequest.get(`products/type/${type.id}/`);
          return {
            ...type,
            products: resProduct.data.status ? resProduct.data.data : []
          };
        });
        this.productTypes = await Promise.all(promises);
      } catch (err) {
        this.productTypes = [];
      }
    },
     async handleLinkClick(linkId) {
    try {
      await baseRequest.post(`api/links/${linkId}/click/`);
    } catch (error) {
      console.error("Lỗi khi ghi nhận click link:", error);
    }
  },
    
    async handleClick(productId) {
      try {
        const res = await baseRequest.post(`san-pham/${productId}/click/`);
        console.log(res.data);
      } catch (error) {
        console.error("Lỗi khi gửi click:", error);
      }
    },
    loadlink_Array() {
            this.loading = true;
            baseRequest
              .get("api/links/list/data/")
              .then((res) => {
                console.log("API Response:", res.data); 
                this.api_response = JSON.stringify(res.data);
                
                // Kiểm tra cấu trúc response
                if (res.data && res.data.data) {
                  this.Array_link = res.data.data;
                } else if (Array.isArray(res.data)) {
                  // Trường hợp API trả về trực tiếp array
                  this.Array_link = res.data;
                } else {
                  console.error("Unexpected response structure:", res.data);
                  this.Array_link = [];
                }
                
                if (res.data.status === 0) {
                  toaster.error(res.data.message);
                }
              })
              .catch((error) => {
                console.error("API Error:", error);
                this.Array_link = [];
                if (toaster) {
                  toaster.error("Lỗi khi tải dữ liệu: " + error.message);
                }
              })
              .finally(() => {
                this.loading = false;
              });
          },
    loadlink() {
      baseRequest
        .get("api/links/list/")
        .then((res) => {
           console.log('Links:', res.data); 
          if (res.data && res.data.data) {
            this.list_link = res.data.data;
          } else if (Array.isArray(res.data)) {
            this.list_link = res.data;
          } else {
            this.list_link = {};
          }
          console.log('list_link:', this.list_link);
        })
        .catch(() => {
          this.list_link = {};
          console.error('Error loading links:', err);
        });
    },
     async loadStyle() {
    baseRequest
      .get("api/styles/list/data/")
      .then((res) => {
        if (res.data && res.data.data) {
          this.list_style = res.data.data;
        } else if (Array.isArray(res.data)) {
          this.list_style = res.data;
        } else {
          this.list_style = {};
        }
        // Tự động tải font nếu có
        Object.values(this.list_style).forEach(style => {
          if (style.font_family) this.loadFont(style.font_family);
        });
      })
      .catch(() => {
        this.list_style = {};
      });
  },
      loadFont(fontFamily) {
  if (!fontFamily) return;
  // Google Fonts
  const googleFontUrl = `https://fonts.googleapis.com/css?family=${fontFamily.replace(/ /g, '+')}:400,700&display=swap`;
  // Kiểm tra đã tải chưa
  if (!document.querySelector(`link[href="${googleFontUrl}"]`)) {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = googleFontUrl;
    document.head.appendChild(link);
  }
},
        getStyle(tag) {
          const style = this.list_style[tag] || {};
          return {
            fontFamily: style.font_family || undefined,
            fontSize: style.font_size || undefined,
            color: style.color || undefined,
            background: style.background || undefined,
          };
        },
    getFullImageUrl(imagePath) {
  if (!imagePath) return '';
  
  // Nếu đã là URL đầy đủ thì return luôn
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
    return imagePath;
  }

  // Nếu đường dẫn không bắt đầu bằng /media thì thêm vào
  if (!imagePath.startsWith('/media/')) {
    imagePath = '/media/' + imagePath.replace(/^\/+/, '');
  }

  // Đảm bảo baseUrl là IP LAN, không phải localhost
  let baseUrl = this.baseUrl;
  if (baseUrl.includes('localhost') || baseUrl.includes('127.0.0.1')) {
    baseUrl = 'http://192.168.1.28:8000'; // Đổi thành IP LAN của bạn
  }

  // Bỏ dấu / cuối nếu có
  baseUrl = baseUrl.replace(/\/$/, '');

  return baseUrl + imagePath;
},
    showImagePreview(imageUrl) {
      this.previewImageUrl = imageUrl;
      // Sử dụng Bootstrap modal
      const modal = new bootstrap.Modal(document.getElementById('imagePreviewModal'));
      modal.show();
    },
    handleImageError(event) {
      event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0zMCAyMEMyNi42ODYzIDIwIDI0IDIyLjY4NjMgMjQgMjZDMjQgMjkuMzEzNyAyNi42ODYzIDMyIDMwIDMyQzMzLjMxMzcgMzIgMzYgMjkuMzEzNyAzNiAyNkMzNiAyMi42ODYzIDMzLjMxMzcgMjAgMzAgMjBaIiBmaWxsPSIjOUNBM0FGIi8+CjxwYXRoIGQ9Ik0xNiA0MEw0NCA0MEw0MCAzNkwzNiAzMkwyOCAzNkwyMCAzMkwxNiAzNloiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+';
      event.target.alt = 'Không thể tải ảnh';
    },
     initializeBaseUrl() {
      // Lấy baseURL từ baseRequest
      this.baseUrl = baseRequest.defaults?.baseURL || 
                    baseRequest.defaults?.url || 
                    baseRequest.config?.baseURL ||
                    'http://localhost:8000' ||
                    'http://192.168.1.28:8000'; // fallback
      
      // Bỏ dấu / cuối nếu có
      this.baseUrl = this.baseUrl.replace(/\/$/, '');
      console.log('Base URL:', this.baseUrl); // Debug
    },
    
    
  }
}
</script>

<style>
    @media (max-width: 600px) {
      body { font-size: 14px; max-width: 100vw;
    overflow-x: hidden; }
      .bogiki-linktree { padding: 4px 1px 4px 1px;
    gap: 2px;
    max-width: 100vw;
    width: 100vw;
    overflow-x: hidden;}
      .main-btn { gap: 2px; border-radius: 10px; margin: 8px 0; font-size: 0.9rem; padding: 10px 8px; width: 250px; }
      .btn-icon { width: 14px; height: 14px; }
      .shop-now-btn {
        padding: 6px 10px;
        border-radius: 12px;
        font-size: 0.9rem;
      }
      .avatar-circle { width: 50px; height: 50px; }
      .avatar-img { width: 100%; height: 100%; }
      .brand { font-size: 0.9rem; }
      .section-title, .product-title { font-size: 1.5rem; margin: 4px 0 2px 0; }
      .social-list { gap: 4px; flex-wrap: nowrap; overflow-x: auto; }
      .social-btn { width: 18px; height: 18px; }
      .social-btn img { width: 10px; height: 10px; }
      .product-section { margin: 0 0 10px 0; }
      
    .footer { padding: 12px 0 8px 0; }
    .footer-inner { gap: 2px; }
.shop-now-wrapper-mobile {
  width: 100%;
  display: flex;
  justify-content: center;
  grid-column: 1 / -1;
  margin-top: 20px; /* Cố định 20px cho mobile */
}
.name-socal {
      font-weight: normal; 
      font-size: 16px;
    }
      .card {
        min-height: 60px;
        border-radius: 4px;
        width: 100%;
        max-width: 100%;
        margin: 0;
        box-sizing: border-box;
        padding: 2px;
      }
      .card-img-top {
        height: 48px;
        border-radius: 4px 4px 0 0;
        width: 100%;
        object-fit: cover;
      }
      .product-name {
        font-size: 0.75rem;
        margin: 1px 0 1px 0;
      }
      .product-section{
        margin: 0 0 10px 0;
      }
      .product-price {
        font-size: 0.75rem;
      }
  
      .footer-logo { width: 30px; }
      .footer-inner { gap: 4px; }
      .footer-text { font-size: 0.85rem; }
    }
    :root {
      --bg: #faf9f6;
      --card: #ffffff;
      --text: #1a1a1a;
      --brand: #6b8ed8ff;
      --accent: #e75480;
      --ring: rgba(37, 99, 235, .25);
      --shadow-soft: 0 4px 20px rgba(0,0,0,.08);
      --shadow-hover: 0 10px 28px rgba(0,0,0,.12);
      --radius-lg: 28px;
      --radius-xl: 36px;
      --container-w: 760px;
      --gap: 22px;
      --space: clamp(18px, 2.6vw, 28px);
    }

    * { box-sizing: border-box; }
    html, body { height: 100%; }

    body {
        /* font-family: 'Comic Neue', cursive; */
        font-weight: 400;
        background: #fffef3;
        color: #4b4040ff;
      }
    /* Container */
    .bogiki-linktree {
      min-height: 100dvh;
      max-width: var(--container-w);
      margin: 0 auto;
      padding: calc(var(--space) * 1.5) var(--space) calc(var(--space) * 1.2);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: calc(var(--space) * 0.8);
    }
   

    /* Shop button */
    .shop-now-btn {
      display: inline-block;
      padding: 16px 38px;
      border: 3px solid #818080;
      border-radius: 40px;
      background: #fff;
      font-weight: 800;
      font-size: 1.18rem;
      letter-spacing: .04em;
      text-decoration: none;
      transition: background .18s, color .18s, box-shadow .18s;
      box-shadow: 0 2px 12px rgba(37,99,235,0.07);
      text-align: center;
    }
    .shop-now-btn:hover {
      background: #eb25b0ff;
      border: 3px solid #eb25b0ff;
      color: #fff;
      box-shadow: 0 6px 24px rgba(37,99,235,0.13);
    }
    .product-link {
      text-decoration: none;   /* bỏ gạch chân */
      color: inherit;          /* giữ nguyên màu chữ như trong div */
      display: block;          /* để toàn bộ card clickable */
    }
    

    /* Profile */
    .profile { text-align: center; }
    .avatar-circle {
      width: 180px;
      height: 180px;
      border-radius: 50%;
      background: transparent;
      display: flex;
      align-items: center;
      justify-content: center;
      /* box-shadow: 0 4px 20px rgba(0,0,0,0.08); */
      margin: 0 auto var(--gap);
      overflow: hidden;
    }
    .avatar-img {
      width: 70%;
      height: 70%;
      object-fit: cover;
      border-radius: 50%;
      background: transparent;
      border: 1px solid #000000;
      display: block;
    }
    .brand {
      /* font-family: Georgia, "Times New Roman", serif; */
      font-weight: 600;
      font-size: clamp(2rem, 4vw, 1.5rem);
      letter-spacing: .2px;
      margin: 0;
    }
    .link-icon {
      margin-top: -43px;
    }

    /* Section title */
    .section-title {
      width: 100%;
      color: var(--brand);
      font-weight: auto;
      text-align: center;
      font-size: clamp(1.9rem, 2.4vw, 1.35rem);
      letter-spacing: .06em;
      margin: calc(var(--gap) * 0.6) 0 .2rem;
      text-transform: uppercase;
    }
    .name-socal {
      font-weight: normal; 
      font-size: 1.2rem;
    }

    /* Socials */
    .social-list {
      width: 100%;
      display: flex;
      justify-content: center;
      gap: clamp(8px, 1.5vw, 15px);
      flex-wrap: nowrap;
      overflow-x: auto;
    }
    
  .social-btn {
    /* background: var(--card); */
    border-radius: 50%;
    width: 70px;
    height: 70px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform .18s, box-shadow .18s, outline-color .18s;
    outline: none;
    border: none;
    padding: 0;
    margin: 0 8px;
}
.avatar-footer {
  width: 4%;
  height: 4%;
  border-radius: 50%;
  object-fit: cover;
  background: transparent;
  border: 1px solid #000000;
  display: block;
}
.email-footer {
  font-size: 1.0rem;
  margin: 0;
  text-align: center;
}

    .social-btn:hover { transform: translateY(-3px) scale(1.04);  }
    .social-btn:focus-visible { outline: 4px solid var(--ring); }
    .social-btn img.icon-connect {
    width: 55px;
    height: 55px;
    border-radius: 50%;
    border: none;
    background: transparent;
    outline: none;
    object-fit: cover;
    box-shadow: none;
}
.sub-title {
  display: block;
  font-size: 0.9rem;
  color: #444;
  font-weight: 400;
  margin-top: -8px;
  margin-bottom: -30px;
  letter-spacing: 0.01em;
}

    /* Main CTAs */
    .main-btn {
      width: 500px;
      height: 90px;
      display: flex;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      gap: 14px;
      text-decoration: none;
      padding: clamp(0px, 3.2vw, 32px) clamp(10px, 3vw, 30px);
      margin: 20px 0;
      background: #ffe6ec;
      color: var(--text);
      font-weight: 800;
      font-size: clamp(1.05rem, 2.6vw, 1.45rem);
      border-radius: var(--radius-xl);
      box-shadow: var(--shadow-soft);
      letter-spacing: .03em;
      transition: transform .18s ease, box-shadow .18s ease, background .18s ease, color .18s ease;
      will-change: transform;
    }
    .main-btn:hover {
      font-size: clamp(1.1rem, 2.7vw, 1.5rem); 
      background: #ffeefdff;
      color: #725858ff;
      transform: translateY(-2px) scale(1.06); /* tăng scale để to ra hơn */
      box-shadow: var(--shadow-hover);
      /* border: 2.5px solid #fac2c2; */
      transition: transform .18s ease, box-shadow .18s ease, background .18s ease, color .18s ease;
    }
    .h2-title{
      font-size:30px;
      font-weight: 700;
    }
    
    .main-btn:active { transform: translateY(0); }
    .btn-icon {
        width: clamp(26px, 3.8vw, 45px);
        height: clamp(26px, 3.8vw, 45px);
        flex: 0 0 auto;
        border-radius: 50%;
        object-fit: cover;
        background: transparent;
        border: none;
        outline: none;
        display: inline-block;
        vertical-align: middle;
        margin-right: 12px;
        flex: 0 0 auto;
        margin-right: -2px;
      }
      .main-btn span {
        flex: 1;
        text-align: center; /* căn giữa text */
        display: block;
      }

    /* Product grid */
    .product-section { width: 100%; }
    
    .h3-title {
      text-align: center;
      /* font-weight: bolder; */
    }
    .product-list {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: clamp(16px, 3.2vw, 28px);
    
    }
    .shop-now-wrapper {
  grid-column: 1 / -1;
  display: flex;
  justify-content: center;
  margin-top: 16px; /* chỉ cần ít thôi */
}

    .card {
      background: var(--card);
      border-radius: 16px;
      box-shadow: var(--shadow-soft);
      display: flex;
      flex-direction: column;
      align-items: center;
      transition: transform .18s ease, box-shadow .18s ease;
      border: none !important;         /* Xóa viền Bootstrap */
      box-shadow: none !important;     /* Xóa bóng viền nếu có */
      background: transparent !important;  /* Nền trong suốt */
    }
    .card:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }
    .card-img-top {
    border-radius: 16px 16px 0 0;
    }
    .product-name {
        font-weight: 300;
        font-size: clamp(1rem, 2.2vw, 1.2rem);
        text-align: center;
        margin: 6px 6px 2px;
        display: -webkit-box;
        -webkit-line-clamp: 1;      /* tối đa 2 dòng */
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.2em;         /* khoảng cách dòng */
        
        /* thêm để giữ đúng 2 dòng luôn */
        /* min-height: calc(1.2em * 2);  chiều cao bằng 2 dòng */
      }
    .product-price {
      
      font-weight: 600;
      text-align: center;
      font-size: clamp(1.05rem, 2.4vw, 1.3rem);
    }

    /* Shop now wrapper: căn giữa và chiếm toàn bộ chiều ngang */
    .shop-now-wrapper {
      width: 100%;
      display: flex;
      justify-content: center;
      grid-column: 1 / -1;
      margin-top: 50px;
    }

    /* Footer */
    .footer {
      width: 100%;
      background: transparent;
      padding: 36px 0 18px 0;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
    }
    .footer-inner {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }
    .footer-logo { width: 120px; height: auto; margin-bottom: 8px; }
    .footer-text {
      color: #888;
      font-size: 1rem;
      text-align: center;
    }
    .product-list.horizontal-scroll {
  display: flex !important;
  flex-direction: row;
  gap: 30px;
  overflow-x: auto;
  padding-bottom: 12px;
  scrollbar-width: thin;
  scrollbar-color: #e75480 #faf9f6;
}
.product-list.horizontal-scroll::-webkit-scrollbar {
  height: 8px;
}
.product-list.horizontal-scroll::-webkit-scrollbar-thumb {
  background: #e75480;
  border-radius: 8px;
}
.product-list.horizontal-scroll::-webkit-scrollbar-track {
  background: #faf9f6;
  border-radius: 8px;
}
.product-list.horizontal-scroll .product-link {
  min-width: 240px;
  max-width: 260px;
  flex: 0 0 auto;
}
.product-list.horizontal-scroll .card {
  width: 105%;
}
    
    /* Animations */
       /* Responsive: all mobile under 820px */

.product-list-btn {
  display: flex;
  flex-direction: column;
  gap: 22px;
  width: 100%;
  align-items: center;
}
.btn-layout2 {
  display: flex;
  align-items: center;
  background: #f7ccd6;
  border-radius: 40px;
  padding: 18px 32px;
  width: 100%;
  max-width: 520px;
  text-decoration: none;
  color: #222;
  box-shadow: 0 2px 12px rgba(37,99,235,0.07);
  transition: background .18s, box-shadow .18s;
  font-weight: 600;
}
.btn-layout2:hover {
  font-size: clamp(1.1rem, 2.7vw, 1.1rem); 
  background: #f7ccd6;
  color: #725858ff;
  transform: translateY(-2px) scale(1.06); /* tăng scale để to ra hơn */
  box-shadow: var(--shadow-hover);
  /* border: 2.5px solid #fac2c2; */
  transition: transform .18s ease, box-shadow .18s ease, background .18s ease, color .18s ease;
}
.btn-layout2-img {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 18px;
  background: #fff;
  border: 2px solid #fff;
}
.btn-layout2-content {
  /* display: flex; */
  flex-direction: column;
  justify-content: center;
}
.btn-layout2-title {
  font-size: 1.25rem;
  font-weight: normal;
}
.btn-layout2-sub {
  font-size: 0.9rem;
  /* color: #fff; */
  font-weight: normal;
  opacity: 0.85;
}
@media (max-width: 600px) {
  .btn-layout2 {
    padding: 12px 10px;
    font-size: 1rem;
    border-radius: 28px;
    max-width: 98vw;
  }
  .btn-layout2-img {
    width: 48px;
    height: 48px;
    margin-right: 12px;
  }
  .btn-layout2-title {
    font-size: 1.05rem;
  }
  .btn-layout2-sub {
    font-size: 0.85rem;
  }
}
@media (max-width: 820px) {
  body { font-size: 16.5px; }
  .bogiki-linktree { padding: 10px 8px 20px; max-width: 100vw; gap: 12px; }
  .main-btn { gap: 10px; border-radius: 18px; margin: 12px auto; width: 300px;height:55px;}
  .btn-icon { width: 32px; height: 32px; }
  .shop-now-btn {
    padding: 10px 22px;
    border: 2px solid #d0d8e9;
    border-radius: 28px;
    font-size: 1rem;
    box-shadow: 0 1px 6px rgba(37,99,235,0.07);
  }
   .h2-title{
      font-size:25px;
      font-weight: 550;
    }
    .name-socal {
      font-weight: normal; 
      font-size: 16px;
    }
    .product-list.horizontal-scroll .card {
      width: 80%;
    }
    .product-list.horizontal-scroll {
      gap: 0;
    }

    .btn-layout2 {
    padding: 12px 10px;
    font-size: 1rem;
    border-radius: 28px;
    max-width: 98vw;
  }
  .btn-layout2-img {
    width: 48px;
    height: 48px;
    margin-right: 12px;
  }
  .btn-layout2-title {
    font-size: 1.05rem;
  }
  .btn-layout2-sub {
    font-size: 0.85rem;
  }
  .shop-now-btn:hover {
    background: #f8f8f8;
    color: #fff;
    box-shadow: 0 4px 16px rgba(37,99,235,0.13);
  }
  
  .social-btn img.icon-connect {
    width: 45px;
    height: 45px;
    border-radius: 50%;
    border: none;
    background: transparent;
    outline: none;
    object-fit: cover;
    box-shadow: none;
}
  .link-icon {
      margin-top: -24px;
    }
.sub-title {
  font-size: 0.75rem;
  color: #444;
  font-weight: 400;
  margin-top: -6px;
  margin-bottom: -30px;
  letter-spacing: 0.01em;
}
 .avatar-footer {
  width: 20%;
  height: 20%;
  border-radius: 50%;
  object-fit: cover;
  background: transparent;
  border: 1px solid #000000;
  display: block;
}
.email-footer {
  font-size: 20px;
  margin: 0;
  text-align: center;
}
  .avatar-circle { width: 120px; height: 120px; }
  .avatar-img { width: 70%; height: 70%; }
  .brand { font-size: 1.5rem; }
  .section-title, .product-title { font-size: 1.1rem; margin: 12px 0 6px; }
  .social-list { gap: 12px; flex-wrap: nowrap; overflow-x: auto; }
  .social-btn { width: 55px; height: 55px; }
  .social-btn img { width: 40px; height: 40px; }
  .product-list { grid-template-columns: 0.5fr 0.5fr; }
  .card { width: 100%;
  overflow: hidden;
  display: flex; }
  .card-img-top  { width: 100%; height: 100%; display: block; flex: 1 0 0;}
  .product-name  { font-size: 1rem; margin: 4px 0 2px;   }
  
  .product-price { font-size: 1.05rem; }
  
}

@keyframes floatIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
.bogiki-linktree > * { animation: floatIn .5s ease both; }
.bogiki-linktree > *:nth-child(1) { animation-delay: .02s; }
.bogiki-linktree > *:nth-child(2) { animation-delay: .06s; }
.bogiki-linktree > *:nth-child(3) { animation-delay: .1s; }
.bogiki-linktree > *:nth-child(4) { animation-delay: .14s; }
.bogiki-linktree > *:nth-child(5) { animation-delay: .18s; }
</style>