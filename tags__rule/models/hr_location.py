# -*- coding: utf-8 -*-

from odoo import models, fields


class HrLocation(models.Model):
    _name = 'hr.location'
    _description = "Program"
    _inherit = ['mail.thread']
    
    name = fields.Char(string="Work Location", required=True)
    code = fields.Char(string="Location Code", required=True)

class EmployeeStatus(models.Model):
    _name = 'employee.status'
    _inherit = ['mail.thread']
    _description = "Employee Status"

    name = fields.Char(string="Employee Status", required=True)
    code = fields.Char(string="Status Code", required=True)