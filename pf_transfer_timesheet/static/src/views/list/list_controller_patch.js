/** @odoo-module **/

import { ListController } from "@web/views/list/list_controller";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { user } from "@web/core/user";
import { onWillStart, useState } from "@odoo/owl";

patch(ListController.prototype, {
    setup() {
        super.setup(...arguments);
        this.updateTimesheetState = useState({
            isAvailable: false,
        });
        onWillStart(async () => {
            this.updateTimesheetState.isAvailable = await user.hasGroup("pf_transfer_timesheet.group_update_timesheet_project_task");
        });
    },

    getStaticActionMenuItems() {
        const items = super.getStaticActionMenuItems();
        if (this.props.resModel === "account.analytic.line") {
            items.update_timesheet = {
                isAvailable: () => this.updateTimesheetState.isAvailable,
                sequence: 60,
                icon: "fa fa-pencil-square-o",
                description: _t("Update Timesheet"),
                callback: () => {
                    // Filter out sample data record IDs (strings like 'datapoint_4')
                    const activeIds = this.model.root.selection
                        .map((r) => r.resId || r.id)
                        .filter((id) => typeof id === "number");
                    
                    if (activeIds.length === 0) {
                        return;
                    }

                    this.actionService.doAction("pf_transfer_timesheet.action_pf_update_timesheet_wizard", {
                        resIds: activeIds,
                        additionalContext: {
                            active_id: activeIds[0],
                            active_ids: activeIds,
                            active_model: this.model.root.resModel,
                        },
                        onClose: () => {
                            this.model.load();
                        },
                    });
                },
            };
        }
        return items;
    },
});
