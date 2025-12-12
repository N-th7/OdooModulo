/** @odoo-module */

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

export class InvoiceDashboard extends Component {
    static template = "custom_clients.custom_invoice_dashboard";
}

registry.category("actions").add("custom_invoice_dashboard", InvoiceDashboard);
