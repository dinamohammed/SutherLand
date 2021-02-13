# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api, _
from odoo.exceptions import Warning, UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from odoo.tools.safe_eval import safe_eval


class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    @api.onchange('hr_trans_lines_ids')
    @api.depends('hr_trans_lines_ids.int_amount', 'hr_trans_lines_ids.ext_amount')
    def _get_total_trans_allowance(self):
        for rec in self:
            rec.total_trans_allowance = sum(l.int_amount + l.ext_amount for l in rec.hr_trans_lines_ids)
            rec.total_trans_internal = sum(l.int_amount for l in rec.hr_trans_lines_ids)
            rec.total_trans_external = sum(l.ext_amount for l in rec.hr_trans_lines_ids)

    method = fields.Selection(string="Method", selection=[('gross', 'Gross'), ('net', 'Net')], required=True,
                              default='gross')
    hr_bonus_ids = fields.One2many(comodel_name='hr.bonus.line', inverse_name='payslip_id', string="Bonuses")
    hr_penalty_ids = fields.One2many(comodel_name='hr.penalty.line', inverse_name='payslip_id', string="Penalties")
    hr_trans_lines_ids = fields.One2many(comodel_name='hr.trans.allowance.line', inverse_name='payslip_id',
                                         string="Transportation Allowance")
    hr_award_profit_ids = fields.One2many(comodel_name='hr.award.profit.line', inverse_name='payslip_id',
                                          string="Award/Profit")
    total_bonus_ids = fields.One2many(comodel_name="hr.total.bonus", inverse_name="payslip_id", string="Bonus Totals",
                                      compute='_get_hr_bonuses', store=True)
    total_penalty_ids = fields.One2many(comodel_name="hr.total.penalty", inverse_name="payslip_id",
                                        string="Penalty Totals", compute='_get_hr_penalties', store=True)

    # # Bonus Allowance
    # total_bonuses = fields.Float("Total Bonuses", compute=_get_total_bonus)
    # total_bonuses_allowance = fields.Float("Total Bonuses(Allowance)", compute=_get_total_bonus)
    # total_bonuses_rewards = fields.Float("Total Bonuses(Rewards)", compute=_get_total_bonus)
    # total_bonus_production = fields.Float("Production", compute=_get_total_bonus)
    # total_bonus_leadership = fields.Float("Leadership", compute=_get_total_bonus)
    # total_bonus_workshop = fields.Float("Workshop", compute=_get_total_bonus)
    # total_bonus_direction = fields.Float("Board of Direction", compute=_get_total_bonus)
    # # Bonus Rewards
    # total_bonus_comp_off_site = fields.Float("Comp Off Site", compute=_get_total_bonus)
    # total_bonus_comp_off_home = fields.Float("Comp Off Home", compute=_get_total_bonus)
    # total_bonus_overtime_site = fields.Float("OverTime Site", compute=_get_total_bonus)
    # total_bonus_overtime_home = fields.Float("OverTime Home", compute=_get_total_bonus)
    # total_bonus_vpp = fields.Float("VPP", compute=_get_total_bonus)
    # total_bonus_ramadan = fields.Float("Ramadan", compute=_get_total_bonus)
    # total_bonus_other = fields.Float("Other", compute=_get_total_bonus)
    # total_bonus_night_shift = fields.Float("Night Shift", compute=_get_total_bonus)
    # total_bonus_leave_balance = fields.Float("Leave Balance", compute=_get_total_bonus)
    # total_bonus_amount_vpp = fields.Float("Amount VPP", compute=_get_total_bonus)
    # # PENALTY PART
    # # ####################################################
    # total_penalties = fields.Float("Total Penalties", compute=_get_total_penalty)
    # total_penalty_other = fields.Float("Other", compute=_get_total_penalty)
    # total_penalty_absence = fields.Float("Absence", compute=_get_total_penalty)
    # total_penalty_ramadan = fields.Float("Ramadan", compute=_get_total_penalty)
    # total_penalty_advanced = fields.Float("Advanced", compute=_get_total_penalty)
    # Transportation Allowance PART
    # ####################################################0 = {tuple: 3} ('employee_id', '=', 20)
    # total_trans_allowance = fields.Float("Total Trans. Allowance", compute=_get_total_trans_allowance)
    # total_trans_internal = fields.Float("Internal", compute=_get_total_trans_allowance)
    # total_trans_external = fields.Float("External", compute=_get_total_trans_allowance)
    # total_award_profit = fields.Float("Total Award/Profit", compute=_get_total_award_profit)
    # total_award = fields.Float("Award", compute=_get_total_award_profit)
    # total_profit = fields.Float("Profit", compute=_get_total_award_profit)

    def _get_hr_bonuses(self):
        bonus_line_obj = self.env['hr.bonus.line']
        domain = []
        for payslip in self:
            if payslip.employee_id:
                domain = [('employee_id', '=', payslip.employee_id.id),
                          ('state', '=', 'confirm')]
                if payslip.date_from:
                    domain.append(('date', '>=', payslip.date_from))
                if payslip.date_to:
                    domain.append(('date', '<=', payslip.date_to))
                payslip.write({'hr_bonus_ids': [(6, 0, bonus_line_obj.search(domain).mapped('id'))]})
            # grp_bonus_lines = bonus_line_obj.read_group(domain,
            #                                             fields=['bonus_id', 'bonus_type_id', 'method', 'amount:sum'],
            #                                             groupby=['bonus_id', 'bonus_type_id', 'method'],
            #                                             orderby="bonus_type_id desc, method desc",
            #                                             lazy=False)
            # payslip.total_bonus_ids = False
            # total_list = []
            # for total in grp_bonus_lines:
            #     total_list.append((0, 0, {
            #         'bonus_id': total['bonus_id'][0],
            #         'bonus_type_id': total['bonus_type_id'][0],
            #         'method': total['method'],
            #         'total': total['amount'],
            #     }))
            # payslip.write({'total_bonus_ids': total_list})

            #
            # # total_list = []
            #
            # for total in grp_bonus_lines:
            #     # val.append((0, 0, {
            #     #     'bonus_id': 5,
            #     #     'bonus_type_id': total['bonus_type_id'][0],
            #     #     'method': total['method'],
            #     #     'total': total['amount'],
            #     # }))
            #     payslip.total_bonus_ids.create({
            #         'bonus_id': total['bonus_id'][0],
            #         'bonus_type_id': total['bonus_type_id'][0],
            #         'method': total['method'],
            #         'total': total['amount'],
            #     })
            #     # self.env.cr.commit()
            #     # total_list.append((0, 0, new_record))
            # # self.write({
            # #     'total_bonus_ids': (0, 0, total_list)
            # # })
            # # self.env.cr.commit()
            # # payslip.create({'total_bonus_ids': total_list})

    def _get_hr_penalties(self):
        penalty_line_obj = self.env['hr.penalty.line']
        for payslip in self:
            if payslip.employee_id:
                domain = [('employee_id', '=', payslip.employee_id.id), ('state', '=', 'confirm')]
                if payslip.date_from:
                    domain.append(('date', '>=', payslip.date_from))
                if payslip.date_to:
                    domain.append(('date', '<=', payslip.date_to))
                penalty_line_ids = penalty_line_obj.search(domain).mapped('id')
                payslip.write({'hr_penalty_ids': [(6, 0, penalty_line_ids)]})

    def _get_hr_trans_allowance(self):
        trans_line_obj = self.env['hr.trans.allowance.line']
        for payslip in self:
            if payslip.employee_id:
                domain = [('employee_id', '=', payslip.employee_id.id),
                          ('state', '=', 'confirm')]
                if payslip.date_from:
                    domain.append(('date', '>=', payslip.date_from))
                if payslip.date_to:
                    domain.append(('date', '<=', payslip.date_to))
                payslip.write({'hr_trans_lines_ids': [(6, 0, trans_line_obj.search(domain).mapped('id'))]})

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        super(HrPayslipInherit, self)._onchange_employee()
        self._get_hr_bonuses()
        self._get_hr_penalties()
        self._get_hr_trans_allowance()
        self._get_hr_award_profit()

    def action_payslip_done(self):
        """
        Append Function to add extra action action_set_line_confirm
        :return: SUPER
        """
        lines_dicts = [{'lines': self.hr_bonus_ids, 'inverse_name': 'bonus_id'},
                       {'lines': self.hr_penalty_ids, 'inverse_name': 'penalty_id'},
                       {'lines': self.hr_award_profit_ids, 'inverse_name': 'award_profit_id'},
                       {'lines': self.hr_trans_lines_ids, 'inverse_name': 'trans_id'}]
        for lines_dict in lines_dicts:
            self.action_set_line_confirm(lines_dict)
        return super(HrPayslipInherit, self).action_payslip_done()

    def action_set_line_confirm(self, lines_dict):
        """
        Change State of this field lines to done to avoid using it on another payslip
        :param lines_dict: one2many field of those lines
        """
        for line in lines_dict['lines']:
            line.write({'state': 'done'})
            main_field = getattr(line, lines_dict['inverse_name'])
            if all(state == 'done' for state in main_field.bonus_line_ids.mapped('state')):
                main_field.write({'state': 'done'})

    def default_action_payslip_done(self):
        if any(slip.state == 'cancel' for slip in self):
            raise ValidationError(_("You can't validate a cancelled payslip."))
        self.write({'state': 'done'})
        self.mapped('payslip_run_id').action_close()
        if self.env.context.get('payslip_generate_pdf'):
            for payslip in self:
                if not payslip.struct_id or not payslip.struct_id.report_id:
                    report = self.env.ref('hr_payroll.action_report_payslip', False)
                else:
                    report = payslip.struct_id.report_id
                pdf_content, content_type = report.render_qweb_pdf(payslip.id)
                if payslip.struct_id.report_id.print_report_name:
                    pdf_name = safe_eval(payslip.struct_id.report_id.print_report_name, {'object': payslip})
                else:
                    pdf_name = _("Payslip")
                self.env['ir.attachment'].create({
                    'name': pdf_name,
                    'type': 'binary',
                    'datas': base64.encodestring(pdf_content),
                    'res_model': payslip._name,
                    'res_id': payslip.id
                })

    def _get_hr_award_profit(self):
        line_obj = self.env['hr.award.profit.line']
        for payslip in self:
            if payslip.employee_id:
                domain = [('employee_id', '=', payslip.employee_id.id), ('state', '=', 'confirm')]
                if payslip.date_from:
                    domain.append(('date', '>=', payslip.date_from))
                if payslip.date_to:
                    domain.append(('date', '<=', payslip.date_to))
                payslip.write({'hr_award_profit_ids': [(6, 0, line_obj.search(domain).mapped('id'))]})

    # Collect Report Data
    def get_salary_rules(self):
        salary_rules = []
        for payslip_id in self:
            for line in payslip_id.line_ids:
                if line.total and line.salary_rule_id.appears_on_payslip \
                        and line.salary_rule_id.id not in salary_rules:
                    salary_rules.append(line.salary_rule_id.id)
        return salary_rules

    def assign_parents_and_free_rules(self):
        """
        Get payslips rules and seprate them according to parent
        :return:
        - dict of parent and it's rules ids
        - list of rules ids which have no parents
        """
        salary_rules_obj = self.env['hr.salary.rule']
        salary_rules = self.get_salary_rules()
        salary_rule_ids = salary_rules_obj.browse(salary_rules).sorted(lambda l: l.sequence)
        salary_rule_parent = {}
        rules_without_parent = []
        for rule in salary_rule_ids:
            if rule.parent_id:
                if rule.parent_id.id in salary_rule_parent.keys():
                    # Parent Exist collect rules
                    if rule.id not in salary_rule_parent[rule.parent_id.id]:
                        salary_rule_parent[rule.parent_id.id].append(rule.id)
                else:
                    # new parent
                    salary_rule_parent[rule.parent_id.id] = [rule.id]
            else:
                # fill list of rules without parents
                rules_without_parent.append(rule.id)
        return salary_rule_parent, rules_without_parent

    def get_rule_parents_and_free(self, parent=False):
        """
        This will return object of parents and rules
        :param parent:
        :return:
        """
        salary_rule_parent_obj = self.env['hr.salary.rule.parent']
        salary_rules_obj = self.env['hr.salary.rule']
        salary_rule_parent, rules_without_parent = self.assign_parents_and_free_rules()
        parents = salary_rule_parent_obj.browse([r for r in salary_rule_parent])
        if parent:
            return parents.mapped('name')
        else:
            return salary_rules_obj.browse(rules_without_parent).mapped('name')

    def get_parent_amount(self, salary_rule_parent):
        payslip_line_obj = self.env['hr.payslip.line']
        list_of_totals = []
        for parent in salary_rule_parent:
            total = sum(l.total for l in payslip_line_obj.search([('salary_rule_id', 'in', salary_rule_parent[parent]),
                                                                  ('slip_id', 'in', self.ids)]))
            list_of_totals.append(round(total, 2))
        return list_of_totals

    def get_free_rule_amount(self, rules_without_parent):
        payslip_line_obj = self.env['hr.payslip.line']
        list_of_totals = []
        for rule in rules_without_parent:
            total = sum(l.total for l in payslip_line_obj.search([('salary_rule_id', '=', rule),
                                                                  ('slip_id', 'in', self.ids)]))
            list_of_totals.append(round(total, 2))
        return list_of_totals

    # @api.onchange('hr_award_profit_ids')
    # @api.depends('hr_award_profit_ids.amount')
    # def _get_total_award_profit(self):
    #     for rec in self:
    #         rec.total_award_profit = sum(l.amount for l in rec.hr_award_profit_ids)
    #         rec.total_award = sum(l.amount for l in
    #                               rec.hr_award_profit_ids.filtered(lambda x: x.award_profit_id.extra_type == 'award'))
    #         rec.total_profit = sum(l.amount for l in
    #                                rec.hr_award_profit_ids.filtered(lambda x: x.award_profit_id.extra_type == 'profit'))

    # @api.onchange('hr_bonus_ids')
    # @api.depends('hr_bonus_ids.amount')
    # def _get_total_bonus(self):
    #     # Bonus Allowance
    #     bonus_production = self.env.ref('egymentors_hr.bonus_production')
    #     bonus_leadership = self.env.ref('egymentors_hr.bonus_leadership')
    #     bonus_board_of_direction = self.env.ref('egymentors_hr.bonus_board_of_direction')
    #     bonus_workshop = self.env.ref('egymentors_hr.bonus_workshop')
    #     # Bonus Reward
    #     bonus_comp_off_site = self.env.ref('egymentors_hr.bonus_comp_off_site')
    #     bonus_comp_off_home = self.env.ref('egymentors_hr.bonus_comp_off_home')
    #     bonus_overtime_site = self.env.ref('egymentors_hr.bonus_overtime_site')
    #     bonus_overtime_home = self.env.ref('egymentors_hr.bonus_overtime_home')
    #     bonus_vpp = self.env.ref('egymentors_hr.bonus_vpp')
    #     bonus_ramadan = self.env.ref('egymentors_hr.bonus_ramadan')
    #     bonus_other = self.env.ref('egymentors_hr.bonus_other')
    #     bonus_night_shift = self.env.ref('egymentors_hr.bonus_night_shift')
    #     bonus_leave_balance = self.env.ref('egymentors_hr.bonus_leave_balance')
    #     bonus_amount_vpp = self.env.ref('egymentors_hr.bonus_amount_vpp')
    #
    #     for rec in self:
    #         rec.total_bonuses = sum(l.amount for l in rec.hr_bonus_ids)
    #         # Allowance
    #         rec.total_bonus_production = sum(l.amount for l in
    #                                          rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_production))
    #         rec.total_bonus_leadership = sum(l.amount for l in
    #                                          rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_leadership))
    #         rec.total_bonus_workshop = sum(l.amount for l in
    #                                        rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_workshop))
    #         rec.total_bonus_direction = sum(l.amount for l in
    #                                         rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_board_of_direction))
    #         rec.total_bonuses_allowance = sum(l.amount for l in
    #                                           rec.hr_bonus_ids.filtered(lambda x: x.type_id.bonus_type == 'allowance'))
    #         # Rewards
    #         rec.total_bonus_comp_off_site = sum(l.amount for l in
    #                                             rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_comp_off_site))
    #         rec.total_bonus_comp_off_home = sum(l.amount for l in
    #                                             rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_comp_off_home))
    #         rec.total_bonus_overtime_site = sum(l.amount for l in
    #                                             rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_overtime_site))
    #         rec.total_bonus_overtime_home = sum(l.amount for l in
    #                                             rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_overtime_home))
    #         rec.total_bonus_vpp = sum(l.amount for l in
    #                                   rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_vpp))
    #         rec.total_bonus_ramadan = sum(l.amount for l in
    #                                       rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_ramadan))
    #         rec.total_bonus_other = sum(l.amount for l in
    #                                     rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_other))
    #         rec.total_bonus_night_shift = sum(l.amount for l in
    #                                           rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_night_shift))
    #         rec.total_bonus_leave_balance = sum(l.amount for l in
    #                                             rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_leave_balance))
    #         rec.total_bonus_amount_vpp = sum(l.amount for l in
    #                                          rec.hr_bonus_ids.filtered(lambda x: x.type_id == bonus_amount_vpp))
    #
    #         rec.total_bonuses_rewards = sum(l.amount for l in rec.hr_bonus_ids.
    #                                         filtered(lambda x: x.type_id.bonus_type == 'rewards'))

    # @api.onchange('hr_penalty_ids')
    # @api.depends('hr_penalty_ids.days_num')
    # def _get_total_penalty(self):
    #     # Penalty
    #     penalty_other = self.env.ref('egymentors_hr.penalty_other')
    #     penalty_ramadan = self.env.ref('egymentors_hr.penalty_ramadan')
    #     penalty_absence = self.env.ref('egymentors_hr.penalty_absence')
    #     penalty_advanced = self.env.ref('egymentors_hr.penalty_advanced')
    #     for rec in self:
    #         rec.total_penalties = sum(l.days_num for l in rec.hr_penalty_ids)
    #         # Penalty
    #         rec.total_penalty_other = sum(l.days_num for l in
    #                                       rec.hr_penalty_ids.filtered(lambda x: x.type_id == penalty_other))
    #         rec.total_penalty_absence = sum(l.days_num for l in
    #                                         rec.hr_penalty_ids.filtered(lambda x: x.type_id == penalty_absence))
    #         rec.total_penalty_ramadan = sum(l.days_num for l in
    #                                         rec.hr_penalty_ids.filtered(lambda x: x.type_id == penalty_ramadan))
    #         rec.total_penalty_advanced = sum(l.days_num for l in
    #                                          rec.hr_penalty_ids.filtered(lambda x: x.type_id == penalty_advanced))


class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'

    all_employees = fields.Boolean('All Employees', default=False)

    work_location_id = fields.Many2one('hr.location', "Work Location")
    company_id = fields.Many2one('res.company', string='Company')
    department_id = fields.Many2one('hr.department', "Department")

