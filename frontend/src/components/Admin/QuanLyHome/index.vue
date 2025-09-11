<template>
  <div class="card">
    <div class="row">
      <div class="col m-2">
        <h3 class="card-title">Danh sách thẻ </h3>
      </div>
      <div class="col text-end m-2">
        <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#exampleModal">
          Thêm thẻ mới
        </button>
      </div>
    </div>

    <!-- Modal Thêm Mới -->
   <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">
          Thêm Mới Style
        </h1>
      </div>
      <div class="modal-body">
        <div class="mb-2">
          <label class="form-label">Tag</label>
          <input v-model="create_san_pham.tag" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Font Family</label>
          <input v-model="create_san_pham.font_family" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Font Size</label>
          <input v-model="create_san_pham.font_size" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Color</label>
          <input v-model="create_san_pham.color" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Background</label>
          <input v-model="create_san_pham.background" type="text" class="form-control" />
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
          Close
        </button>
        <button @:click="create_style()" class="btn btn-primary" data-bs-dismiss="modal">
          Thêm Mới
        </button>
      </div>
    </div>
  </div>
</div>

    <!-- Modal Cập Nhật -->
     <div class="modal fade" id="editModal" tabindex="-1" aria-labelledby="editModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="editModalLabel">
          Cập Nhật Style
        </h1>
      </div>
      <div class="modal-body">
        <div class="mb-2">
          <label class="form-label">Tag</label>
          <input v-model="edit_san_pham.tag" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Font Family</label>
          <input v-model="edit_san_pham.font_family" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Font Size</label>
          <input v-model="edit_san_pham.font_size" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Color</label>
          <input v-model="edit_san_pham.color" type="text" class="form-control" />
        </div>
        <div class="mb-2">
          <label class="form-label">Background</label>
          <input v-model="edit_san_pham.background" type="text" class="form-control" />
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
          Close
        </button>
        <button @click="update_style()" class="btn btn-primary" data-bs-dismiss="modal">
          Cập Nhật
        </button>
      </div>
    </div>
  </div>
</div>
    
    <div class="modal fade" id="deleteModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Xóa tag
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
                    Bạn chắc chắc xóa link
                    <b>{{ delete_san_pham.tag }}</b> này chứ !!!
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
            <button type="button" class="btn btn-danger" data-bs-dismiss="modal" v-on:click="delete_style()">
              Xác nhận
            </button>
          </div>
        </div>
      </div>
    </div> 

    <!-- Bảng dữ liệu -->
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th class="text-center align-middle text-nowrap">#</th>
              <th class="text-center align-middle text-nowrap">Tag</th>
              <th class="text-center align-middle text-nowrap">Font_family</th>
              <th class="text-center align-middle text-nowrap">Font_size</th>
              <th class="text-center align-middle text-nowrap">Color</th>
              <th class="text-center align-middle text-nowrap">background</th>
              <th class="text-center align-middle text-nowrap">Action</th>
            </tr>
          </thead>
         <tbody>
          <tr v-for="(linkItem, k) in list_style" :key="linkItem.id || k">
            <td class="align-middle text-nowrap">{{ k + 1 }}</td> <!-- số thứ tự -->
            <td class="align-middle text-nowrap">{{ linkItem.tag }}</td>
            <td class="align-middle" >
              {{ linkItem.font_family }}
            </td>
            <td class="align-middle" >
              {{ linkItem.font_size }}
            </td>
            <td class="align-middle" >
              {{ linkItem.color }}
            </td>
            <td class="align-middle" >
              {{ linkItem.background }}
            </td>
            

            <td class="text-center align-middle text-nowrap">
              <button @click="setEditSanPham(linkItem)" class="btn btn-info me-2" data-bs-toggle="modal" data-bs-target="#editModal">Cập Nhật</button>
              <button @click="setDeleteSanPham(linkItem)"  class="btn btn-danger" data-bs-toggle="modal" data-bs-target="#deleteModal">Xóa Bỏ</button>
            </td>
          </tr>
        </tbody>

        </table>
      </div>
    </div>
  </div>
</template>
<script>
import { createToaster } from "@meforma/vue-toaster";
const toaster = createToaster({ position: "top-right" });
import baseRequest from '../../../../src/core/baseRequest';
export default {
    data() {
        return {
            list_style: [],
            loading: false,
            api_response: '',
            create_san_pham: {},
            edit_san_pham: {},
            delete_san_pham: {},

            
        }
    },
    mounted() {
        this.loadStyle();
        
    },
    methods: {
      loadStyle() {
      this.loading = true;
      baseRequest
        .get("api/styles/list/")
        .then((res) => {
          console.log("API Response:", res.data); 
          this.api_response = JSON.stringify(res.data);
          
          // Kiểm tra cấu trúc response
          if (res.data && res.data.data) {
            this.list_style = res.data.data;
          } else if (Array.isArray(res.data)) {
            // Trường hợp API trả về trực tiếp array
            this.list_style = res.data;
          } else {
            console.error("Unexpected response structure:", res.data);
            this.list_style = [];
          }
          
          if (res.data.status === 0) {
            toaster.error(res.data.message);
          }
        })
        .catch((error) => {
          console.error("API Error:", error);
          this.list_style = [];
          if (toaster) {
            toaster.error("Lỗi khi tải dữ liệu: " + error.message);
          }
        })
        .finally(() => {
          this.loading = false;
        });
      },
      create_style() {
        // Chuẩn bị dữ liệu gửi lên API
        const payload = {
          tag: this.create_san_pham.tag,
          font_family: this.create_san_pham.font_family,
          font_size: this.create_san_pham.font_size,
          color: this.create_san_pham.color,
          background: this.create_san_pham.background,
        };

        baseRequest
          .post("api/styles/create/", payload)
          .then((res) => {
            if (res.data.status) {
              this.loadStyle(); // Load lại danh sách sau khi tạo mới
              toaster.success(res.data.message || "Tạo style thành công!");
            } else {
              toaster.error(res.data.message || "Tạo style thất bại!");
            }
          })
          .catch((error) => {
            toaster.error("Lỗi khi tạo style: " + error.message);
          });
      },
      update_style() {
      // Chuẩn bị dữ liệu gửi lên API
      const payload = {
        tag: this.edit_san_pham.tag,
        font_family: this.edit_san_pham.font_family,
        font_size: this.edit_san_pham.font_size,
        color: this.edit_san_pham.color,
        background: this.edit_san_pham.background,
      };

      // Giả sử bạn đã có id của style cần cập nhật trong edit_san_pham.id
      baseRequest
        .post(`api/styles/update/${this.edit_san_pham.id}/`, payload)
        .then((res) => {
          if (res.data.status) {
            this.loadStyle(); // Load lại danh sách sau khi cập nhật
            toaster.success(res.data.message || "Cập nhật style thành công!");
          } else {
            toaster.error(res.data.message || "Cập nhật style thất bại!");
          }
        })
        .catch((error) => {
          toaster.error("Lỗi khi cập nhật style: " + error.message);
        });
    },
      delete_style() {
        // Giả sử bạn đã có id của style cần xóa trong delete_san_pham.id
        baseRequest
          .post(`api/styles/delete/${this.delete_san_pham.id}/`)
          .then((res) => {
            if (res.data.status) {
              this.loadStyle(); // Load lại danh sách sau khi xóa
              toaster.success(res.data.message || "Xóa style thành công!");
            } else {
              toaster.error(res.data.message || "Xóa style thất bại!");
            }
          })
          .catch((error) => {
            toaster.error("Lỗi khi xóa style: " + error.message);
          });
      },
      setEditSanPham(item) {
          // Copy toàn bộ dữ liệu từ item sang edit_san_pham để binding vào form sửa
          this.edit_san_pham = {
            id: item.id,
            tag: item.tag,
            font_family: item.font_family,
            font_size: item.font_size,
            color: item.color,
            background: item.background,
          };
        },
      setDeleteSanPham(item) {
          // Copy toàn bộ dữ liệu từ item sang edit_san_pham để binding vào form sửa
          this.delete_san_pham = {
            id: item.id,
            tag: item.tag,
            font_family: item.font_family,
            font_size: item.font_size,
            color: item.color,
            background: item.background,
          };
        },
      
    }
}
</script>
<style >
    
</style>