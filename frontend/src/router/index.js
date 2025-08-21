import { createRouter, createWebHistory } from "vue-router"; // cài vue-router: npm install vue-router@next --save
import KiemTraAdmin from './KiemTraAdmin'

const routes = [
    {
        path: '/', component: () => import('../components/NguoiDung/home/index.vue'), 
    },
    {
        path: '/admin/quan-ly-loai-san-pham', component: () => import('../components/Admin/LoaiSanPham/index.vue'), 
        meta : {layout : 'client'},
        beforeEnter: KiemTraAdmin,


    },
    {
        path: '/admin/quan-ly-san-pham', component: () => import('../components/Admin/SanPham/index.vue'), 
        meta : {layout : 'client'},
        beforeEnter: KiemTraAdmin,


    },
    {
        path: '/admin/quan-ly-thong-ke', component: () => import('../components/Admin/ThongKe/index.vue'), 
        meta : {layout : 'client'},
        beforeEnter: KiemTraAdmin,


    },
    {
        path: '/admin/dang-nhap', component: () => import('../components/Admin/DangNhap/index.vue'), 

    },
]
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router