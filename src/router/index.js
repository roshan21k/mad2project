import { createRouter, createWebHashHistory } from "vue-router";
import HomeView from "../views/user/HomeView.vue";
import LoginView from "../views/auth/LoginView.vue";
import SignupView from "../views/auth/SignupView.vue";
import AdminView from "../views/admin/AdminView.vue";
import UnauthorisedView from "../views/auth/UnauthorisedView.vue";
import CartView from "../views/user/CartView.vue";
import OrderView from "../views/user/OrderView.vue";
import OrderdetailsView from "../views/user/OrderdetailsView.vue";
import ProductdetailsView from "../views/user/ProductdetailsView.vue";
import ApplyView from "../views/user/ApplyView.vue";
import RoleView from "../views/admin/RoleView.vue";
import CategoryrequestView from "../views/admin/CategoryrequestView.vue";
import ManagerView from "../views/manager/ManagerView.vue";
import AddproductView from "../views/manager/AddproductView.vue";
import UpdateproductView from "../views/manager/UpdateproductView.vue";
import DeleteproductView from "../views/manager/DeleteproductView.vue";
import AddcategoryView from "../views/manager/AddcategoryView.vue";
import UpdatecategoryView from "../views/manager/UpdatecategoryView.vue";
import DeletecategoryView from "../views/manager/DeletecategoryView.vue";
import ProductrequestView from "../views/admin/ProductrequestView.vue";
import store from "@/store";
const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
    meta: { requiresAuth: true, role: ["user", "manager"] },
  },
  {
    path: "/product/:id",
    name: "productDetails",
    component: ProductdetailsView,
    meta: { requiresAuth: true, role: ["user", "manager"] },
    props: true,
  },
  {
    path: "/cart",
    name: "cart",
    component: CartView,
    meta: { requiresAuth: true, role: ["user", "manager"] },
  },
  {
    path: "/orders",
    name: "order",
    component: OrderView,
    meta: { requiresAuth: true, role: ["user", "manager"] },
  },
  {
    path: "/order/:id",
    name: "orderDetails",
    component: OrderdetailsView,
    meta: { requiresAuth: true, role: ["user", "manager"] },
    props: true,
  },
  {
    path: "/apply",
    name: "apply",
    component: ApplyView,
    meta: { requiresAuth: true, role: ["user"] },
  },
  {
    path: "/manage",
    name: "manage",
    component: ManagerView,
    meta: { requiresAuth: true, role: ["manager"] },
  },
  {
    path: "/add-product",
    name: "addProduct",
    component: AddproductView,
    meta: { requiresAuth: true, role: ["manager"] },
  },
  {
    path: "/update-product",
    name: "updateProduct",
    component: UpdateproductView,
    meta: { requiresAuth: true, role: ["manager"] },
  },
  {
    path: "/delete-product",
    name: "deleteProduct",
    component: DeleteproductView,
    meta: { requiresAuth: true, role: ["manager"] },
  },
  {
    path: "/add-category",
    name: "addCategory",
    component: AddcategoryView,
    meta: { requiresAuth: true, role: ["manager"] },
  },
  {
    path: "/update-category",
    name: "updateCategory",
    component: UpdatecategoryView,
    meta: { requiresAuth: true, role: ["manager"] },
  },
  {
    path: "/delete-category",
    name: "deleteCategory",
    component: DeletecategoryView,
    meta: { requiresAuth: true, role: ["manager"] },
  },
  {
    path: "/admin",
    name: "admin",
    component: AdminView,
    meta: { requiresAuth: true, role: ["admin"] },
  },
  {
    path: "/admin/role",
    name: "role",
    component: RoleView,
    meta: { requiresAuth: true, role: ["admin"] },
  },
  {
    path: "/admin/category_requests",
    name: "categoryRequests",
    component: CategoryrequestView,
    meta: { requiresAuth: true, role: ["admin"] },
  },
  {
    path: "/admin/product_requests",
    name: "productRequests",
    component: ProductrequestView,
    meta: { requiresAuth: true, role: ["admin"] },
  },
  {
    path: "/unauthorised",
    name: "unauthorised",
    component: UnauthorisedView,
    meta: { requiresAuth: true, role: [] },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
    meta: { requiresAuth: false, role: [] },
  },
  {
    path: "/signup",
    name: "signup",
    component: SignupView,
    meta: { requiresAuth: false, role: [] },
  },
  {
    path: "/signup",
    name: "signup",
    component: SignupView,
    meta: { requiresAuth: false, role: [] },
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authToken = localStorage.getItem("accessToken");
  const userRole = localStorage.getItem("userRole");
  if (authToken) {
    store.commit("setAuthenticated", true);
  }
  if (userRole) {
    store.commit("setUserRole", userRole);
  }
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth);
  const allowedRoles = to.matched.map((record) => record.meta.role).flat();

  if (requiresAuth && !store.state.isAuthenticated) {
    next("/login");
  } else if (
    requiresAuth &&
    allowedRoles.length > 0 &&
    !allowedRoles.includes(userRole)
  ) {
    if (store.state.isAuthenticated) {
      if (userRole === "admin") {
        next("/admin");
      } else {
        next("/");
      }
    } else {
      next("/login");
    }
  } else if (!requiresAuth && store.state.isAuthenticated) {
    if (userRole === "admin") {
      next("/admin");
    } else {
      next("/");
    }
  } else {
    next();
  }
});
export default router;
