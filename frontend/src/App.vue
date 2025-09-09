<template>
  <component :is="layout">
      <router-view></router-view>
  </component>
</template>
<style>
@font-face {
  font-family: 'Handineat';
  /* Try multiple path resolutions to ensure bundlers/dev-servers pick it up */
  src: url('./assets/fonts/Handineat.otf') format('opentype');
  /* Fallback for environments resolving from /src root */
  src: url('/src/assets/fonts/Handineat.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}
.section-title,
.product-title,
.shop-now-btn,
.text-decoration-none.fw-bold.fs-5.text-darkz {
  font-family: 'Handineat', sans-serif !important;
}
</style>

<script>
const default_layout = "default";
export default {
  computed: {
    layout() {
      return (this.$route.meta.layout || default_layout) + "-layout";
    },
  },
};
</script>
