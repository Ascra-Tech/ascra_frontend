import { userResource } from "@/data/user"
import { createRouter, createWebHistory } from "vue-router"
import { session } from "./data/session"

const routes = [
	{
		path: "/",
		name: "Home",
		component: () => import("@/pages/Home.vue"),
		meta: { requiresAuth: false }
	},
	{
		name: "Login",
		path: "/account/login",
		component: () => import("@/pages/Login.vue"),
		meta: { requiresAuth: false }
	},
	{
		name: "Signup",
		path: "/account/signup",
		component: () => import("@/pages/Signup.vue"),
		meta: { requiresAuth: false }
	},
	{
		name: "MyAccount",
		path: "/my-account",
		component: () => import("@/pages/MyAccount.vue"),
		meta: { requiresAuth: true }
	},
	{
		name: "EmployeeDashboard",
		path: "/employee-dashboard",
		component: () => import("@/pages/EmployeeDashboard.vue"),
		meta: { requiresAuth: true, requiresEmployeeRole: true }
	},
	{
		name: "ERPNext",
		path: "/erpnext",
		component: () => import("@/pages/ERPNext.vue"),
		meta: { requiresAuth: false }
	},
]

const router = createRouter({
	history: createWebHistory("/"),
	routes,
})

router.beforeEach(async (to, from, next) => {
	let isLoggedIn = session.isLoggedIn
	try {
		await userResource.promise
	} catch (error) {
		isLoggedIn = false
	}

	// Check if route requires authentication
	const requiresAuth = to.meta.requiresAuth

	if (to.name === "Login" && isLoggedIn) {
		// Redirect logged-in users away from login page to my account
		next({ name: "MyAccount" })
	} else if (requiresAuth && !isLoggedIn) {
		// Redirect unauthenticated users to login for protected routes
		next({ name: "Login" })
	} else {
		// Allow navigation
		next()
	}
})

export default router
