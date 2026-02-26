app_name = "ascra_frontend"
app_title = "Ascra Frontend"
app_publisher = "Amit Kumar"
app_description = "Frontend of Ascratech Website"
app_email = "amit@ascratech.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ascra_frontend",
# 		"logo": "/assets/ascra_frontend/logo.png",
# 		"title": "Ascra Frontend",
# 		"route": "/ascra_frontend",
# 		"has_permission": "ascra_frontend.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ascra_frontend/css/ascra_frontend.css"
# app_include_js = "/assets/ascra_frontend/js/ascra_frontend.js"

# include js, css files in header of web template
# web_include_css = "/assets/ascra_frontend/css/ascra_frontend.css"
# web_include_js = "/assets/ascra_frontend/js/ascra_frontend.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ascra_frontend/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ascra_frontend/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# website_route_rules = [
# 	{"from_route": "/<path:app_path>", "to_route": "frontend"},
# ]

# More specific route rules to avoid overriding Frappe's standard routes
website_route_rules = [
	{"from_route": "/", "to_route": "frontend"},
	{"from_route": "/home", "to_route": "frontend"},
	{"from_route": "/dashboard", "to_route": "frontend"},
	{"from_route": "/employee-dashboard", "to_route": "frontend"},
	{"from_route": "/account/login", "to_route": "frontend"},
	{"from_route": "/account/signup", "to_route": "frontend"},
]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ascra_frontend.utils.jinja_methods",
# 	"filters": "ascra_frontend.utils.jinja_filters"
# }

# Installation
# ------------

before_install = "ascra_frontend.install.before_install"
after_install = "ascra_frontend.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ascra_frontend.uninstall.before_uninstall"
# after_uninstall = "ascra_frontend.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ascra_frontend.utils.before_app_install"
# after_app_install = "ascra_frontend.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ascra_frontend.utils.before_app_uninstall"
# after_app_uninstall = "ascra_frontend.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ascra_frontend.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ascra_frontend.tasks.all"
# 	],
# 	"daily": [
# 		"ascra_frontend.tasks.daily"
# 	],
# 	"hourly": [
# 		"ascra_frontend.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ascra_frontend.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ascra_frontend.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ascra_frontend.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ascra_frontend.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ascra_frontend.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ascra_frontend.utils.before_request"]
# after_request = ["ascra_frontend.utils.after_request"]

# Job Events
# ----------
# before_job = ["ascra_frontend.utils.before_job"]
# after_job = ["ascra_frontend.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ascra_frontend.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

# Translation
# ------------
# List of apps whose translatable strings should be excluded from this app's translations.
# ignore_translatable_strings_from = []

