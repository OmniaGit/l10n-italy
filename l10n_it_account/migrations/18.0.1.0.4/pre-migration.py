# Copyright 2026 OmniaSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
# v16 -> v18 migration helper (step 2).
#
# Archive STALE CUSTOM VIEWS left over in the database that reference fields
# removed in v18. These are views with no ir_model_data pointing at an
# installed module (Studio customisations or leftovers of v16 third-party
# modules no longer installed), so the previous cleanup in 18.0.1.0.3 - which
# only targets views owned by the deprecated l10n_it modules - cannot reach
# them.
#
# Symptom this fixes (logged on every module load until the view is archived):
#   WARNING ... odoo.modules.loading: invalid custom view(s) for model
#   project.task.type: Field "show_on_task" does not exist in model
#   "project.task.type"
#
# Odoo re-validates every active=true custom view on each load
# (ir.ui.view._validate_custom_views). The referenced field no longer exists
# in any module, so the view can never be valid again; archiving it (active =
# false) removes it from the validation tree without deleting anything.
#
# NON-DESTRUCTIVE: only flips ir_ui_view.active. Reversible by setting it back.

import logging

_logger = logging.getLogger(__name__)

# (model, field) pairs for fields removed in v18 whose stale custom views must
# be archived. arch_db is jsonb in v18, so we match on its text rendering.
STALE_CUSTOM_VIEW_FIELDS = [
    ("project.task.type", "show_on_task"),
]

def migrate(cr, version):
    # Wrapped in a savepoint so a failure here can NEVER abort the whole
    # v16->v18 upgrade transaction; the cleanup is best-effort.
    try:
        with cr.savepoint():
            archived_total = 0
            for model, field in STALE_CUSTOM_VIEW_FIELDS:
                cr.execute(
                    """
                    UPDATE ir_ui_view SET active = false
                    WHERE active = true
                      AND model = %s
                      AND arch_db::text LIKE %s
                      AND id NOT IN (
                          SELECT res_id FROM ir_model_data
                          WHERE model = 'ir.ui.view'
                            AND module IN (SELECT name FROM ir_module_module)
                      )
                    """,
                    (model, "%" + field + "%"),
                )
                if cr.rowcount:
                    _logger.info(
                        "v18 migration: archived %s stale custom view(s) for "
                        "model %s referencing removed field %r",
                        cr.rowcount,
                        model,
                        field,
                    )
                archived_total += cr.rowcount

            _logger.info(
                "v18 migration (non-destructive): archived %s stale custom "
                "view(s) referencing fields removed in v18",
                archived_total,
            )
    except Exception:
        _logger.exception(
            "v18 migration: stale-custom-view archival failed; continuing "
            "without aborting the upgrade"
        )
