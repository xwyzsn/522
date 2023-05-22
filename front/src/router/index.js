import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'adminLayout',
      component: () => import('../views/admin/AdminLayout.vue'),
      redirect: '/personmanagement',
      children: [
        { path: 'usermanagement', name: 'usermanagement', component: () => import('../views/admin/userManage.vue') },
        { path: 'roommanagement', name: 'roommanagement', component: () => import('../views/admin/roomManage.vue') },
        { path: 'reservationmanagement', name: 'reservationmanagement', component: () => import('../views/admin/reservationManage.vue') },
        { path: 'personmanagement', name: 'personmanagement', component: () => import('../views/admin/personManage.vue') },
        { path: 'commentmanagement', name: 'commentmanagement', component: () => import('../views/admin/commentManage.vue') },
        { path: 'bookmarkmanagement', name: 'bookmarkmanagement', component: () => import('../views/admin/bookmarkManage.vue') },
      ]

    }
  ]
})

export default router
