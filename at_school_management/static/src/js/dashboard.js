/** @odoo-module **/

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

class StudentDashboard extends Component {

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            student_count: 0,
            fee_total: 0,
            fee_paid: 0,
            fee_pending: 0,
            company_name: "",
            currency_symbol: "",
            academic_years: [],
            selected_year_id: null,
        });

        onWillStart(async () => {
            await this.loadAcademicYears();
            await this.loadData();
        });
    }

    async loadAcademicYears() {
        const years = await this.orm.searchRead(
            "school.academic.year",
            [],
            ["name"]
        );

        this.state.academic_years = years;

        if (years.length) {
            this.state.selected_year_id = years[0].id; // default
        }
    }

    async loadData() {

        const domain = this.state.selected_year_id
            ? [["academic_id", "=", this.state.selected_year_id]]
            : [];

        const company = await this.orm.searchRead(
            "res.company",
            [],
            ["name"]
        );

        const currency = await this.orm.searchRead(
            "res.currency",
            [],
            ["symbol"]
        );

        const student_count = await this.orm.searchCount("school.student", []);
        const fees = await this.orm.searchRead("school.fee.payment", domain, ["total_amount", "amount_paid", "balance_amount"]);

        let total = 0, paid = 0, pending = 0;
        fees.forEach(f => { total += f.total_amount; paid += f.amount_paid; pending += f.balance_amount; });

        this.state.student_count = student_count;
        this.state.fee_total = total;
        this.state.fee_paid = paid;
        this.state.fee_pending = pending;

        this.state.company_name = company[0].name;
        this.state.currency_symbol = currency[0].symbol;
    }

    openStudents() {
        this.action.doAction("at_school_management.action_school_student");
    }

    openFees() {
        this.action.doAction("at_school_management.action_school_fee_payment");
    }

    onYearChange(ev) {
        this.state.selected_year_id = parseInt(ev.target.value);
        this.loadData();  // reload dashboard
    }

}

StudentDashboard.template = "student_fee_dashboard";

registry.category("actions").add("student_fee_dashboard", StudentDashboard);