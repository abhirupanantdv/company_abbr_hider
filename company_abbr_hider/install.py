import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from company_abbr_hider.labels import DISPLAY_TITLE_FIELD, TITLE_FIELDS, strip_company_abbreviations


CUSTOM_FIELDS = {
	doctype: [
		{
			"fieldname": DISPLAY_TITLE_FIELD,
			"label": "Company Abbreviation Hider Title",
			"fieldtype": "Data",
			"hidden": 1,
			"read_only": 1,
			"no_copy": 1,
			"is_system_generated": 1,
		}
	]
	for doctype in TITLE_FIELDS
}


def after_install():
	apply_display_properties()


def after_migrate():
	apply_display_properties()


def apply_display_properties():
	create_custom_fields(CUSTOM_FIELDS, update=True)

	for doctype, title_field in TITLE_FIELDS.items():
		make_property_setter(
			doctype,
			None,
			"title_field",
			title_field,
			"Data",
			for_doctype=True,
		)
		make_property_setter(
			doctype,
			None,
			"show_title_field_in_link",
			"1",
			"Check",
			for_doctype=True,
		)
		_backfill_display_titles(doctype)

	frappe.clear_cache()


def after_uninstall():
	for doctype, title_field in TITLE_FIELDS.items():
		_remove_property_setter_if_owned(doctype, "title_field", title_field)
		_remove_property_setter_if_owned(doctype, "show_title_field_in_link", "1")
		_remove_custom_title_field_if_owned(doctype)

	frappe.clear_cache()


def _remove_property_setter_if_owned(doctype: str, property_name: str, expected_value: str):
	name = f"{doctype}-main-{property_name}"
	if not frappe.db.exists("Property Setter", name):
		return

	property_setter = frappe.get_doc("Property Setter", name)
	if property_setter.value == expected_value and property_setter.is_system_generated:
		property_setter.delete(ignore_permissions=True, force=True)


def _remove_custom_title_field_if_owned(doctype: str):
	name = f"{doctype}-{DISPLAY_TITLE_FIELD}"
	if not frappe.db.exists("Custom Field", name):
		return

	custom_field = frappe.get_doc("Custom Field", name)
	if custom_field.is_system_generated:
		custom_field.delete(ignore_permissions=True, force=True)


def set_display_title(doc, method=None):
	doc.set(DISPLAY_TITLE_FIELD, strip_company_abbreviations(doc.name))


def refresh_display_title_after_rename(doc, old_name, new_name, merge=False):
	frappe.db.set_value(
		doc.doctype,
		new_name,
		DISPLAY_TITLE_FIELD,
		strip_company_abbreviations(new_name),
		update_modified=False,
	)


def _backfill_display_titles(doctype: str):
	for name in frappe.get_all(doctype, pluck="name"):
		frappe.db.set_value(
			doctype,
			name,
			DISPLAY_TITLE_FIELD,
			strip_company_abbreviations(name),
			update_modified=False,
		)
