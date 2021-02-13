# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

_STATES = [('draft', 'Draft'), ('confirm', 'Confirmed'), ('done', 'Done'), ('cancel', 'Cancelled')]


class HRPenalty(models.Model):
    _name = 'hr.penalty'
    _description = 'HR Penalty'
    _inherit = ['mail.thread', 'image.mixin']

    name = fields.Char(string="Name", translate=True)
    penalty_categ_id = fields.Many2one(comodel_name="hr.penalty.categ", string="Penalty Category")
    date = fields.Date(string="Date", default=fields.Date.today(), readonly=True,
                       states={'draft': [('readonly', False)]})
    fixed_amount = fields.Boolean("Fixed Amount", readonly=True, states={'draft': [('readonly', False)]})
    date_to = fields.Date("To Date", readonly=True, states={'draft': [('readonly', False)]})
    period_month = fields.Char(string="Period Month", default=lambda x: fields.Date.today().strftime("%B"),
                               readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(_STATES, default='draft', string="Stage", track_visibility='onchange')
    penalty_line_ids = fields.One2many(comodel_name="hr.penalty.line", inverse_name="penalty_id",
                                       string="Penalty Lines", readonly=True, states={'draft': [('readonly', False)]})
    total_penalty_ids = fields.One2many(comodel_name="hr.total.penalty", inverse_name="penalty_id",
                                        string="Penalty Totals", compute='_compute_total_penalty', store=True)

    @api.depends('penalty_line_ids')
    def _compute_total_penalty(self):
        """
        This function computes group of totals based on the penalty type and the method used in the penalty line.
        """
        if self.penalty_line_ids:
            for rec in self:
                grp_penalty_lines = self.env['hr.penalty.line'].read_group([('penalty_id', '=', self._origin.id)],
                                                                           fields=['penalty_type_id', 'method',
                                                                                   'amount:sum'],
                                                                           groupby=['penalty_type_id', 'method'],
                                                                           orderby="penalty_type_id desc, method desc",
                                                                           lazy=False)
                rec.total_penalty_ids = False
                val = []
                for total in grp_penalty_lines:
                    val.append((0, 0, {
                        'penalty_id': self._origin.id,
                        'penalty_type_id': total['penalty_type_id'][0],
                        'method': total['method'],
                        'total': total['amount'],
                    }))
                rec.total_penalty_ids = val

    def action_confirm(self):
        """
        This function calls `_change_state` that changes the state to be "Confirmed".
        """
        for action in self:
            action._change_state('confirm')

    def _change_state(self, state):
        """
         This function changes the state of the line to be as given in the parameter.
        :param state: The state of the line that will be changed to.
        """
        self.write({'state': state})
        for line in self.penalty_line_ids:
            line.write({'state': state})

    def action_print_report(self):
        """
        This function prints the penalty report.
        """
        return self.env.ref('egymentors_hr.hr_penalty_report').report_action(self)

    def action_cancel(self):
        """
        This function cancels the penalty by calling the function `_change_state` and changes the state to cancel.
        """
        for action in self:
            action._change_state('cancel')

    def unlink(self):
        """
        This function unlink the penalty, but if the state of the it is confirmed, it will raise warning.
        """
        for rec in self:
            if rec.state == 'confirm':
                raise Warning(_("You can't delete confirmed records!!!"))
        return super(HRPenalty, self).unlink()

    def action_reset(self):
        """
        This function reset the penalty and changes its state to draft.
        :return:
        """
        for action in self:
            action._change_state('draft')


class HRPenaltyLine(models.Model):
    _name = 'hr.penalty.line'
    _description = 'HR Penalty Line'

    name = fields.Char(string="Name")
    penalty_id = fields.Many2one(comodel_name='hr.penalty', string="Penalty")
    payslip_id = fields.Many2one(comodel_name='hr.payslip', string="Payslip")
    date = fields.Date(related='penalty_id.date')
    employee_id = fields.Many2one(comodel_name='hr.employee', string="Employee", required=True)
    penalty_type_id = fields.Many2one(comodel_name='hr.penalty.type', string="Type", required=True)
    method = fields.Selection(string="Method", selection=[('gross', 'Gross'), ('net', 'Net')], required=True,
                              default='gross')
    amount = fields.Float(string="Amount")
    notes = fields.Text(string="Notes")
    state = fields.Selection(_STATES, default='draft', string="Stage", track_visibility='onchange')


class HRPenaltyType(models.Model):
    _name = 'hr.penalty.type'
    _description = 'HR Penalty Type'

    name = fields.Char(string="Name")
    penalty_categ_id = fields.Many2one(comodel_name="hr.penalty.categ", string="Penalty Category", required=True)
    code = fields.Char(string="Code", required=True, )


class HRPenaltyCategory(models.Model):
    _name = 'hr.penalty.categ'
    _description = 'HR Penalty Category'

    name = fields.Char(string="Name")


class HRTotalPenalty(models.Model):
    _name = 'hr.total.penalty'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char()
    penalty_id = fields.Many2one(comodel_name='hr.penalty', string="Penalty")
    payslip_id = fields.Many2one(comodel_name='hr.payslip', string="Payslip")
    method = fields.Selection(string="Method", selection=[('gross', 'Gross'), ('net', 'Net')], required=True,
                              default='gross')
    penalty_type_id = fields.Many2one(comodel_name='hr.penalty.type', string="Penalty Type", required=True)
    total = fields.Float(string="Total")
