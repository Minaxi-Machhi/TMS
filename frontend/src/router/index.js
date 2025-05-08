// internal imports
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", redirect: "/dashboard" },
    {
      path: "/",
      component: () => import("@/layouts/default.vue"),
      children: [
        {
          path: "dashboard",
          name: "dashboard",
          component: () => import("@/pages/admin/dashboard/index.vue"),
        },
        {
          path: "project",
          name: "project-list",
          component: () => import("@/pages/admin/projects/index.vue"),
        },
        {
          path: "project/detail/:id",
          name: "project-detail",
          component: () =>
            import("@/pages/admin/projects/components/project-detail-page.vue"),
        },
        {
          path: "tasks",
          name: "task-list",
          component: () => import("@/pages/admin/tasks/index.vue"),
        },
        {
          path: "users",
          name: "user-list",
          component: () => import("@/pages/admin/users/index.vue"),
        },
        {
          path: "users",
          name: "user-list",
          component: () => import("@/pages/admin/users/index.vue"),
        },
      ],
    },
    {
      path: "/",
      component: () => import("@/layouts/blank.vue"),
      children: [
        {
          path: "login/",
          name: "Login",
          component: () => import("@/pages/login.vue"),
        },
        {
          path: "/:pathMatch(.*)*",
          component: () => import("@/pages/[...error].vue"),
        },
      ],
    },
  ],
});

export default router;
