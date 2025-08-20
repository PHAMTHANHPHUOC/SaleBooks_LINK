<template >
   <div class="card">
    <div class="card-header">
        <div class="row">
            <div class="col">
        <h3 class="card-title">Danh sách sản phẩm</h3>
            </div>
            <div class="col text-end"><button class="btn btn-info">Thêm Sản Phẩm</button></div>
        </div>
    </div>
    <div class="card-body">
        <div class="table-responsive">
            <table class="table table-bordered" >
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Tên sản phẩm</th>
                        <th>Đường Dẫn Ngoại</th>
                        <th>Giá</th>
                        <th>Ảnh</th>
                        <th>Loại Sản Phẩm</th>
                        <th>action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(v, k) in list_san_pham" :key="k">
                        <td>{{ k+1 }}</td>
                        <td>{{ v.ten_san_pham }}</td>
                        <td>{{ v.duong_dan_ngoai }}</td>
                        <td>${{ v.gia_mac_dinh }}</td>
                        <td>{{ v.anh_dai_dien }}</td>
                        <td>{{ v.loai_san_pham_id }}</td>
                         <td class="text-center align-middle text-nowrap">
                            <button class="btn btn-info me-2" data-bs-toggle="modal" v-on:click="Object.assign(edit_loai_san_pham, v)" data-bs-target="#editModal">Cập Nhật</button>
                            <button class="btn btn-danger" data-bs-toggle="modal" v-on:click="Object.assign(delete_loai_san_pham, v)" data-bs-target="#deleteModal">Xóa Bỏ</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
   </div>
</template>
<script>
import axios from "axios";
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster({ position: "top-right" });
export default {
  data() {
    return {
      create_loai_san_pham: {},
      edit_loai_san_pham: {},
      delete_loai_san_pham: {},
      list_san_pham: [],
      loading: false,
      debug_mode: true, // Bật debug mode để kiểm tra
      api_response: null
    };
  },
  mounted() {
    this.loadSanPham();
  },
  methods: {
    loadSanPham() {
      this.loading = true;
      axios
        .get("http://127.0.0.1:8000/products/data/")
        .then((res) => {
          console.log("API Response:", res.data); 
          this.api_response = JSON.stringify(res.data);
          
          // Kiểm tra cấu trúc response
          if (res.data && res.data.data) {
            this.list_san_pham = res.data.data;
          } else if (Array.isArray(res.data)) {
            // Trường hợp API trả về trực tiếp array
            this.list_san_pham = res.data;
          } else {
            console.error("Unexpected response structure:", res.data);
            this.list_san_pham = [];
          }
          
          if (res.data.status === 0) {
            toaster.error(res.data.message);
          }
        })
        .catch((error) => {
          console.error("API Error:", error);
          this.list_san_pham = [];
          if (toaster) {
            toaster.error("Lỗi khi tải dữ liệu: " + error.message);
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    // createLoaiSanPham() {
    //   if (!this.create_loai_san_pham.ten_loai) {
    //     toaster.error("Vui lòng nhập tên sản phẩm");
    //     return;
    //   }
      
    //   axios
    //     .post(
    //       "http://127.0.0.1:8000/products/type/create/",
    //       this.create_loai_san_pham
    //     )
    //     .then((res) => {
    //       if (res.data.status) {
    //         toaster.success(res.data.message);
    //         this.create_loai_san_pham = {};
    //         this.loadLoaiSanPham();
    //       } else {
    //         toaster.error(res.data.message);
    //       }
    //     })
    //     .catch((res) => {
    //       if (res.response && res.response.data && res.response.data.errors) {
    //         const errors = Object.values(res.response.data.errors);
    //         errors.forEach((v) => {
    //           toaster.error(v[0]);
    //         });
    //       } else {
    //         toaster.error("Có lỗi xảy ra khi thêm mới");
    //       }
    //     });
    // },
    
    // capNhatLoaiSanPham() {
    //   axios
    //     .post(`http://127.0.0.1:8000/products/type/update/${this.edit_loai_san_pham.id}/`, this.edit_loai_san_pham)
    //     .then((res) => {
    //       if (res.data.status) {
    //         toaster.success(res.data.message);
    //         this.loadLoaiSanPham();

    //       } else {
    //         toaster.error(res.data.message);
    //       }
    //     })
    //     .catch((res) => {
    //       if (res.response && res.response.data && res.response.data.errors) {
    //         const errors = Object.values(res.response.data.errors);
    //         errors.forEach((v) => {
    //           toaster.error(v[0]);
    //         });
    //       } else {
    //         toaster.error("Có lỗi xảy ra khi cập nhật");
    //       }
    //     });
    // },
    
    // xoaLoaiSanPham() {
    //   axios
    //     .post(
    //       `http://127.0.0.1:8000/products/type/delete/${this.delete_loai_san_pham.id}/`,
    //       this.delete_loai_san_pham
    //     )
    //     .then((res) => {
    //       if (res.data.status) {
    //         toaster.success(res.data.message);
    //         this.loadLoaiSanPham();

    //       } else {
    //         toaster.error(res.data.message);
    //       }
    //     })
    //     .catch((res) => {
    //       if (res.response && res.response.data && res.response.data.errors) {
    //         const errors = Object.values(res.response.data.errors);
    //         errors.forEach((v) => {
    //           toaster.error(v[0]);
    //         });
    //       } else {
    //         toaster.error("Có lỗi xảy ra khi xóa");
    //       }
    //     });
    // },
    
    
  },
};
</script>
<style >
    
</style>