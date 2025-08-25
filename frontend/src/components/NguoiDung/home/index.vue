<template>
<div class="bogiki-linktree">
    <!-- Avatar & Name -->
    <div class="profile">
      <div class="avatar-circle">
        <img class="avatar-img" src="../../../assets/images/TINY.jpg" alt="Avatar" />
        </div>
      <h1 class="brand">Tiny Daisy</h1>
    </div>

    <!-- Social Icons -->
    <div class="section-title">Connect with us</div>
    <div class="social-list">
      <a target="_blank" rel="noopener"  :href="list_link.Facebook" class="social-btn" aria-label="Facebook"><img src="https://img.icons8.com/color/96/000000/facebook.png" alt="Facebook" /></a>
      <a target="_blank" rel="noopener"  :href="list_link.Instagram" class="social-btn" aria-label="Instagram"><img src="https://img.icons8.com/color/96/000000/instagram-new.png" alt="Instagram" /></a>
      <a target="_blank" rel="noopener"  :href="list_link.YouTube" class="social-btn" aria-label="YouTube"><img src="https://img.icons8.com/color/96/000000/youtube-play.png" alt="YouTube" /></a>
      <a target="_blank" rel="noopener"  :href="list_link.TikTok" class="social-btn" aria-label="TikTok"><img src="https://img.icons8.com/color/96/000000/tiktok--v1.png" alt="TikTok" /></a>
    </div>

    <!-- Shop Now -->
    <div class="section-title">Shop now on</div>
    <a class="main-btn" :href="list_link.Amazon" target="_blank" rel="noopener">
      <img class="btn-icon" src="https://img.icons8.com/color/96/000000/amazon.png" alt="Amazon" />
      Amazon
    </a>
    <a class="main-btn" :href="list_link.Website" target="_blank" rel="noopener">
      <img class="btn-icon" src="https://img.icons8.com/color/96/000000/internet--v1.png" alt="Website" />
      tinydaisycoloring.com
    </a>

    <!-- Community -->
    <div class="section-title">Connect with me</div>
    <a class="main-btn" :href="list_link.Bogiki" target="_blank" rel="noopener">Bogiki Coloring Community</a>
    <a class="main-btn" :href="list_link.FreeDigital" target="_blank" rel="noopener">Free Digital Coloring Pages</a>

    <!-- Product Section: For từng loại sản phẩm -->
    <div v-for="type in productTypes" :key="type.id" class="product-section">
      <div class="product-title">{{ type.ten_loai }}</div>
      <div class="product-list">
        <a v-for="product in type.products" :key="product.id" :href="product.duong_dan_ngoai"  @click="handleClick(product.id)" target="_blank" class="product-link">
          <div class="card">
            <img :src="product.anh_dai_dien" class="card-img-top" alt="...">
            <div class="card-body">
              <div class="product-name">{{ product.ten_san_pham }}</div>
              <div class="product-price">${{ product.gia_mac_dinh }}</div>
            </div>
          </div>
        </a>
      </div>
      <!-- Enhanced calcMargin for multiple devices -->
      <div :style="{ marginTop: calcMargin(type.products.length) + 'px' }" class="shop-now-wrapper">
        <a target="_blank" rel="noopener" :href="type.link_danh_muc" class="shop-now-btn">SHOP NOW</a>
      </div>
    </div>
  </div>
  
  <footer class="footer">
    <div class="footer-inner">
      <img src="../../../assets/images/TINY.jpg" alt="Bogiki Logo" class="footer-logo" />
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
      list_link : [],
      windowHeight: window.innerHeight
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
    this.loadlink();
    this.loadAllProductTypes();
    try {
      await baseRequest.get('api/frontend-page-visit/?page=home');
    } catch (err) {
      // Handle error
    }
    window.addEventListener('resize', this.handleResize);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
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
    
    async handleClick(productId) {
      try {
        const res = await baseRequest.post(`san-pham/${productId}/click/`);
        console.log(res.data);
      } catch (error) {
        console.error("Lỗi khi gửi click:", error);
      }
    },
    loadlink() {
      baseRequest
        .get("api/links/")
        .then((res) => {
          if (res.data && res.data.data) {
            this.list_link = res.data.data;
          } else if (Array.isArray(res.data)) {
            this.list_link = res.data;
          } else {
            this.list_link = {};
          }
        })
        .catch(() => {
          this.list_link = {};
        });
    },
  }
}
</script>

<style>
    @media (max-width: 600px) {
      body { font-size: 14px; }
      .bogiki-linktree { padding: 4px 1px 4px 1px; gap: 2px; }
      .main-btn { gap: 2px; border-radius: 10px; margin-bottom: 2px; font-size: 0.9rem; padding: 6px 8px; }
      .btn-icon { width: 14px; height: 14px; }
      .shop-now-btn {
        padding: 6px 10px;
        border-radius: 12px;
        font-size: 0.9rem;
      }
      .avatar-circle { width: 50px; height: 50px; }
      .avatar-img { width: 30px; height: 30px; }
      .brand { font-size: 0.9rem; }
      .section-title, .product-title { font-size: 0.9rem; margin: 4px 0 2px 0; }
      .social-list { gap: 2px; }
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
        font-family: 'Comic Neue', cursive;
        font-weight: 400;
        background: #fff7fbff;
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
      border: 3px solid #2563eb;
      border-radius: 40px;
      background: #fff;
      color: #1a1a1a;
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
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
      margin: 0 auto var(--gap);
    }
    .avatar-img {
      width: 140px;
      height: 140px;
      object-fit: contain;
      border-radius: 50%;
      background: #fff;
      display: block;
    }
    .brand {
      font-family: Georgia, "Times New Roman", serif;
      font-weight: 800;
      font-size: clamp(2rem, 4vw, 3.2rem);
      letter-spacing: .2px;
      margin: 0;
    }

    /* Section title */
    .section-title {
      width: 100%;
      color: var(--brand);
      font-weight: auto;
      text-align: center;
      font-size: clamp(1.05rem, 2.4vw, 1.35rem);
      letter-spacing: .06em;
      margin: calc(var(--gap) * 0.6) 0 .2rem;
      text-transform: uppercase;
    }

    /* Socials */
    .social-list {
      width: 100%;
      display: flex;
      justify-content: center;
      gap: clamp(12px, 2vw, 22px);
      flex-wrap: wrap;
    }
    .social-btn {
      background: var(--card);
      border-radius: 999px;
      width: clamp(56px, 8vw, 72px);
      height: clamp(56px, 8vw, 72px);
      display: grid;
      place-items: center;
      box-shadow: var(--shadow-soft);
      transition: transform .18s ease, box-shadow .18s ease, outline-color .18s ease;
      outline: 0 solid transparent;
    }
    .social-btn:hover { transform: translateY(-3px) scale(1.04); box-shadow: var(--shadow-hover); }
    .social-btn:focus-visible { outline: 4px solid var(--ring); }
    .social-btn img { width: clamp(30px, 4.5vw, 40px); height: clamp(30px, 4.5vw, 40px); }

    /* Main CTAs */
    .main-btn {
      width: 100%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 14px;
      text-decoration: none;
      padding: clamp(18px, 2.8vw, 26px) clamp(18px, 3vw, 28px);
      background: var(--card);
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
      border: 2.5px solid #111;
      transition: transform .18s ease, box-shadow .18s ease, background .18s ease, color .18s ease;
    }
    .main-btn:active { transform: translateY(0); }
    .btn-icon { width: clamp(26px, 3.8vw, 34px); height: clamp(26px, 3.8vw, 34px); flex: 0 0 auto; }

    /* Product grid */
    .product-section { width: 100%; }
    .product-title {
      color: var(--brand);
      text-align: center;
      font-weight: 800;
      letter-spacing: .05em;
      font-size: clamp(1.25rem, 3vw, 1.9rem);
      margin: calc(var(--gap) * .9) 0 calc(var(--gap) * .6);
      text-transform: uppercase;
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
    }
    .card:hover { transform: translateY(-6px); box-shadow: var(--shadow-hover); }
    .card-img-top {
    border-radius: 16px 16px 0 0;
    }
    .product-name {
        font-weight: 700;
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
      color: var(--accent);
      font-weight: 800;
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
    /* Animations */
       /* Responsive: all mobile under 820px */
@media (max-width: 820px) {
  body { font-size: 16.5px; }
  .bogiki-linktree { padding: 10px 8px 20px; max-width: 100vw; gap: 12px; }
  .main-btn { gap: 10px; border-radius: 18px; margin: 0 auto 8px; }
  .btn-icon { width: 22px; height: 22px; }
  .shop-now-btn {
    padding: 10px 22px;
    border: 2px solid #2563eb;
    border-radius: 28px;
    font-size: 1rem;
    box-shadow: 0 1px 6px rgba(37,99,235,0.07);
  }
  .shop-now-btn:hover {
    background: #2563eb;
    color: #fff;
    box-shadow: 0 4px 16px rgba(37,99,235,0.13);
  }

  .avatar-circle { width: 120px; height: 120px; }
  .avatar-img { width: 90px; height: 90px; }
  .brand { font-size: 1.5rem; }
  .section-title, .product-title { font-size: 1.1rem; margin: 12px 0 6px; }
  .social-list { gap: 8px; }
  .social-btn { width: 38px; height: 38px; }
  .social-btn img { width: 22px; height: 22px; }
  .product-list { grid-template-columns: 1fr 1fr; }
  .card { width: 100%;
  overflow: hidden;
  display: flex; }
  .card-img-top  { width: 100%; height: 100%; display: block; flex: 1 0 0;}
  .product-name  { font-size: 1rem; margin: 4px 0 2px;   }
  
  .product-price { font-size: 1.05rem; }
}

/* Subtle animation */
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