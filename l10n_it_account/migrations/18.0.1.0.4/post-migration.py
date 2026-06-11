# Copyright 2026 OmniaSolutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
#
# v16 -> v18 migration helper (step 2, post).
#
# Deduplicate discuss_channel.uuid so v18 can create the new
# discuss_channel_uuid_unique UNIQUE(uuid) constraint. The v16 DB has
# NULL/duplicate uuids, which makes the constraint creation fail at load:
#   ERROR odoo.schema: Table 'discuss_channel': unable to add constraint
#   'discuss_channel_uuid_unique' as UNIQUE(uuid)
#
# We backfill missing uuids and regenerate duplicates here; Odoo re-attempts
# the constraint on the next load, when the data is clean. Non-destructive.

import logging

from openupgradelib import openupgrade, openupgrade_tools

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    if not openupgrade_tools.table_exists(cr, "discuss_channel"):
        return
    if not openupgrade.column_exists(cr, "discuss_channel", "uuid"):
        return

    # NULL/empty uuids -> assign a fresh one
    cr.execute(
        """
        UPDATE discuss_channel
        SET uuid = md5(random()::text || clock_timestamp()::text || id::text)
        WHERE uuid IS NULL OR uuid = ''
        """
    )
    backfilled = cr.rowcount

    # Duplicates -> keep the lowest id, regenerate the rest
    cr.execute(
        """
        UPDATE discuss_channel d
        SET uuid = md5(random()::text || clock_timestamp()::text || d.id::text)
        WHERE EXISTS (
            SELECT 1 FROM discuss_channel d2
            WHERE d2.uuid = d.uuid AND d2.id < d.id
        )
        """
    )
    deduped = cr.rowcount

    if backfilled or deduped:
        _logger.info(
            "v18 migration: discuss_channel.uuid - backfilled %s null/empty, "
            "regenerated %s duplicate(s) so the unique constraint can be added",
            backfilled,
            deduped,
        )
