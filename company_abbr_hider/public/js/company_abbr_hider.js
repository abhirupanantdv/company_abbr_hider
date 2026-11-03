frappe.provide("company_abbr_hider");

(() => {
	const config = frappe.boot.company_abbr_hider || {};
	const abbreviations = [...(config.abbreviations || [])].sort((a, b) => b.length - a.length);
	const display_doctypes = new Set(config.display_doctypes || []);
	const display_fieldnames = new Set([
		"account",
		"account_name",
		"account_head",
		"against",
		"against_account",
		"parent_account",
		"warehouse",
		"warehouse_name",
		"parent_warehouse",
		"source_warehouse",
		"target_warehouse",
		"from_warehouse",
		"to_warehouse",
		"s_warehouse",
		"t_warehouse",
		"cost_center",
		"cost_center_name",
		"parent_cost_center",
	]);

	const escaped = abbreviations.map((value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
	const suffix_pattern = escaped.length
		? new RegExp(`\\s-\\s(?:${escaped.join("|")})(?=$|[\\s,;:/|)\\]}"'<])`, "g")
		: null;

	company_abbr_hider.strip = (value) => {
		if (typeof value !== "string" || !suffix_pattern) return value;
		return value.replace(suffix_pattern, "");
	};

	company_abbr_hider.strip_html_text = (value) => {
		if (typeof value !== "string" || !value.includes("<")) {
			return company_abbr_hider.strip(value);
		}

		const template = document.createElement("template");
		template.innerHTML = value;
		const walker = document.createTreeWalker(template.content, NodeFilter.SHOW_TEXT);
		let node;
		while ((node = walker.nextNode())) {
			node.nodeValue = company_abbr_hider.strip(node.nodeValue);
		}
		return template.innerHTML;
	};

	const should_clean = (df = {}) => {
		const linked_doctype = df._options || df.options;
		return display_doctypes.has(linked_doctype) || display_fieldnames.has(df.fieldname);
	};

	for (const doctype of display_doctypes) {
		const existing_formatter = frappe.form.link_formatters[doctype];
		frappe.form.link_formatters[doctype] = (value, doc, docfield) => {
			const formatted = existing_formatter
				? existing_formatter(value, doc, docfield)
				: value;
			return company_abbr_hider.strip(formatted);
		};
	}

	if (!frappe.format.__company_abbr_hider_wrapped) {
		const original_format = frappe.format;
		const wrapped_format = function (value, df, options, doc) {
			const formatted = original_format.call(this, value, df, options, doc);
			return should_clean(df) ? company_abbr_hider.strip_html_text(formatted) : formatted;
		};
		wrapped_format.__company_abbr_hider_wrapped = true;
		frappe.format = wrapped_format;
	}
})();
