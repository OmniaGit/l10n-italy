#  Copyright 2021 Simone Rubino - Agile Business Group
#  License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    views_xmlids = [
        "view_form_report_intrastat_code",
        "view_tree_report_intrastat_code",
    ]
    for view_xmlid in views_xmlids:
        full_xml_id = ".".join(["l10n_it_intrastat", view_xmlid])
        view = env.ref(full_xml_id)
        view.inherit_id = False
