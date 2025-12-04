/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { registry } from "@web/core/registry";

class SurveyKanbanRenderer extends KanbanRenderer {
    render() {
        const el = super.render(...arguments);

        // Crear el dashboard
        const dashboard = document.createElement("div");
        dashboard.classList.add("survey-dashboard");
        dashboard.style.cssText =
            "display:flex; gap:20px; margin:20px; padding:20px; background:#f8f9fa; border-radius:8px;";

        dashboard.innerHTML = `
            <div class="kpi-card" style="flex:1; background:white; padding:20px; border-radius:8px; text-align:center;">
                <div style="font-size:24px; font-weight:bold; color:#28a745;">3.8</div>
                <div style="font-size:14px; color:#888;">Promedio Satisfacción</div>
            </div>
            <div class="kpi-card" style="flex:1; background:white; padding:20px; border-radius:8px; text-align:center;">
                <div style="font-size:32px; font-weight:bold; color:#007bff;">4</div>
                <div style="color:#666;">Encuestas Positivas</div>
            </div>
            <div class="kpi-card" style="flex:1; background:white; padding:20px; border-radius:8px; text-align:center;">
                <div style="font-size:32px; font-weight:bold; color:#dc3545;">1</div>
                <div style="color:#666;">Encuestas Negativas</div>
            </div>
        `;

        // Insertar antes de las tarjetas
        el.prepend(dashboard);

        return el;
    }
}

// Registrar renderer para este modelo
registry.category("views").add("internet_survey_kanban_js", {
    ...registry.category("views").get("kanban"),
    Renderer: SurveyKanbanRenderer,
});
