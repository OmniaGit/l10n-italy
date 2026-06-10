# Deprecated stub kept for the v16 -> v18 migration.
# Payment-time withholding is now handled by Odoo 18 core. This empty
# module preserves the installed-module record so the database upgrade
# does not uninstall it (keeping its data as orphan instead).
{
    "name": "ITA - Ritenuta d'acconto - Pagamenti (deprecated stub)",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Deprecated: moved to Odoo 18 core. "
    "Empty stub kept to preserve the module record during migration.",
    "author": "OmniaSolutions",
    "website": "https://www.omniasolutions.eu",
    "license": "AGPL-3",
    "depends": ["account", "l10n_it_withholding_tax"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
