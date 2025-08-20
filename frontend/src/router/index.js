import { createRouter, createWebHistory } from "vue-router"; // cài vue-router: npm install vue-router@next --save
const routes = [
    {
        path: '/', component: () => import('../components/NguoiDung/home/index.vue'), 
    },
    {
        path: '/admin/quan-ly-loai-san-pham', component: () => import('../components/Admin/LoaiSanPham/index.vue'), 
    },
    {
        path: '/admin/quan-ly-san-pham', component: () => import('../components/Admin/SanPham/index.vue'), 
    },
]
const router = createRouter({
    history: createWebHistory(),
    routes: routes
})

export default router