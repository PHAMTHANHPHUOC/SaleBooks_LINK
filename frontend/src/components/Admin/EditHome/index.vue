<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">Sắp xếp sản phẩm (Admin)</h2>

    <draggable v-model="products" item-key="id" class="grid grid-cols-4 gap-4" @end="saveOrder">
      <template #item="{ element }">
        <div class="border rounded p-2 shadow text-center bg-white">
          <img :src="getFullImageUrl(element.anh_dai_dien)" class="w-full h-32 object-cover mb-2" />
          <p class="font-semibold">{{ element.ten_san_pham }}</p>
          <p class="text-sm text-gray-500">{{ element.gia_mac_dinh }}</p>
        </div>
      </template>
    </draggable>
  </div>
</template>

<script>
import draggable from "vuedraggable";
import axios from "axios";

export default {
  components: { draggable },
  data() {
    return {
      products: []
    };
  },
  async mounted() {
    const res = await axios.get("/api/products/type/list/");
    this.products = res.data;
  },
  methods: {
    getFullImageUrl(path) {
      return path ? `/media/${path}` : "/no-image.png";
    },
    async saveOrder() {
      const payload = this.products.map((item, index) => ({
        id: item.id,
        stt: index
      }));
      await axios.post("/api/update-order/", payload);
      alert("Đã lưu thứ tự!");
    }
  }
};
</script>
