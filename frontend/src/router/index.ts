import { createRouter, createWebHistory } from "vue-router";
import BuilderView from "../views/BuilderView.vue";

const routes = [
  {
    path: "/",
    name: "builder",
    component: BuilderView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;