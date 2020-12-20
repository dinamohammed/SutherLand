# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
from odoo.tools.float_utils import float_round


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    one_per_month = fields.Boolean('Execute once per Month',store=True)




