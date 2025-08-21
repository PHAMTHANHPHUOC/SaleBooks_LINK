<template>
    <header>
        <div class="topbar d-flex align-items-center">
            <nav class="navbar navbar-expand">
                <div class="topbar-logo-header">
                    <div class="">
                        <img src="../../assets/images/TINY.jpg" class="logo-icon" alt="logo icon">
                    </div>
                    <div class="">
                        <h4 class="logo-text">Tiny Daisy</h4>
                    </div>
                </div>
                <div class="mobile-toggle-menu"><i class='bx bx-menu'></i></div>
                <div class="search-bar flex-grow-1">
                    <div class="position-relative search-bar-box">
                        <input type="text" class="form-control search-control" placeholder="Type to search...">
                        <span class="position-absolute top-50 search-show translate-middle-y"><i
                                class='bx bx-search'></i></span>
                        <span class="position-absolute top-50 search-close translate-middle-y"><i
                                class='bx bx-x'></i></span>
                    </div>
                </div>
           
                <div class="user-box dropdown">
                    <a class="d-flex align-items-center nav-link dropdown-toggle dropdown-toggle-nocaret" href="#"
                        role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        <img src="../../assets/images/TINY.jpg" class="user-img" alt="user avatar">
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end">
                    
                        <li>
                            <div class="dropdown-divider mb-0"></div>
                        </li>
                        <li><a v-on:click="dangXuat()" class="dropdown-item"><i
                                        class='bx bx-log-out-circle'></i><span>Đăng Xuất</span></a>
                        </li>
                        <li><a v-on:click="dangXuatAll()" class="dropdown-item"><i
                                    class='bx bx-log-out-circle'></i><span>Đăng Xuất Tất Cả</span></a>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    </header>
</template>
<script>
import { createToaster } from "@meforma/vue-toaster";
import axios from "axios";
const toaster = createToaster({ position: "top-right" });
export default {
    data() {
        return {
            name_admin            : '',
        }
    },
    mounted() {
        this.name_admin = localStorage.getItem('ten_admin')
    },
    methods: {
        dangXuat() {
            const token = localStorage.getItem("chia_khoa");
            axios
                .post("http://127.0.0.1:8000/logout/", {}, {
                    headers: {
                        Authorization: "Token " + token,
                    },
                })
                .then((res) => {
                    if (res.data.status) {
                        toaster.success(res.data.message);
                        localStorage.setItem("chia_khoa", "");
                        this.$router.push("dang-nhap");
                    } else {
                        toaster.error(res.data.message);
                    }
                });
        },
        dangXuatAll() {
            const token = localStorage.getItem("chia_khoa");
            axios
                .post("http://127.0.0.1:8000/logout-all/", {}, {
                    headers: {
                        Authorization: "Token " + token,
                    },
                })
                .then((res) => {
                    if (res.data.status) {
                        toaster.success(res.data.message);
                        localStorage.setItem("chia_khoa", "");
                        this.$router.push("dang-nhap");
                    } else {
                        toaster.error(res.data.message);
                    }
                });
        },
    },
}
</script>
<style scoped>
.topbar {
    height: 64px;
    padding: 0 32px;
    display: flex;
    align-items: center;

    gap: 16px;
}

.topbar-logo-header {
    display: flex;
    align-items: center;
    gap: 12px;
    flex: 0 0 auto;
}

.search-bar {
    flex: 1 1 0;
    display: flex;
    justify-content: center;
    max-width: 500px;
    min-width: 200px;
    margin: 0 24px;
}

.search-bar-box {
    width: 100%;
    position: relative;
    max-width: 400px;
}

.user-box {
    margin-left: auto;
    flex: 0 0 auto;
    display: flex;
    align-items: center;
}
.logo-text {
    font-size: 22px;
    margin-left: 10px;
    margin-bottom: 0;
    letter-spacing: 1px;
    color: #0e0f0f;
}
</style>