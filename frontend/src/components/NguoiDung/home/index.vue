<template>
<div class="bogiki-linktree">
    <!-- Avatar & Name -->
    <div class="profile">
      <div class="avatar-circle">
        <img class="avatar-img" src="https://www.hngallery.com.my/image/hngallery/image/data/yqBiBGII1595518895.jpg" alt="Avatar" />
        </div>
      <h1 class="brand">Bogiki Coloring</h1>
    </div>

    <!-- Social Icons -->
    <div class="section-title">Connect with us</div>
    <div class="social-list">
      <a href="#" class="social-btn" aria-label="Facebook"><img src="https://img.icons8.com/color/96/000000/facebook.png" alt="Facebook" /></a>
      <a href="#" class="social-btn" aria-label="Instagram"><img src="https://img.icons8.com/color/96/000000/instagram-new.png" alt="Instagram" /></a>
      <a href="#" class="social-btn" aria-label="Pinterest"><img src="https://img.icons8.com/color/96/000000/pinterest--v1.png" alt="Pinterest" /></a>
      <a href="#" class="social-btn" aria-label="YouTube"><img src="https://img.icons8.com/color/96/000000/youtube-play.png" alt="YouTube" /></a>
      <a href="#" class="social-btn" aria-label="TikTok"><img src="https://img.icons8.com/color/96/000000/tiktok--v1.png" alt="TikTok" /></a>
     <a href="#" class="social-btn" aria-label="Threads">
  <img src="https://cdn.jsdelivr.net/gh/simple-icons/simple-icons/icons/threads.svg" alt="Threads" style="background:#fff; border-radius:50%;" />
</a>
      <a href="#" class="social-btn" aria-label="Reddit"><img src="https://img.icons8.com/color/96/000000/reddit--v1.png" alt="Reddit" /></a>
    </div>

    <!-- Shop Now -->
    <div class="section-title">Shop now on</div>
    <a class="main-btn" href="https://amazon.com" target="_blank" rel="noopener">
      <img class="btn-icon" src="https://img.icons8.com/color/96/000000/amazon.png" alt="Amazon" />
      Amazon
    </a>
    <a class="main-btn" href="https://bogiki.com" target="_blank" rel="noopener">
      <img class="btn-icon" src="https://img.icons8.com/color/96/000000/internet--v1.png" alt="Website" />
      Bogiki.com
    </a>

    <!-- Community -->
    <div class="section-title">Connect with me</div>
    <a class="main-btn" href="#" target="_blank" rel="noopener">Bogiki Coloring Community</a>
    <a class="main-btn" href="#" target="_blank" rel="noopener">Free Digital Coloring Pages</a>

    <!-- Product Section: For từng loại sản phẩm -->
    <div v-for="type in productTypes" :key="type.id" class="product-section">
      <div class="product-title">{{ type.ten_loai }}</div>
      <div style="margin-bottom: 550px;" class="product-list ">
        <a v-for="product in type.products" :key="product.id" :href="product.duong_dan_ngoai" target="_blank" class="product-link">
          <div class="card">
            <img :src="product.anh_dai_dien" class="card-img-top" alt="...">
            <div class="card-body">
              <div class="product-name">{{ product.ten_san_pham }}</div>
              <div class="product-price">${{ product.gia_mac_dinh }}</div>
            </div>
          </div>
        </a>
      </div>
      <div class="shop-now-wrapper" style="width:100%; display:flex; justify-content:center; ">
        <a href="#" class="shop-now-btn">SHOP NOW</a>
      </div>
    </div>
  </div>
  <footer class="footer">
  <div class="footer-inner">
    <img src="https://www.hngallery.com.my/image/hngallery/image/data/yqBiBGII1595518895.jpg" alt="Bogiki Logo" class="footer-logo" />
  </div>
</footer>
</template>
<script>
import axios from 'axios';
export default {
  data() {
    return {
      productTypes: [] // [{id, ten_loai, products: []}]
    };
  },
  async mounted() {
    this.loadAllProductTypes();
    // Gọi API đếm lượt truy cập trang home
    try {
      await axios.get('http://127.0.0.1:8000/api/frontend-page-visit/?page=home');
    } catch (err) {
      // Có thể log lỗi hoặc bỏ qua
    }
  },
  methods: {
    async loadAllProductTypes() {
      try {
        // Lấy danh sách loại sản phẩm
        const resType = await axios.get('http://127.0.0.1:8000/products/type/list/');
        const types = resType.data.filter(type => type.tinh_trang == 1);
        // For từng loại, lấy sản phẩm theo id loại
        const promises = types.map(async (type) => {
          const resProduct = await axios.get(`http://127.0.0.1:8000/products/type/${type.id}/`);
          return {
            ...type,
            products: resProduct.data.status ? resProduct.data.data : []
          };
        });
        this.productTypes = await Promise.all(promises);
      } catch (err) {
        this.productTypes = [];
      }
    }
  }
}
</script>
 <style>
    @media (max-width: 600px) {
      body { font-size: 14px; }
      .bogiki-linktree { padding: 4px 1px 8px 1px; gap: 4px; }
      .main-btn { gap: 4px; border-radius: 10px; margin-bottom: 4px; font-size: 0.9rem; padding: 8px 10px; }
      .btn-icon { width: 14px; height: 14px; }
      .shop-now-btn {
        padding: 6px 10px;
        border-radius: 12px;
        font-size: 0.9rem;
      }
      .avatar-circle { width: 50px; height: 50px; }
      .avatar-img { width: 30px; height: 30px; }
      .brand { font-size: 0.9rem; }
      .section-title, .product-title { font-size: 0.9rem; margin: 6px 0 2px 0; }
      .social-list { gap: 2px; }
      .social-btn { width: 18px; height: 18px; }
      .social-btn img { width: 10px; height: 10px; }
      .product-list {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 4px;
        padding: 0;
      }
      .shop-now-wrapper {  margin-top: 500px;}

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
      font-weight: 800;
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
      display: -webkit-box;       /* tạo hộp linh hoạt */
      -webkit-line-clamp: 1;      /* giới hạn 2 dòng */
      -webkit-box-orient: vertical;
      overflow: hidden;           /* ẩn phần dư */
      text-overflow: ellipsis;    /* dấu … nếu quá dài */
      line-height: 1.2em;         /* chỉnh khoảng cách dòng */
    }
    .product-price {
      color: var(--accent);
      font-weight: 800;
      text-align: center;
      font-size: clamp(1.05rem, 2.4vw, 1.3rem);
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
  .product-name  { font-size: 1rem; margin: 4px 0 2px; }
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