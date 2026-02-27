import { createApp } from "vue"
import { FrappeUI } from "frappe-ui"

import App from "./App.vue"
import router from "./router"
import { initSocket } from "./socket"
import "./index.css"
import { useTheme } from "./composables/useTheme"

import {
	Alert,
	Badge,
	Button,
	Dialog,
	ErrorMessage,
	FormControl,
	Input,
	TextInput,
	frappeRequest,
	pageMetaPlugin,
	resourcesPlugin,
	setConfig,
} from "frappe-ui"

import "./index.css"

const globalComponents = {
	Button,
	TextInput,
	Input,
	FormControl,
	ErrorMessage,
	Dialog,
	Alert,
	Badge,
}

const app = createApp(App)

setConfig("resourceFetcher", frappeRequest)

app.use(router)
app.use(resourcesPlugin)
app.use(pageMetaPlugin)

const socket = initSocket()
app.config.globalProperties.$socket = socket

for (const key in globalComponents) {
	app.component(key, globalComponents[key])
}

// Initialize theme before mounting app
const theme = useTheme()
theme.initTheme()

app.mount("#app")
