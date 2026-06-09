# Deprecated stub kept for the v16 -> v18 migration.
# Reverse charge ("Inversione contabile") is now handled by Odoo 18 core
# (l10n_it / l10n_it_edi). This empty module defines no models, views or
# data; it only preserves the installed-module record so the database
# upgrade does not uninstall it (which would drop its orphan tables/columns).
{
    "name": "ITA - Inversione contabile (deprecated stub)",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Deprecated: reverse charge moved to Odoo 18 core. "
    "Empty stub kept to preserve the module record during migration.",
    "author": "OmniaSolutions",
    "website": "https://www.omniasolutions.eu",
    "license": "AGPL-3",
    "depends": ["account"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
