<template >
   <div class="card">
    <div class="card-header">
        <div class="row">
            <div class="col">
        <h3 class="card-title">Danh sách sản phẩm</h3>
            </div>
            <div class="col text-end"><button class="btn btn-info" data-bs-toggle="modal"
                            data-bs-target="#exampleModal" >Thêm Sản Phẩm</button></div>
            <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">
                            Thêm Mới Sản Phẩm
                        </h1>
                    </div>
                    <div class="modal-body">
                        <div class="mb-2">
                            <label class="form-label">Tên Sản Phẩm</label>
                            <input v-model="create_san_pham.ten_san_pham" type="text" class="form-control" />
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Đường dẫn ngoài</label>
                            <input v-model="create_san_pham.duong_dan_ngoai" type="email" class="form-control" />
                        </div>
                 
                        <div class="mb-2">
                            <label class="form-label">Giá Tiền</label>
                            <input v-model="create_san_pham.gia_mac_dinh" type="text" class="form-control" />
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Ảnh bìa</label>
                            <input v-model="create_san_pham.anh_dai_dien" type="text" class="form-control" />
                        </div>
                        <label class="form-lable mt-2"> Tình Trạng</label>
                          <select
                            v-model="create_san_pham.tinh_trang"
                            class="form-control"
                          >
                            <option value="1">Hiển Thị</option>
                            <option value="0">Tạm Dừng</option>
                          </select>

                        <div class="mb-2">
                            <label>Loại Sản Phẩm</label>
                            <select v-model="create_san_pham.loai_san_pham" class="form-control mt-2">
                                <template v-for="(v, k) in loaisanpham" :key="k">
                                    <option v-bind:value="v.id">{{ v.ten_loai }}</option>
                                </template>
                            </select>
                    </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button v-on:click="createSanPham()" class="btn btn-primary" data-bs-dismiss="modal">
                            Thêm Mới
                        </button>
                    </div>
                </div>
            </div>
        </div>
            <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">
                            Cập Nhật Sản Phẩm
                        </h1>
                    </div>
                    <div class="modal-body">
                        <div class="mb-2">
                            <label class="form-label">Tên Sản Phẩm</label>
                            <input v-model="edit_san_pham.ten_san_pham" type="text" class="form-control" />
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Đường dẫn ngoài</label>
                            <input v-model="edit_san_pham.duong_dan_ngoai" type="email" class="form-control" />
                        </div>
                      
                        <div class="mb-2">
                            <label class="form-label">Giá Tiền</label>
                            <input v-model="edit_san_pham.gia_mac_dinh" type="text" class="form-control" />
                        </div>
                        <div class="mb-2">
                            <label class="form-label">Ảnh bìa</label>
                            <input v-model="edit_san_pham.anh_dai_dien" type="text" class="form-control" />
                        </div>
                        <label class="form-lable mt-2"> Tình Trạng</label>
                          <select
                            v-model="edit_san_pham.tinh_trang"
                            class="form-control"
                          >
                            <option value="1">Hiển Thị</option>
                            <option value="0">Tạm Dừng</option>
                          </select>
                        <div class="mb-2">
                            <label>Loại Sản Phẩm</label>
                            <select v-model="edit_san_pham.loai_san_pham" class="form-control mt-2">
                                <template v-for="(v, k) in loaisanpham" :key="k">
                                    <option v-bind:value="v.id">{{ v.ten_loai }}</option>
                                </template>
                            </select>
                    </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button v-on:click="capNhatSanPham()" class="btn btn-primary" data-bs-dismiss="modal">
                            Cập Nhật </button>
                    </div>
                </div>
            </div>
        </div>
         <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="exampleModalLabel">
                            Xóa Sản Phẩm
                        </h1>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="alert alert-danger border-0 bg-danger alert-dismissible fade show py-2">
                            <div class="d-flex align-items-center">
                                <div class="font-35 text-white">
                                    <i class="bx bxs-message-square-x"></i>
                                </div>
                                <div class="ms-1">
                                    <h6 class="mb-1 text-white">
                                        Bạn chắc chắc xóa Sản Phẩm
                                        <b>{{ delete_san_pham.ten_san_pham }}</b> này chứ !!!
                                    </h6>
                                    <div class="text-white text-nowrap">
                                        <b>LƯU Ý !!!</b> Điều này không thể khôi phục khi ấn xác
                                        nhận
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button type="button" class="btn btn-danger" data-bs-dismiss="modal" v-on:click="xoaLoaiSanPham()">
                            Xác nhận
                        </button>
                    </div>
                </div>
            </div>
        </div>
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
                        <th>Tình Trạng</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(v, k) in list_san_pham" :key="k">
                        <td>{{ k+1 }}</td>
                        <td>{{ v.ten_san_pham }}</td>
                        <td>{{ v.duong_dan_ngoai }}</td>
                        <td>${{ v.gia_mac_dinh }}</td>
                        <td>{{ v.anh_dai_dien }}</td>
                        <td>{{ getLoaiSanPhamName(v.loai_san_pham) }}</td>
                        <td class="align-middle text-nowrap text-center">
                          <template v-if="v.tinh_trang == 1">
                            <button v-on:click="changeStatus(v)" class="btn btn-success w-100">Hiển Thị</button>
                          </template>
                          <template v-else-if="v.tinh_trang == 0">
                            <button v-on:click="changeStatus(v)" class="btn btn-danger w-100">Tạm Tắt</button>
                          </template>
                        </td>
                         <td class="text-center align-middle text-nowrap">
                            <button class="btn btn-info me-2" data-bs-toggle="modal" v-on:click="Object.assign(edit_san_pham, v)" data-bs-target="#editModal">Cập Nhật</button>
                            <button class="btn btn-danger" data-bs-toggle="modal" v-on:click="Object.assign(delete_san_pham, v)" data-bs-target="#deleteModal">Xóa Bỏ</button>
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
      create_san_pham: {},
      edit_san_pham: {},
      delete_san_pham: {},
      list_san_pham: [],
      loaisanpham: [], // Thêm mảng loại sản phẩm
      loading: false,
      debug_mode: true, // Bật debug mode để kiểm tra
      api_response: null
    };
  },
  mounted() {
    this.loadSanPham();
    this.loadLoaiSanPham();
  },
  methods: {
    loadLoaiSanPham() {
      axios
        .get("http://127.0.0.1:8000/products/type/list/")
        .then((res) => {
          if (res.data && res.data.data) {
            this.loaisanpham = res.data.data;
          } else if (Array.isArray(res.data)) {
            this.loaisanpham = res.data;
          } else {
            this.loaisanpham = [];
          }
        })
        .catch(() => {
          this.loaisanpham = [];
        });
    },
    changeStatus(value) {
      axios
        .post(
          "http://127.0.0.1:8000/products/change-status/",
          value
        )
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.loadSanPham();
            
          } else {
            toaster.error(res.data.message);
          }
        })
        .catch((res) => {
          if (res.response && res.response.data && res.response.data.errors) {
            const errors = Object.values(res.response.data.errors);
            errors.forEach((v) => {
              toaster.error(v[0]);
            });
          } else {
            toaster.error("Có lỗi xảy ra khi thay đổi trạng thái");
          }
        });
    },
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
    getLoaiSanPhamName(idLoaiSanPham) {
      const loai = this.loaisanpham.find(item => Number(item.id) === Number(idLoaiSanPham));
      return loai ? loai.ten_loai : 'N/A';
    },
    
    createSanPham() {
      if (!this.create_san_pham.ten_san_pham || this.create_san_pham.ten_san_pham.trim() === "") {
        toaster.error("Vui lòng nhập tên sản phẩm");
        return;
      }
      
      axios
        .post(
          "http://127.0.0.1:8000/products/create/",
          this.create_san_pham
        )
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.create_san_pham = {};
            this.loadSanPham();
          } else {
            toaster.error(res.data.message);
          }
        })
        .catch((res) => {
          if (res.response && res.response.data && res.response.data.errors) {
            const errors = Object.values(res.response.data.errors);
            errors.forEach((v) => {
              toaster.error(v[0]);
            });
          } else {
            toaster.error("Có lỗi xảy ra khi thêm mới");
          }
        });
    },
    
    capNhatSanPham() {
      axios
        .post(`http://127.0.0.1:8000/products/update/${this.edit_san_pham.id}/`, this.edit_san_pham)
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.loadSanPham();

          } else {
            toaster.error(res.data.message);
          }
        })
        .catch((res) => {
          if (res.response && res.response.data && res.response.data.errors) {
            const errors = Object.values(res.response.data.errors);
            errors.forEach((v) => {
              toaster.error(v[0]);
            });
          } else {
            toaster.error("Có lỗi xảy ra khi cập nhật");
          }
        });
    },
    
    xoaLoaiSanPham() {
      axios
        .post(
          `http://127.0.0.1:8000/products/delete/${this.delete_san_pham.id}/`,
          this.delete_san_pham
        )
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.loadSanPham();

          } else {
            toaster.error(res.data.message);
          }
        })
        .catch((res) => {
          if (res.response && res.response.data && res.response.data.errors) {
            const errors = Object.values(res.response.data.errors);
            errors.forEach((v) => {
              toaster.error(v[0]);
            });
          } else {
            toaster.error("Có lỗi xảy ra khi xóa");
          }
        });
    },
    
    
  },
};
</script>
<style >
    .section-title {
  width: 100%;
  color: #2563eb;
  font-weight: 700;
  text-align: center;
  font-size: clamp(1.15rem, 2.5vw, 1.5rem);
  letter-spacing: 0.04em;
  margin: 24px 0 10px 0;
  text-transform: uppercase;
  background: linear-gradient(90deg, #e0e7ff 0%, #fff 100%);
  border-radius: 12px;
  padding: 10px 0 8px 0;
  box-shadow: 0 2px 12px rgba(37,99,235,0.07);
  transition: background 0.2s, color 0.2s;
  position: relative;
  z-index: 1;
}

.section-title::after {
  content: "";
  display: block;
  margin: 8px auto 0 auto;
  width: 48px;
  height: 3px;
  border-radius: 2px;
  background: linear-gradient(90deg, #2563eb 0%, #e75480 100%);
  opacity: 0.7;
}

@media (max-width: 600px) {
  .section-title {
    font-size: 1rem;
    padding: 7px 0 6px 0;
    margin: 14px 0 6px 0;
  }
  .section-title::after {
    width: 32px;
    height: 2px;
    margin-top: 5px;
  }
}
.table td:nth-child(3) {
  max-width: 320px;      /* Giới hạn chiều rộng tối đa */
  white-space: nowrap;   /* Không xuống dòng */
  overflow: hidden;      /* Ẩn phần vượt quá */
  text-overflow: ellipsis; /* Hiển thị ... */
}
</style>