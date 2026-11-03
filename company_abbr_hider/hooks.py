app_name = "company_abbr_hider"
app_title = "Company Abbreviation Hider"
app_publisher = "Anantdv"
app_description = "Hide ERPNext company abbreviations in user-facing labels and exports while preserving internal identifiers."
app_email = "support@anantdv.com"
app_license = "mit"

required_apps = ["erpnext"]

app_include_js = "/assets/company_abbr_hider/js/company_abbr_hider.js"

doctype_tree_js = {
	"Account": "public/js/tree_labels.js",
	"Warehouse": "public/js/tree_labels.js",
	"Cost Center": "public/js/tree_labels.js",
}

after_install = "company_abbr_hider.install.after_install"
after_migrate = "company_abbr_hider.install.after_migrate"
after_uninstall = "company_abbr_hider.install.after_uninstall"

boot_session = "company_abbr_hider.boot.boot_session"

override_whitelisted_methods = {
	"frappe.desk.query_report.export_query": "company_abbr_hider.exports.export_query_report",
	"frappe.desk.reportview.export_query": "company_abbr_hider.exports.export_report_view",
}

doc_events = {
	doctype: {
		"before_save": "company_abbr_hider.install.set_display_title",
		"after_rename": "company_abbr_hider.install.refresh_display_title_after_rename",
	}
	for doctype in ("Account", "Warehouse", "Cost Center")
}

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "company_abbr_hider",
# 		"logo": "/assets/company_abbr_hider/logo.png",
# 		"title": "Company Abbreviation Hider",
# 		"route": "/company_abbr_hider",
# 		"has_permission": "company_abbr_hider.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/company_abbr_hider/css/company_abbr_hider.css"
# app_include_js = "/assets/company_abbr_hider/js/company_abbr_hider.js"

# include js, css files in header of web template
# web_include_css = "/assets/company_abbr_hider/css/company_abbr_hider.css"
# web_include_js = "/assets/company_abbr_hider/js/company_abbr_hider.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "company_abbr_hider/public/scss/website"

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
# app_include_icons = "company_abbr_hider/public/icons.svg"

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

# automatically load and sync documents of this doctype from downstream apps
# importable_doctypes = [doctype_1]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "company_abbr_hider.utils.jinja_methods",
# 	"filters": "company_abbr_hider.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "company_abbr_hider.install.before_install"
# after_install = "company_abbr_hider.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "company_abbr_hider.uninstall.before_uninstall"
# after_uninstall = "company_abbr_hider.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "company_abbr_hider.utils.before_app_install"
# after_app_install = "company_abbr_hider.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "company_abbr_hider.utils.before_app_uninstall"
# after_app_uninstall = "company_abbr_hider.utils.after_app_uninstall"

# Build
# ------------------
# To hook into the build process

# after_build = "company_abbr_hider.build.after_build"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "company_abbr_hider.notifications.get_notification_config"

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
# 		"company_abbr_hider.tasks.all"
# 	],
# 	"daily": [
# 		"company_abbr_hider.tasks.daily"
# 	],
# 	"hourly": [
# 		"company_abbr_hider.tasks.hourly"
# 	],
# 	"weekly": [
# 		"company_abbr_hider.tasks.weekly"
# 	],
# 	"monthly": [
# 		"company_abbr_hider.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "company_abbr_hider.install.before_tests"

# Extend DocType Class
# ------------------------------
#
# Specify custom mixins to extend the standard doctype controller.
# extend_doctype_class = {
# 	"Task": "company_abbr_hider.custom.task.CustomTaskMixin"
# }

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "company_abbr_hider.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "company_abbr_hider.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["company_abbr_hider.utils.before_request"]
# after_request = ["company_abbr_hider.utils.after_request"]

# Job Events
# ----------
# before_job = ["company_abbr_hider.utils.before_job"]
# after_job = ["company_abbr_hider.utils.after_job"]

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
# 	"company_abbr_hider.auth.validate"
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

