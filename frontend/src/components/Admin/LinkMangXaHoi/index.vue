<template>
  <div class="card">
    <div class="row">
      <div class="col">
        <h3 class="card-title">Danh sách sản phẩm</h3>
      </div>
      <div class="col text-end">
        <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#exampleModal">
          Thêm Sản Phẩm
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
              <label class="form-label">Link</label>
              <input v-model="create_link.links" type="url" class="form-control" />
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
              <label class="form-label">Links</label>
              <input v-model="edit_link.links" type="url" class="form-control" />
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
              <th class="text-center align-middle text-nowrap">Link</th>
              <th class="text-center align-middle text-nowrap">Action</th>
            </tr>
          </thead>
         <tbody>
          <tr v-for="(linkItem, k) in list_link" :key="linkItem.id || k">
            <td class="align-middle text-nowrap">{{ k + 1 }}</td> <!-- số thứ tự -->
            <td class="align-middle text-nowrap">{{ linkItem.name }}</td>
            <td class="align-middle" style="max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
              {{ linkItem.links }}
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
      api_response: null


    };
  },
  mounted() {
    this.loadlink();
  },
  methods: {
    loadlink() {
      this.loading = true;
      baseRequest
        .get("api/links/list/")
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
      
      baseRequest
        .post("api/link/create/", this.create_link)
        .then((res) => {
          if (res.data.status) {
            toaster.success(res.data.message);
            this.create_link = {};
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

  
  baseRequest
    .post(`api/link/update/${idToUse}/`, {
      name: this.edit_link.name,
      links: this.edit_link.links
    })
    .then((res) => {
      if (res.data.status) {
        toaster.success(res.data.message);
        this.loadlink();
      } else {
        toaster.error(res.data.message);
      }
    })
    .catch((error) => {
      toaster.error("Có lỗi xảy ra khi cập nhật");
    });
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
</style>