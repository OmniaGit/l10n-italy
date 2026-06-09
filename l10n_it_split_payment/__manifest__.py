# Deprecated stub kept for the v16 -> v18 migration.
# Split payment ("Scissione pagamenti") is now handled by Odoo 18 core
# (l10n_it). This empty module defines no models, views or data; it only
# preserves the installed-module record so the database upgrade does not
# uninstall it (which would drop its orphan tables/columns).
{
    "name": "ITA - Scissione pagamenti (deprecated stub)",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "summary": "Deprecated: split payment moved to Odoo 18 core. "
    "Empty stub kept to preserve the module record during migration.",
    "author": "OmniaSolutions",
    "website": "https://www.omniasolutions.eu",
    "license": "AGPL-3",
    "depends": ["account"],
    "installable": True,
    "auto_install": False,
    "application": False,
}
