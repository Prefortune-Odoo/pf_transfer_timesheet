import { ActionMenus } from "@web/search/action_menus/action_menus";
import { patch } from "@web/core/utils/patch";

patch(ActionMenus.prototype, {
    async getActionItems(props) {
        const items = await super.getActionItems(props);
        for (const item of items) {
            if (item.action && item.action.icon) {
                item.icon = item.action.icon;
            }
        }
        return items;
    }
});
