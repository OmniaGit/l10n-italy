# Copyright 2026 OmniaSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
# v16 -> v18 migration helper. Runs before l10n_it_account loads its own
# views (and before later modules), to neutralise the leftovers of the
# deprecated v16 l10n_it modules that would otherwise break - or silently
# destroy data during - the upgrade build.
#
# IMPORTANT: this script is fully NON-DESTRUCTIVE. It only updates flags
# (ir_ui_view.active, ir_ui_menu.active, ir_model_data.noupdate). It never
# deletes a view, menu, model, field, table, column or external-id.
#
# It does three things:
#
# 1) Archive obsolete VIEWS (active = false) so they are excluded from the
#    inheritance/validation tree (they reference fields removed in v18, e.g.
#    res.partner.electronic_invoice_obliged_subject).
#
# 2) Archive obsolete MENUS (active = false) so the deprecated modules' dead
#    menu items do not show in the v18 UI.
#
# 3) Set noupdate = TRUE on the deprecated modules' external-ids. The
#    deprecated modules now ship as empty stubs, so at the end of the load
#    Odoo's _process_end() would try to DELETE every record they used to own.
#    That deletion (a) crashes on a foreign-key violation when an obsolete
#    view is still inherited by another obsolete view, and (b) DROPS the data
#    tables/columns of the deprecated models (withholding.tax.statement = 16
#    rows, account.rc.type = 5 rows, declaration_of_intent = 1 row,
#    payment.reason = 28 rows, ...). _process_end() only removes records whose
#    ir_model_data has "noupdate = false", so flipping noupdate to true makes
#    it skip them entirely - nothing is deleted, everything is preserved, and
#    the change is reversible (set noupdate back to false to allow cleanup).

import logging

_logger = logging.getLogger(__name__)

# Deprecated v16 l10n_it modules (28, all verified absent as real v18 modules)
DEPRECATED_MODULES = [
    "l10n_it_fatturapa",
    "l10n_it_fatturapa_in",
    "l10n_it_fatturapa_out",
    "l10n_it_fatturapa_in_rc",
    "l10n_it_fatturapa_in_purchase",
    "l10n_it_fatturapa_out_di",
    "l10n_it_fatturapa_out_rc",
    "l10n_it_fatturapa_out_sp",
    "l10n_it_fatturapa_out_stamp",
    "l10n_it_fatturapa_out_wt",
    "l10n_it_fatturapa_sale",
    "l10n_it_fatturapa_export_zip",
    "l10n_it_fatturapa_pec",
    "l10n_it_sdi_channel",
    "l10n_it_fiscalcode",
    "l10n_it_fiscal_document_type",
    "l10n_it_fiscal_payment_term",
    "l10n_it_ipa",
    "l10n_it_rea",
    "l10n_it_vat_payability",
    "l10n_it_account_tax_kind",
    "l10n_it_withholding_tax",
    "l10n_it_withholding_tax_payment",
    "l10n_it_withholding_tax_reason",
    "l10n_it_payment_reason",
    "l10n_it_reverse_charge",
    "l10n_it_split_payment",
    "l10n_it_declaration_of_intent",
]

# Stale views from KEPT modules; reactivated by their own v18 code.
STALE_KEPT_VIEWS = [
    ("plm_license_management", "website_sale_cart_line_plm_license_uuid"),
]


def migrate(cr, version):
    # 1) Archive obsolete views owned by deprecated modules
    cr.execute(
        """
        UPDATE ir_ui_view SET active = false
        WHERE active = true
          AND id IN (SELECT res_id FROM ir_model_data
                     WHERE model = 'ir.ui.view' AND module = ANY(%s))
        """,
        (DEPRECATED_MODULES,),
    )
    archived_views = cr.rowcount

    # 1b) Archive stale website_sale cart view(s) from kept modules
    archived_kept = 0
    if STALE_KEPT_VIEWS:
        cr.execute(
            """
            UPDATE ir_ui_view SET active = false
            WHERE active = true
              AND id IN (SELECT res_id FROM ir_model_data
                         WHERE model = 'ir.ui.view' AND (module, name) IN %s)
            """,
            (tuple(STALE_KEPT_VIEWS),),
        )
        archived_kept = cr.rowcount

    # 2) Archive deprecated menus so they don't show in the v18 UI
    cr.execute(
        """
        UPDATE ir_ui_menu SET active = false
        WHERE active = true
          AND id IN (SELECT res_id FROM ir_model_data
                     WHERE model = 'ir.ui.menu' AND module = ANY(%s))
        """,
        (DEPRECATED_MODULES,),
    )
    archived_menus = cr.rowcount

    # 2c) Unbind deprecated WINDOW ACTIONS (clear binding_model_id) so they
    #     stop being injected into the v18 "Action" (gear) menu of kept models.
    #     The deprecated modules bound actions to still-live models (e.g.
    #     l10n_it_fatturapa_out.action_wizard_export_fatturapa -> account.move),
    #     but their target res_model (wizard.export.fatturapa, ...) no longer
    #     exists in code. Archiving views/menus does NOT remove these bindings,
    #     so the orphan action keeps appearing and opening it raises
    #     KeyError -> "404 Not Found" (registry has no such model).
    #     Non-destructive: the action record is kept (noupdate-protected in
    #     step 3); only the binding columns are cleared.
    cr.execute(
        """
        UPDATE ir_act_window SET binding_model_id = NULL,
                                 binding_view_types = NULL
        WHERE binding_model_id IS NOT NULL
          AND id IN (SELECT res_id FROM ir_model_data
                     WHERE model = 'ir.actions.act_window' AND module = ANY(%s))
        """,
        (DEPRECATED_MODULES,),
    )
    unbound_actions = cr.rowcount

    # 3) Protect every deprecated external-id from _process_end deletion by
    #    flipping noupdate to true (non-destructive: nothing is removed).
    cr.execute(
        """
        UPDATE ir_model_data SET noupdate = true
        WHERE module = ANY(%s) AND COALESCE(noupdate, false) = false
        """,
        (DEPRECATED_MODULES,),
    )
    protected = cr.rowcount

    _logger.info(
        "v18 migration (non-destructive): archived %s deprecated + %s kept "
        "views, %s menus; unbound %s deprecated window actions; set "
        "noupdate=true on %s external-ids to protect records/tables from "
        "_process_end cleanup",
        archived_views,
        archived_kept,
        archived_menus,
        unbound_actions,
        protected,
    )
