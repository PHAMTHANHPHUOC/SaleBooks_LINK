<template>
  <div class="card">
    <div class="row">
      <div class="col m-2">
        <h3 class="card-title">Danh sách sản phẩm </h3>
      </div>
      <div class="col text-end m-2 mt-2">
        <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#exampleModal">
          Thêm Sản Phẩm
        </button>
        <button class="btn btn-secondary m-2" data-bs-toggle="modal" data-bs-target="#ghichumodel">
         Ghi chú
        </button>
      </div>
    </div>

    <!-- Modal Thêm Mới -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="exampleModalLabel">
              Thêm Mới links
            </h1>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label">Tên Link</label>
              <input v-model="create_link.name" type="text" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Sub title</label>
              <input v-model="create_link.subtitle" type="text" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Link</label>
              <input v-model="create_link.links" type="url" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Loại</label>
              <select v-model="create_link.loai" class="form-control">
                <option :value="0">Liên hệ</option>
                <option :value="1">Mạng Xã Hội (Có icon)</option>
                <option :value="2">Mạng Xã Hội</option>
                <option :value="3">Khác</option>
              </select>
            </div>
            <div class="mb-2">
              <label class="form-label">Ảnh bìa</label>
              <input type="file" class="form-control" @change="onFileChange" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>
            <button v-on:click="createLink()" class="btn btn-primary" data-bs-dismiss="modal">
              Thêm Mới
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="ghichumodel" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog modal-xl"> <!-- Thay modal-xl để bảng to hơn -->
    <div class="modal-content">
      <div class="modal-header">
        <h1 class="modal-title fs-5" id="exampleModalLabel">
          Ghi chú
        </h1>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <div class="card-body">
          <div class="table-responsive">
            <table class="table table-bordered align-middle">
              <tbody>
                <tr>
                  <th>Liên hệ</th>
                  <td>Là những link icon đầu</td>
                </tr>
                <tr>
                  <th>Mạng Xã Hội (có icon)</th>
                  <td>là button bên dưới, có icon bên trái</td>
                </tr>
                <tr>
                  <th>Mạng Xã Hội</th>
                  <td>là button bên dưới, không có icon bên trái</td>
                </tr>
                <tr>
                  <th><p style="color: red;">Lưu ý</p></th>
                  <td  style="color: red;">Edit theo loại</td>
                </tr>
                
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
          Close
        </button>
        <button type="button" class="btn btn-danger" data-bs-dismiss="modal" >
          Xác nhận
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
              Cập Nhật Link
            </h1>
          </div>
          <div class="modal-body">
            <div class="mb-2">
              <label class="form-label">Tên Link</label>
              <input v-model="edit_link.name" type="text" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Sub Title</label>
              <input v-model="edit_link.subtitle" type="text" class="form-control" />
            </div>
           
            <div class="mb-2">
              <label class="form-label">Links</label>
              <input v-model="edit_link.links" type="url" class="form-control" />
            </div>
            <div class="mb-2">
              <label class="form-label">Loại</label>
              <select v-model="edit_link.loai" class="form-control">
                <option :value="0">Liên hệ</option>
                <option :value="1">Mạng Xã Hội (Có icon)</option>
                <option :value="2">Mạng Xã Hội</option>
                <option :value="3">Khác</option>
              </select>
            </div>
            <div class="mb-2">
              <label class="form-label">Icon hiên tại</label>
              <div v-if="edit_link.anh_dai_dien" class="mb-2">
                  <img :src="getFullImageUrl(edit_link.anh_dai_dien)" 
                        class="img-thumbnail" 
                        style="max-width: 100px; max-height: 100px;" 
                        @error="handleImageError" />
              </div>
              <input type="file" class="form-control" @change="onEditFileChange" />
          </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Close
            </button>
                  <button v-on:click="updateLink()" class="btn btn-primary" data-bs-dismiss="modal">
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
                    Xóa link
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
                          <b>{{ delete_link.name }}</b> này chứ !!!
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
                  <button type="button" class="btn btn-danger" data-bs-dismiss="modal" v-on:click="deleteLink()">
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
                    <th class="text-center align-middle text-nowrap">Tên Link</th>
                    <th class="text-center align-middle text-nowrap">Sub title</th>
                    <th class="text-center align-middle text-nowrap">Link</th>
                    <th class="text-center align-middle text-nowrap">Icon</th>
                    <th class="text-center align-middle text-nowrap">Loai</th>
                    <th class="text-center align-middle text-nowrap">Tình Trạng</th>
                    <th class="text-center align-middle text-nowrap">Action</th>
                  </tr>
                </thead>
              <tbody>
                <tr v-for="(linkItem, k) in list_link" :key="linkItem.id || k">
                  <td class="align-middle text-nowrap">{{ k + 1 }}</td> <!-- số thứ tự -->
                  <td class="align-middle text-nowrap">{{ linkItem.name }}</td>
                  <td class="align-middle text-nowrap">{{ linkItem.subtitle }}</td>
                  <td class="align-middle link-column" style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
                    {{ linkItem.links }}
                  </td>
                  <td>
                    <div v-if="linkItem.anh_dai_dien" class="image-container">
                      <img  :src="getFullImageUrl(linkItem.anh_dai_dien)" 
                        class="product-image img-thumbnail" 
                        @error="handleImageError"
                        @click="showImagePreview(getFullImageUrl(linkItem.anh_dai_dien))" />
                    </div>
                    <div v-else class="no-image">
                      <i class="bx bx-image text-muted"></i>
                      <small class="text-muted">Chưa có ảnh</small>
                    </div>
                  </td>
                  <td class="align-middle text-nowrap text-center">
                    <template v-if="linkItem.loai == 0">
                      <span class="badge bg-success">Liên hệ</span>
                    </template>
                    <template v-else-if="linkItem.loai == 1">
                      <span class="badge bg-primary">Mạng Xã Hội(có icon)</span>
                    </template>
                    <template v-else-if="linkItem.loai == 2">
                      <span class="badge bg-primary">Mạng Xã Hội</span>
                    </template>
                    <template v-else>
                      <span class="badge bg-secondary">Khác</span>
                    </template> 
                  </td>
                  <td class="align-middle text-nowrap text-center">
                                <template v-if="linkItem.tinh_trang == 1">
                                  <button v-on:click="changeStatus(linkItem)" class="btn btn-success w-100">Hiển Thị</button>
                                </template>
                                <template v-else-if="linkItem.tinh_trang == 0">
                                  <button v-on:click="changeStatus(linkItem)" class="btn btn-danger w-100">Tạm Tắt</button>
                                </template>
                              </td>

                  <td class="text-center align-middle text-nowrap">
                    <button class="btn btn-info me-2" @click="prepareEdit(linkItem)" data-bs-toggle="modal" data-bs-target="#editModal">Cập Nhật</button>
                    <button class="btn btn-danger" @click="prepareDelete(linkItem)" data-bs-toggle="modal" data-bs-target="#deleteModal">Xóa Bỏ</button>
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
            list_link: [],
            create_link: {},
            edit_link: {},
            delete_link: {},
            loading: false,
            debug_mode: true, // Bật debug mode để kiểm tra
            api_response: null,
            previewImageUrl: '', // Thêm để preview ảnh
            baseUrl: '' // Thêm base URL


          };
        },
        mounted() {
          this.loadlink();
          this.initializeBaseUrl();

        },
        methods: {
          changeStatus(value) {
            const idToUse = value?.id || value?.database_id;
            if (!idToUse) {
              toaster.error("ID không hợp lệ để đổi trạng thái");
              return;
            }
            baseRequest
              .post(
                "api/link/change-status/",
                { id: idToUse }
              )
              .then((res) => {
                if (res.data.status) {
                  toaster.success(res.data.message);
                  this.loadlink();
                  
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
          initializeBaseUrl() {
            // Giả sử baseRequest có thuộc tính baseURL hoặc defaults.baseURL
            this.baseUrl = baseRequest.defaults?.baseURL || 'http://192.168.1.28:8000';
            // Đảm bảo không có dấu / cuối
            this.baseUrl = this.baseUrl.replace(/\/$/, '');
          },
          resetCreateModal() {
          this.create_link = {};
          const input = document.querySelector('#exampleModal input[type="file"]');
          if (input) input.value = '';
          },
          resetEditModal() {
            this.edit_link.new_image = null;
            const input = document.querySelector('#editModal input[type="file"]');
            if (input) input.value = '';
          },
          getFullImageUrl(imagePath) {
            if (!imagePath) return '';
            
            // Nếu đã là URL đầy đủ thì return luôn
            if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) {
              return imagePath;
            }
            
            // Nếu không bắt đầu bằng / thì thêm vào
            if (!imagePath.startsWith('/')) {
              imagePath = '/' + imagePath;
            }
            
            return this.baseUrl + imagePath;
          },

          // Xử lý lỗi khi không tải được ảnh
          handleImageError(event) {
            event.target.src = 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHJlY3Qgd2lkdGg9IjYwIiBoZWlnaHQ9IjYwIiBmaWxsPSIjRjNGNEY2Ii8+CjxwYXRoIGQ9Ik0zMCAyMEMyNi42ODYzIDIwIDI0IDIyLjY4NjMgMjQgMjZDMjQgMjkuMzEzNyAyNi42ODYzIDMyIDMwIDMyQzMzLjMxMzcgMzIgMzYgMjkuMzEzNyAzNiAyNkMzNiAyMi42ODYzIDMzLjMxMzcgMjAgMzAgMjBaIiBmaWxsPSIjOUNBM0FGIi8+CjxwYXRoIGQ9Ik0xNiA0MEw0NCA0MEw0MCAzNkwzNiAzMkwyOCAzNkwyMCAzMkwxNiAzNloiIGZpbGw9IiM5Q0EzQUYiLz4KPC9zdmc+';
            event.target.alt = 'Không thể tải ảnh';
          },

          // Hiển thị preview ảnh
          showImagePreview(imageUrl) {
            this.previewImageUrl = imageUrl;
            // Sử dụng Bootstrap modal
            const modal = new bootstrap.Modal(document.getElementById('imagePreviewModal'));
            modal.show();
          },

          // Xử lý file upload cho thêm mới
          onFileChange(event) {
            const file = event.target.files[0];
            if (file) {
              // Có thể thêm logic upload file ở đây
              this.create_link.anh_dai_dien = file;
            }
          },

          // Xử lý file upload cho chỉnh sửa
          onEditFileChange(event) {
            const file = event.target.files[0];
            if (file) {
              // Có thể thêm logic upload file ở đây
              this.edit_link.new_image = file;
            }
          },
          loadlink() {
            this.loading = true;
            baseRequest
              .get("api/links/list/data/")
              .then((res) => {
                console.log("API Response:", res.data); 
                this.api_response = JSON.stringify(res.data);
                
                // Kiểm tra cấu trúc response
                if (res.data && res.data.data) {
                  this.list_link = res.data.data;
                } else if (Array.isArray(res.data)) {
                  // Trường hợp API trả về trực tiếp array
                  this.list_link = res.data;
                } else {
                  console.error("Unexpected response structure:", res.data);
                  this.list_link = [];
                }
                
                if (res.data.status === 0) {
                  toaster.error(res.data.message);
                }
              })
              .catch((error) => {
                console.error("API Error:", error);
                this.list_link = [];
                if (toaster) {
                  toaster.error("Lỗi khi tải dữ liệu: " + error.message);
                }
              })
              .finally(() => {
                this.loading = false;
              });
          },
          

          createLink() {
            if (!this.create_link.name || this.create_link.name.trim() === "") {
              toaster.error("Vui lòng nhập tên sản phẩm");
              return;
            }

            const formData = new FormData();
            formData.append("name", this.create_link.name);
            formData.append("subtitle", this.create_link.subtitle || ''); // Gửi subtitle nếu có
            formData.append("links", this.create_link.links);
            formData.append("loai", this.create_link.loai);
            if (this.create_link.anh_dai_dien) {
              formData.append("anh_dai_dien", this.create_link.anh_dai_dien);
            }

            baseRequest
              .post("api/link/create/", formData, {
                headers: { "Content-Type": "multipart/form-data" }
              })
              .then((res) => {
                if (res.data.status) {
                  toaster.success(res.data.message);
                  this.create_link = {};
                  this.loadlink();
                  this.resetCreateModal();
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

          updateLink() {
        const idToUse = this.edit_link.database_id || this.edit_link.id;
        
        if (!idToUse) {
          toaster.error("ID không hợp lệ để cập nhật");
          return;
        }

        const formData = new FormData();
        formData.append("name", this.edit_link.name);
        formData.append("subtitle", this.edit_link.subtitle || ''); // Gửi subtitle nếu có
        formData.append("links", this.edit_link.links);
        formData.append("loai", this.edit_link.loai);

        // Nếu có ảnh mới thì gửi lên, nếu không thì bỏ qua
        if (this.edit_link.new_image) {
          formData.append("anh_dai_dien", this.edit_link.new_image);
        }

        baseRequest
          .post(`api/link/update/${idToUse}/`, formData, {
            headers: { "Content-Type": "multipart/form-data" }
          })
          .then((res) => {
            if (res.data.status) {
              toaster.success(res.data.message);
              this.loadlink();
              this.resetEditModal();
            } else {
              toaster.error(res.data.message);
            }
          })
          .catch((error) => {
            toaster.error("Có lỗi xảy ra khi cập nhật");
          });
      },
prepareEdit(linkItem) {
    this.edit_link = { ...linkItem, new_image: null };
    this.$nextTick(() => this.resetEditModal());
  },

deleteLink() {
  const idToUse = this.delete_link.database_id || this.delete_link.id;
  
  if (!idToUse) {
    toaster.error("ID không hợp lệ để xóa");
    return;
  }
  
  
  baseRequest.post(`api/link/delete/${idToUse}/`)
  .then((res) => {
    if (res.data.status) {
      toaster.success(res.data.message);
      this.loadlink();
    } else {
      toaster.error(res.data.message);
    }
  })
  .catch((error) => {
    toaster.error("Có lỗi xảy ra khi xóa");
  });
},

prepareEdit(linkItem) {
  this.edit_link = { ...linkItem };
},

prepareDelete(linkItem) {
  this.delete_link = { 
    id: linkItem.id, 
    database_id: linkItem.database_id,
    name: linkItem.name 
  };
}

  }
}
</script>

<style>
.link-column {
  width: 400px !important;
  max-width: 400px !important;
  min-width: 400px !important;
}
</style>