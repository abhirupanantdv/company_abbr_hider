### Company Abbreviation Hider

Hides ERPNext company suffixes from user-facing Account, Warehouse, and Cost Center labels while preserving the original document names and useful numeric prefixes used by accounting and stock transactions.

The app provides clean titles in forms, links, lists, tree views, report output, report printing, and CSV/XLSX presentation exports. Query Report and Report Builder background exports use the same sanitization.

Data Import templates intentionally keep internal identifiers because changing those values would make updates and re-imports unsafe.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app company_abbr_hider
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/company_abbr_hider
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
# company_abbr_hider
