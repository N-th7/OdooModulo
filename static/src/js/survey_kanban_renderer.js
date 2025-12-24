/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";

export class SurveyKanbanRenderer extends KanbanRenderer {
    async willStart() {
        await super.willStart();
        const stats = await this.rpc("/internet_survey/stats", {});
        this.state.stats = stats;
    }
}
