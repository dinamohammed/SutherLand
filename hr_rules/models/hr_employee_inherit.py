# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.tools.float_utils import float_round
from odoo.osv import expression


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    state_id = fields.Many2one('res.country.state', "State",
                               domain=['|', ('country_id.name', '=', "Egypt"),
                                       ('country_id.name', '=', "مصر")])

    extra_remaining_leaves = fields.Integer(string='Relay Leave Balance')

    provin_city_id = fields.Many2one('provin.city.mode',string='Billability')

    percentage_tax = fields.Float(string='Percentage Tax')

    accumlated_tax_base = fields.Float(string='Accumlated Tax Base')

    age = fields.Integer(string='Age', store=True, compute='_compute_age')

    remaining_leaves = fields.Float('Remaining Leaves', compute='_compute_remaining_leaves')

    registration_number = fields.Char('Employee Number', default='/', readonly=False, select=True, copy=False)

    @api.model
    def create(self, vals):
        """
        Add new option to get sequence automatic of Employee number
        :param vals:
        :return:
        """
        if vals.get('registration_number') == '/':
                vals['registration_number'] = self.env['ir.sequence'].next_by_code('employee.number') or '/'
        result = super(HrEmployeeInherit, self).create(vals)

        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('registration_number', operator, name)]
        employee_ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(employee_ids).with_user(name_get_uid))

    @api.depends('birthday')
    def _compute_age(self):
        diff = 0
        for employee in self:
            if employee.birthday:
                y1 = employee.birthday.strftime("%Y")
                y2 = datetime.today().strftime("%Y")
                m1 = employee.birthday.strftime("%m")
                m2 = datetime.today().strftime("%m")
                d1 = employee.birthday.strftime("%d")
                d2 = datetime.today().strftime("%d")
                if (m2, d2) < (m1, d1):
                    diff = 1
                employee.age = int(y2) - int(y1) - diff

    @api.onchange('birthday')
    def _onchange_birth_date(self):
        diff = 0
        for employee in self:
            if employee.birthday:
                y1 = employee.birthday.strftime("%Y")
                y2 = datetime.today().strftime("%Y")
                m1 = employee.birthday.strftime("%m")
                m2 = datetime.today().strftime("%m")
                d1 = employee.birthday.strftime("%d")
                d2 = datetime.today().strftime("%d")
                if (m2, d2) < (m1, d1):
                    diff = 1
                employee.age = int(y2) - int(y1) - diff

    def _get_remaining_leaves(self):
        """ Helper to compute the remaining leaves for the current employees
            :returns dict where the key is the employee id, and the value is the remain leaves
        """
        self._cr.execute("""
                SELECT
                    sum(h.number_of_days) AS days,
                    h.employee_id
                FROM
                    (
                        SELECT holiday_status_id, number_of_days,
                            state, employee_id
                        FROM hr_leave_allocation
                        UNION ALL
                        SELECT holiday_status_id, (number_of_days * -1) as number_of_days,
                            state, employee_id
                        FROM hr_leave
                    ) h
                    join hr_leave_type s ON (s.id=h.holiday_status_id)
                WHERE
                    s.active = true AND h.state='validate' AND
                    (s.allocation_type='fixed' OR s.allocation_type='fixed_allocation') AND
                    h.employee_id in %s
                GROUP BY h.employee_id""", (tuple(self.ids),))
        return dict((row['employee_id'], row['days']) for row in self._cr.dictfetchall())

    def _compute_remaining_leaves(self):
        remaining = self._get_remaining_leaves()
        for employee in self:
            value = float_round(remaining.get(employee.id, 0.0), precision_digits=2)
            employee.leaves_count = value
            employee.remaining_leaves = value
