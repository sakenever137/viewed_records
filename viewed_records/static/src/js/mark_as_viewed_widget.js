/** @odoo-module **/
import { registry } from '@web/core/registry';
import { formView } from "@web/views/form/form_view";

export class MarkAsViewedFormController extends formView.Controller {
    setup() {
        super.setup();
        this.mark_as_viewed();
    }

    async mark_as_viewed() {
        if (!this.props.resId || !this.props.resModel) {
            return;
        }
        await this.orm.call(this.props.resModel, "mark_as_viewed", [this.props.resId, this.props.resModel] );
    }
}


export const markAsViewedFormView = {
    ...formView,
    Controller: MarkAsViewedFormController,
};

registry.category("views").add("viewed_records", markAsViewedFormView);
