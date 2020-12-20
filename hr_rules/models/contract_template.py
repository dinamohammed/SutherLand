# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import Warning


class ContractTemplate(models.Model):
	_name = 'contract.template'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = "HR Contract Template"
	
	name = fields.Char(string='Template Name', track_visibility='onchange')
	allowance_ids = fields.Many2many('allowance.hr', 'contract_template_allowance_rel',
	                                 'template_id', 'allowance_id', string='Allowances', track_visibility='onchange')
	deduction_ids = fields.Many2many('deduction.hr', 'contract_template_deduction_rel',
	                                 'template_id', 'deduction_id', string='Deductions', track_visibility='onchange')


class AllowanceHr(models.Model):
	_name = 'allowance.hr'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = "HR Contract Template Allowance"
	
	name = fields.Char(string='Allowance Type', track_visibility='onchange', require=True)
	value = fields.Float(string='Value', track_visibility='onchange', require=True)
	code = fields.Char("Code", require=True, copy=False)
	
	@api.constrains('code')
	def _unique_code(self):
		for rec in self:
			if rec.code and isinstance(rec.id, int):
				other_ids = self.env['allowance.hr'].search([('code', '=', rec.code), ('id', '!=', rec.id)])
				if other_ids:
					raise Warning(_("You can't have 2 allowance with same code"))


class DeductionHr(models.Model):
	_name = 'deduction.hr'
	_inherit = ['mail.thread', 'mail.activity.mixin']
	_description = "HR Contract Template Deductions"
	
	name = fields.Char(string='Deduction Type', track_visibility='onchange', require=True)
	value = fields.Float(string='Value', track_visibility='onchange', require=True)
	code = fields.Char("Code", require=True, copy=False)
	
	@api.constrains('code')
	def _unique_code(self):
		for rec in self:
			if rec.code and isinstance(rec.id, int):
				other_ids = self.env['allowance.hr'].search([('code', '=', rec.code), ('id', '!=', rec.id)])
				if other_ids:
					raise Warning(_("You can't have 2 allowance with same code"))


class HrContractInherit(models.Model):
	_inherit = 'hr.contract'
	
	contract_template_id = fields.Many2one('contract.template', string='Contract Template',
	                                       track_visibility='onchange')
	
	def load_template_details(self):
		"""
		Load lines of contract template allowance and deduction
		"""
		for contract in self:
			contract.allowance_ids = [[5]]
			contract.deduction_ids = [[5]]
			if contract.contract_template_id.allowance_ids:
				contract.allowance_ids = [(0, 0, {'allowance_id': line.id, 'value': line.value, 'contract_id': contract.id})
				                          for line in contract.contract_template_id.allowance_ids]
			if contract.contract_template_id.deduction_ids:
				contract.deduction_ids = [(0, 0, {'deduction_id': line.id, 'value': line.value, 'contract_id': contract.id})
				                          for line in contract.contract_template_id.deduction_ids]
				
	def bulk_load_template(self):
		"""
		Load Template for contract ids
		"""
		if self.env.context.get('active_ids'):
			contract_ids = self.env['hr.contract'].browse(self.env.context.get('active_ids'))
			contract_ids.load_template_details()
	
	allowance_ids = fields.One2many('hr.contract.allowance.line', 'contract_id', 'Allowances')
	deduction_ids = fields.One2many('hr.contract.deduction.line', 'contract_id', 'Deductions')
	# static Fields
	basic = fields.Float(string='Basic')
	allowance = fields.Float(string='Allowance')
	monthly_vpp = fields.Float(string='Monthly VPP ')
	total_basic_allowance = fields.Float(string='Total Basic & Allowances')
	annual_vpp = fields.Float(string='Annual VPP')
	health_insurance = fields.Float(string='Health Insurance')
	night_shift = fields.Float(string='Night Shift')


class ContractAllowanceLine(models.Model):
	_name = 'hr.contract.allowance.line'
	_description = "HR Contract Allowance Line"
	
	value = fields.Float(string='Value', require=True, default='allowance_id')
	contract_id = fields.Many2one('hr.contract', "contract")
	allowance_id = fields.Many2one('allowance.hr', string='Allowances', require=True)


class ContractDeductionLine(models.Model):
	_name = 'hr.contract.deduction.line'
	_rec_name = 'deduction_id'
	_description = "HR Contract Deductions Line"
	
	value = fields.Float(string='Value', require=True, default='deduction_id.value')
	contract_id = fields.Many2one('hr.contract', "contract")
	deduction_id = fields.Many2one('deduction.hr', string='Deductions', require=True)

