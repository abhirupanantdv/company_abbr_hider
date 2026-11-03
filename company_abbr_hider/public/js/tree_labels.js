(() => {
	for (const doctype of ["Account", "Warehouse", "Cost Center"]) {
		const settings = frappe.treeview_settings[doctype];
		if (!settings || !company_abbr_hider?.strip) continue;

		settings.get_label = (node) => {
			const label = company_abbr_hider.strip(node.title || node.label || "");
			return frappe.utils.escape_html(__(label));
		};
	}
})();
