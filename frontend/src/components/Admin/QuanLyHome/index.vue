<template>
  <div class="card mt-2">
    <!-- Header -->
   

    <!-- Form chỉnh màu nền -->
    <div class="card mb-4">
      <div class="card-body">
         <div class="row align-items-center mb-3">
      <div class="col">
        <h2 class="card-title mt-3 ">Quản lý Style hệ thống</h2>
        <h5 style="color: red;">Lưu ý : không nên xóa bất kỳ Tag nào vì nó ảnh hưởng đến hệ thống</h5 style="color: red;">
      </div>
      <div class="col text-end">
        <button class="btn btn-info" data-bs-toggle="modal" data-bs-target="#addStyleModal">
          Thêm Style mới
        </button>
      </div>
    </div>
        <h5 class="card-title">Thay đổi màu nền hệ thống</h5>
        <div class="row align-items-center">
          <div class="col-md-6">
            <input v-model="site_background" type="text" class="form-control" placeholder="#fffef3" />
          </div>
          <div class="col-md-4">
            <button class="btn btn-success" @click="updateBackground">Cập nhật màu nền</button>
          </div>
          <div class="col-md-2 text-end">
           <button class="btn btn-secondary" data-bs-toggle="modal" data-bs-target="#ghichumodel">
         Ghi chú
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
                  <th>tieude</th>
                  <td>Connect with us</td>
                </tr>
                <tr>
                  <th>button</th>
                  <td>Website, Amazon Store, Tiny Daisy Community, 40 Free Digital Pages</td>
                </tr>
                <tr>
                  <th>loai-san-pham</th>
                  <td>Fantasy, Fuzzy Buddies (tên của loại sản phẩm)</td>
                </tr>
                <tr>
                  <th>san-pham</th>
                  <td>Tên Sản phẩm</td>
                </tr>
                <tr>
                  <th>button-shop-now</th>
                  <td>button SHOP NOW</td>
                </tr>
                <tr>
                  <th>email</th>
                  <td>Email</td>
                </tr>
                <tr>
                  <th>price</th>
                  <td>Giá Sản phẩm</td>
                </tr>
                <tr>
                  <th>tinydaisy</th>
                  <td>@tinydaisy.coloring</td>
                </tr>
                <tr>
                  <th>collapse-title</th>
                  <td>Tên của collapse icon</td>
                </tr>
                <tr>
                  <th>collapse-sub</th>
                  <td>giá trị bên dưới của collapse icon</td>
                </tr>
                <tr>
                  <th>background-layout-icon</th>
                  <td>background layout Collapse icon</td>
                </tr>
                <tr>
                  <th>card-body-style</th>
                  <td>Là ô bên dưới sản phẩm</td>
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

    <!-- Bảng style -->
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-bordered align-middle">
          <thead class="table-light">
            <tr>
              <th>Tag</th>
              <th>Font Family (Google Fonts)</th>
              <!-- <th>Font Size</th> -->
              <th>Color</th>
              <th>Độ dày của chữ</th>
              <th>background</th>
              <th class="text-center">Hành động</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in list_style" :key="item.id">
              <td>{{ item.tag }}</td>
              <td>{{ item.font_family }}</td>
              <td>
                <span :style="{color: item.color}">{{ item.color }}</span>
              </td>
              <td>{{ item.font_weight }}</td>
              <td>
                <span :style="{color: item.background}">{{ item.background }}</span>
              </td>
              <td class="text-center">
                <button class="btn btn-info me-2" @click="setEditSanPham(item)" data-bs-toggle="modal" data-bs-target="#editStyleModal">Sửa</button>
                <button class="btn btn-danger" @click="setDeleteSanPham(item)" data-bs-toggle="modal" data-bs-target="#deleteStyleModal">Xóa</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Thêm Style -->
    <div class="modal fade" id="addStyleModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header"><h5>Thêm Style mới</h5></div>
          <div class="modal-body">
            <input v-model="create_san_pham.tag" class="form-control mb-2" placeholder="Tag (ví dụ: h2, .main-btn)">
            <input v-model="create_san_pham.font_family" class="form-control mb-2" placeholder="Font Family (ví dụ: Roboto)">
            <!-- <input v-model="create_san_pham.font_size" class="form-control mb-2" placeholder="Font Size (ví dụ: 18px)"> -->
            <input v-model="create_san_pham.color" class="form-control mb-2" placeholder="Color (ví dụ: #333)">
            <input v-model="create_san_pham.font_weight" class="form-control mb-2" placeholder="nhập từ 100 đến 1000">
            <input v-model="create_san_pham.background" class="form-control mb-2" placeholder="có thể bỏ trống nếu không cần">
            <small class="text-muted">Font Family có thể nhập bất kỳ, nếu là Google Fonts sẽ tự động tải.</small>
          </div>
          <div class="modal-footer">
            <button class="btn btn-primary" @click="create_style">Thêm mới</button>
            <button class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Sửa Style -->
    <div class="modal fade" id="editStyleModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header"><h5>Sửa Style</h5></div>
          <div class="modal-body">
            <label for="">	Font Family(Google Fonts)</label>
            <input v-model="edit_san_pham.font_family" class="form-control mb-2" placeholder="Font Family">
            <!-- <label for="">Font Size</label>
            <input v-model="edit_san_pham.font_size" class="form-control mb-2" placeholder="Font Size"> -->
            <label for="">Color</label>
            <input v-model="edit_san_pham.color" class="form-control mb-2" placeholder="Color">
            <label for="">font_weight</label>
            <input v-model="edit_san_pham.font_weight" class="form-control mb-2" placeholder="nhập từ 100 - > 1000">
            <label for="">background</label>
            <input v-model="edit_san_pham.background" class="form-control mb-2" placeholder="mã màu">
          </div>
          <div class="modal-footer">
            <button class="btn btn-success" @click="update_style">Cập nhật</button>
            <button class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Xóa Style -->
    <div class="modal fade" id="deleteStyleModal" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header"><h5>Xóa Style</h5></div>
          <div class="modal-body">
            Bạn có chắc muốn xóa style <b>{{ delete_san_pham.tag }}</b>?
          </div>
          <div class="modal-footer">
            <button class="btn btn-danger" @click="delete_style">Xóa</button>
            <button class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
          </div>
        </div>
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
      create_san_pham: {},
      edit_san_pham: {},
      delete_san_pham: {},
      site_background: '',
    }
  },
  mounted() {
    this.loadStyle();
    this.loadBackground();
    
  },
  methods: {
  prepareEdit(sanPhamItem) {
    // Chỉ set dữ liệu cho modal, không reset list, không reload API
    this.edit_san_pham = { ...sanPhamItem, new_image: null };
  },
  prepareDelete(sanPhamItem) {
    this.delete_san_pham = { 
      id: sanPhamItem.id, 
      ten_san_pham: sanPhamItem.ten_san_pham 
    };
  },
    // Lấy danh sách style
    loadStyle() {
      this.loading = true;
      baseRequest.get("api/styles/list/")
        .then((res) => {
          this.list_style = res.data;
        })
        .catch(() => {
          toaster.error("Lỗi khi tải style!");
        })
        .finally(() => {
          this.loading = false;
        });
    },
    // Lấy màu nền hiện tại
    loadBackground() {
      baseRequest.get("api/styles/background/")
        .then(res => {
          this.site_background = res.data.background;
        });
    },
    // Cập nhật màu nền
    updateBackground() {
      baseRequest.post("api/styles/background/", { background: this.site_background })
        .then(res => {
          if (res.data.status) {
            toaster.success("Đã cập nhật màu nền!");
            this.loadBackground();
          } else {
            toaster.error("Cập nhật thất bại!");
          }
        });
    },
    // Thêm style mới
    create_style() {
      baseRequest.post("api/styles/create/", this.create_san_pham)
        .then(() => {
          toaster.success("Thêm style thành công!");
          this.loadStyle();
        })
        .catch(() => {
          toaster.error("Lỗi khi thêm style!");
        });
    },
    // Cập nhật style
    update_style() {
      baseRequest.post(`api/styles/update/${this.edit_san_pham.id}/`, this.edit_san_pham)
        .then(() => {
          toaster.success("Cập nhật style thành công!");
          this.loadStyle();
        })
        .catch(() => {
          toaster.error("Lỗi khi cập nhật style!");
        });
    },
    // Xóa style
    delete_style() {
      baseRequest.post(`api/styles/delete/${this.delete_san_pham.id}/`)
        .then(() => {
          toaster.success("Xóa style thành công!");
          this.loadStyle();
        })
        .catch(() => {
          toaster.error("Lỗi khi xóa style!");
        });
    },
    // Chọn style để sửa
    setEditSanPham(item) {
      this.edit_san_pham = { ...item };
    },
    // Chọn style để xóa
    setDeleteSanPham(item) {
      this.delete_san_pham = { ...item };
    },
  }
}
</script>
<style>
body.modal-open {
    padding-right: 0 !important;
}</style>