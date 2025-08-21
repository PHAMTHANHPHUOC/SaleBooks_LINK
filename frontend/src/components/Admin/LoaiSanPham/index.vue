<template>
  <div class="row" id="app">
    <div class="col-md-3">
      <div class="card">
        <div class="card-header mt-2">
          <h5><b> Thêm Mới Loại Sản Phẩm </b></h5>
        </div>
        <div class="card-body">
          <label class="form-lable">Tên Sản Phẩm</label>
          <input
            v-model="create_loai_san_pham.ten_loai"
            class="form-control mt-1"
            type="text"
          />
          <label class="form-lable">Link Danh Mục</label>
          <input
            v-model="create_loai_san_pham.link_danh_muc"
            class="form-control mt-1"
            type="text"
          />
  
          <label class="form-lable mt-2"> Tình Trạng</label>
          <select
            v-model="create_loai_san_pham.tinh_trang"
            class="form-control"
          >
            <option value="1">Hiển Thị</option>
            <option value="0">Tạm Dừng</option>
          </select>
        </div>
        <div class="card-footer text-end">
          <button @click="createLoaiSanPham()" class="btn btn-primary">
            Thêm Mới Loại Sản Phẩm
          </button>
        </div>
      </div>
    </div>
    <div class="col-md-9">
      <div class="card">
        <div
          class="card-header mt-2 d-flex justify-content-between align-items-center"
        >
          <h5><b>Danh Sách Loại Sản Phẩm</b></h5>
        </div>
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-bordered">
              <thead>
                <tr>
                  <th class="text-center align-middle text-nowrap">#</th>
                  <th class="text-center align-middle text-nowrap">
                    Tên Loại Sản Phẩm
                  </th>
                  <th class="text-center align-middle text-nowrap">
                    Link Danh Mục
                  </th>
                  
                  <th class="text-center align-middle text-nowrap">
                    Tình Trạng
                  </th>
                  <th class="text-center align-middle text-nowrap">Action</th>
                </tr>
              </thead>
              <tbody>
                <!-- Kiểm tra nếu list_loai_san_pham tồn tại và có dữ liệu -->
                <tr v-if="!list_loai_san_pham || list_loai_san_pham.length === 0">
                  <td colspan="5" class="text-center">
                    <span v-if="loading">Đang tải dữ liệu...</span>
                    <span v-else>Không có dữ liệu</span>
                  </td>
                </tr>
                <tr v-else v-for="(v, k) in list_loai_san_pham" :key="k">
                  <th class="text-center align-middle text-nowrap">{{ k + 1 }}</th>
                  <td class="align-middle text-nowrap">{{ v.ten_loai }}</td>
                  <td class="align-middle text-nowrap">  {{ v.link_danh_muc }}</td>
                 
          
                  <td class="align-middle text-nowrap text-center">
                    <template v-if="v.tinh_trang == 1">
                      <button v-on:click="changeStatus(v)" class="btn btn-success w-100">Hiển Thị</button>
                    </template>
                    <template v-else-if="v.tinh_trang == 0">
                      <button v-on:click="changeStatus(v)" class="btn btn-danger w-100">Tạm Tắt</button>
                    </template>
                  </td>
                  <td class="text-center align-middle text-nowrap">
                    <button class="btn btn-info me-2" data-bs-toggle="modal" v-on:click="Object.assign(edit_loai_san_pham, v)" data-bs-target="#editModal">Cập Nhật</button>
                    <button class="btn btn-danger" data-bs-toggle="modal" v-on:click="Object.assign(delete_loai_san_pham, v)" data-bs-target="#deleteModal">Xóa Bỏ</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        
        <!-- Delete Modal -->
        <div
          class="modal fade"
          id="deleteModal"
          tabindex="-1"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">
                  Xóa Loại Sản Phẩm
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <div
                  class="alert alert-danger border-0 bg-danger alert-dismissible fade show py-2"
                >
                  <div class="d-flex align-items-center">
                    <div class="font-35 text-white">
                      <i class="bx bxs-message-square-x"></i>
                    </div>
                    <div class="ms-1">
                      <h6 class="mb-1 text-white">
                        Bạn chắc chắc xóa Loại Sản Phẩm
                        <b>{{ delete_loai_san_pham.ten_loai }}</b> này chứ
                        !!!
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
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Đóng
                </button>
                <button
                  @click="xoaLoaiSanPham()"
                  type="button"
                  class="btn btn-danger"
                  data-bs-dismiss="modal"
                >
                  Xác Nhận
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Edit Modal -->
        <div
          class="modal fade"
          id="editModal"
          tabindex="-1"
          aria-labelledby="exampleModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">
                  Chỉnh Sửa Loại Sản Phẩm
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  data-bs-dismiss="modal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <label class="form-lable">Tên Sản Phẩm</label>
                <input
                  v-model="edit_loai_san_pham.ten_loai"
                  class="form-control mt-1"
                  type="text"
                />
                <label class="form-lable">Link Danh Mục</label>
                <input
                  v-model="edit_loai_san_pham.link_danh_muc"
                  class="form-control mt-1"
                  type="text"
                />

                <label class="form-lable mt-2"> Tình Trạng</label>
                <select
                  v-model="edit_loai_san_pham.tinh_trang"
                  class="form-control"
                >
                  <option value="1">Hiển Thị</option>
                  <option value="0">Tạm Dừng</option>
                </select>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  data-bs-dismiss="modal"
                >
                  Đóng
                </button>
                <button
                  @click="capNhatLoaiSanPham()"
                  type="button"
                  class="btn btn-primary"
                  data-bs-dismiss="modal"
                >
                  Xác Nhận
                </button>
              </div>
            </div>
          </div>
        </div>
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
      list_loai_san_pham: [],
      loading: false,
      debug_mode: true, // Bật debug mode để kiểm tra
      api_response: null
    };
  },
  mounted() {
    this.loadLoaiSanPham();
  },
  methods: {
    loadLoaiSanPham() {
      this.loading = true;
      axios
        .get("http://127.0.0.1:8000/products/type/list/")
        .then((res) => {
          console.log("API Response:", res.data); 
          this.api_response = JSON.stringify(res.data);
          
          // Kiểm tra cấu trúc response
          if (res.data && res.data.data) {
            this.list_loai_san_pham = res.data.data;
          } else if (Array.isArray(res.data)) {
            // Trường hợp API trả về trực tiếp array
            this.list_loai_san_pham = res.data;
          } else {
            console.error("Unexpected response structure:", res.data);
            this.list_loai_san_pham = [];
          }
          
          if (res.data.status === 0) {
            toaster.error(res.data.message);
          }
        })
        .catch((error) => {
          console.error("API Error:", error);
          this.list_loai_san_pham = [];
          if (toaster) {
            toaster.error("Lỗi khi tải dữ liệu: " + error.message);
          }
        })
        .finally(() => {
          this.loading = false;
        });
    },
    
    createLoaiSanPham() {
      if (!this.create_loai_san_pham.ten_loai) {
        toaster.error("Vui lòng nhập tên sản phẩm");
        return;
      }
      
      axios
        .post(
          "http://127.0.0.1:8000/products/type/create/",
          this.create_loai_san_pham
        )
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.create_loai_san_pham = {};
            this.loadLoaiSanPham();
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
    
    capNhatLoaiSanPham() {
      axios
        .post(`http://127.0.0.1:8000/products/type/update/${this.edit_loai_san_pham.id}/`, this.edit_loai_san_pham)
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.loadLoaiSanPham();

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
          `http://127.0.0.1:8000/products/type/delete/${this.delete_loai_san_pham.id}/`,
          this.delete_loai_san_pham
        )
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.loadLoaiSanPham();

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
    
    changeStatus(value) {
      axios
        .post(
          "http://127.0.0.1:8000/products/type/change-status/",
          value
        )
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.loadLoaiSanPham();
            
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
  },
};
</script>