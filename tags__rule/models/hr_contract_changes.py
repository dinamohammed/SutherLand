# -*- coding: utf-8 -*-

from datetime import datetime

from odoo import models, fields


# Ahmed Salama Code Start ---->


class HrContractInherit(models.Model):
	_inherit = 'hr.contract'
	
	# ################## Contract Type # ##########################
	
	contract_type_id = fields.Many2one('hr.contract.type', 'Contract Type', store=True)
	
	# ####################### Allowance Fields # ############### ###############
	internal_transportation_value = fields.Float(string='Internal Transportation')
	veracity_value = fields.Float(string='Veracity')
	external_transportation_value = fields.Float(string='External Transportation')
	meal_value = fields.Float(string='Meal Voucher')
	rest_allowance = fields.Float(string='Rest Allowance')
	supervision_allowance = fields.Float(string='Supervision Allowance')
	allowance_1 = fields.Float(string='Allowance 1')
	allowance_2 = fields.Float(string='Allowance 2')
	allowance_3 = fields.Float(string='Allowance 3')
	allowance_4 = fields.Float(string='Allowance 4')
	allowance_5 = fields.Float(string='Allowance 5')
	allowance_6 = fields.Float(string='Allowance 6')
	allowance_7 = fields.Float(string='Allowance 7')
	allowance_8 = fields.Float(string='Allowance 8')
	
	# ####################### Deduction Fields # ############### ###############
	absence_value = fields.Float(string='Absence')
	deduction_1 = fields.Float(string='Deduction 1')
	house_deduction = fields.Float(string='House Deduction')
	deduction_2 = fields.Float(string='Deduction 2')
	deduction_3 = fields.Float(string='Deduction 3')
	
	# ############### ################ 7afeez --> Incentive # ############### ####################
	effort_allowance = fields.Float(string='Effort Allowance')
	manufacturing_allowance = fields.Float(string='Manufacturing Allowance')
	additional_allowance = fields.Float(string='Additional Allowance')
	ceo_allowance = fields.Float(string='CEO Allowance')
	traveling_days = fields.Integer(string='Traveling Days')
	transportation_expenses = fields.Float(string='Transportation Expenses')
	
	# ########################## Extra Fields Added #########################################
	security_days = fields.Integer(string='Security Days Allowance')
	company_pay = fields.Float(string='Company Pay')
	allowance_apecial = fields.Float(string='Special Allowance')
	total_institution_Value = fields.Float(string='Total Institutions Value')
	
	def Daily_Check_Contract_Value(self):
		
		Current_Date = datetime.now()
		if Current_Date.day == '20':
			cont_rec = self.env['hr.contract'].search([])
			for cont in cont_rec:
				cont['security_days'] = 0
				cont['allowance_1'] = 0
				cont['deduction_3'] = 0
				cont['effort_allowance'] = 0
				cont['manufacturing_allowance'] = 0
				cont['additional_allowance'] = 0
	
	employee_no = fields.Char(string='Employee Registration Number', search='_get_search_list', store=False)
	
	def _get_search_list(self, operator, value):
		# print("------------------- On Search List -----------------")
		# print("VALS:: ",operator,value )
		if operator == 'like':
			operator = 'ilike'
		employee_ids = self.env['hr.employee'].search([('registration_number', operator, value)]).mapped('id')
		# print("Employee Ids:: ", employee_ids)
		contract_ids = self.env['hr.contract'].search([('employee_id', 'in', employee_ids)]).mapped('id')
		# ids = values
		# print("Contract Ids:: ", contract_ids)
		return [('id', 'in', contract_ids)]

# ############### ############### ############### ############### ################
# Create A Scheduled Action :
# Name : Update Specific Values in
# Model : Contract
# Execute Every : 1 Week
# Number of calls : -1
# Action to Do : Execute Python Code
# Code to write : Update Multi Contract Value

# Ahmed Salama Code End.
