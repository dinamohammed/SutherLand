import base64
from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from odoo.tools import float_round, date_utils


class HrPayslipInherit(models.Model):
	_inherit = 'hr.payslip'
	
	tax_base_temp = fields.Float(string='Tax Base Temp', default=0)

	##### Add Employee's registration Number to Payslip
	registration_number = fields.Char('Employee Number', groups="hr.group_hr_user", copy=False, required=True)

	@api.onchange('registration_number')
	def employees_data(self):
		if (not self.registration_number) or (not self.date_from) or (not self.date_to):
			return

		employee = self.env['hr.employee'].search([('registration_number', '=', self.registration_number)])
		date_from = self.date_from
		date_to = self.date_to
		self.employee_id = employee.id

		self.company_id = employee.company_id
		if not self.contract_id or self.employee_id != self.contract_id.employee_id:  # Add a default contract if not already defined
			contracts = employee._get_contracts(date_from, date_to)

			if not contracts or not contracts[0].structure_type_id.default_struct_id:
				self.contract_id = False
				self.struct_id = False
				return
			self.contract_id = contracts[0]
			self.struct_id = contracts[0].structure_type_id.default_struct_id

		payslip_name = self.struct_id.payslip_name or _('Salary Slip')
		self.name = '%s - %s - %s' % (
		payslip_name, self.employee_id.name or '', format_date(self.env, self.date_from, date_format="MMMM y"))

		if date_to > date_utils.end_of(fields.Date.today(), 'month'):
			self.warning_message = _(
				"This payslip can be erroneous! Work entries may not be generated for the period from %s to %s." %
				(date_utils.add(date_utils.end_of(fields.Date.today(), 'month'), days=1), date_to))
		else:
			self.warning_message = False

		self.worked_days_line_ids = self._get_new_worked_days_lines()


	def get_tags(self, category_ids):
		tag = []
		for category in category_ids:
			tag.append(category.name)
		return tag
	
	# ############### ############### ##################
	# To Execute the previous function on a salary rule :
	# Write the following code :
	#       result = payslip.env['hr.payslip'].get_tags(employee.category_ids)
	
	def _date_check(self, specific_date):
		current_Date = datetime.now()
		day_Current_Date = current_Date.strftime("%d")
		specific_date_str = datetime.strptime(specific_date, DEFAULT_SERVER_DATE_FORMAT)
		day_specific_date = specific_date_str.strftime("%d")
		
		if day_specific_date < day_Current_Date:
			raise ValidationError(_('Sorry, Today Date Must be greater Than Start Date...'))
	
	# ############### ############### ##################
	# To Execute the previous function on a salary rule :
	# Write the following code :
	#       result = payslip.env['hr.payslip']._date_check('2019-1-12')
	
	def Tax_Base_Value(self, tax_base, field_to_give):
		emp_rec = self.env['hr.employee'].search([('id', '=', field_to_give)])
		payslip_rec = self.env['hr.payslip'].search([('employee_id', '=', emp_rec['id']), ('state', '=', 'draft')])
		payslip_rec['tax_base_temp'] = tax_base
		return 0
	
	# ############### ############### ##################
	# To Execute the previous function on a salary rule :
	# Write the following code :
	#       result = payslip.env['hr.payslip'].Tax_Base_Value(categories.RuleofTaxBase , employee.id)
	
	def action_payslip_done(self):
		if any(slip.state == 'cancel' for slip in self):
			raise ValidationError(_("You can't validate a cancelled payslip."))
		self.write({'state': 'done'})
		self.mapped('payslip_run_id').action_close()
		for payslip in self:
			# #### Add the part of Tax Base Container
			payslip.employee_id.tax_base = payslip.tax_base_temp + payslip.employee_id.tax_base
		# ############### ##########################
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
	employee_no = fields.Char(string='Employee Number', search='_get_search_list_2')
	
	def _get_search_list_2(self, operator, value):
		if operator == 'like':
			operator = 'ilike'
		employee_ids = self.env['hr.employee'].search([('registration_number',operator,value)]).mapped('id')
		payslip_ids = self.env['hr.payslip'].search([('employee_id','in',employee_ids)]).mapped('id')
		return [('id', 'in', payslip_ids)]
	
	@api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
	def _onchange_employee(self):
        	if (not self.employee_id) or (not self.date_from) or (not self.date_to):
            		return

        	employee = self.employee_id
        	date_from = self.date_from
        	date_to = self.date_to
        
        	self.registration_number = employee.registration_number
        
        	self.company_id = employee.company_id
        	if not self.contract_id or self.employee_id != self.contract_id.employee_id: # Add a default contract if not already defined
            		contracts = employee._get_contracts(date_from, date_to)

            		if not contracts or not contracts[0].structure_type_id.default_struct_id:
                		self.contract_id = False
                		self.struct_id = False
                		return
            		self.contract_id = contracts[0]
            		self.struct_id = contracts[0].structure_type_id.default_struct_id

        	payslip_name = self.struct_id.payslip_name or _('Salary Slip')
        	self.name = '%s - %s - %s' % (payslip_name, self.employee_id.name or '', format_date(self.env, self.date_from, date_format="MMMM y"))

        	if date_to > date_utils.end_of(fields.Date.today(), 'month'):
            		self.warning_message = _("This payslip can be erroneous! Work entries may not be generated for the period from %s to %s." 
                        	             %(date_utils.add(date_utils.end_of(fields.Date.today(), 'month'), days=1), date_to))
        	else:
            		self.warning_message = False

        	self.worked_days_line_ids = self._get_new_worked_days_lines()

	@api.onchange('registration_number')
	def employees_data(self):
		if (not self.registration_number) or (not self.date_from) or (not self.date_to):
			return

		employee = self.env['hr.employee'].search([('registration_number', '=', self.registration_number)])
		date_from = self.date_from
		date_to = self.date_to
		self.employee_id = employee.id

		self.company_id = employee.company_id
		if not self.contract_id or self.employee_id != self.contract_id.employee_id:  # Add a default contract if not already defined
			contracts = employee._get_contracts(date_from, date_to)

			if not contracts or not contracts[0].structure_type_id.default_struct_id:
				self.contract_id = False
				self.struct_id = False
				return
			self.contract_id = contracts[0]
			self.struct_id = contracts[0].structure_type_id.default_struct_id

		payslip_name = self.struct_id.payslip_name or _('Salary Slip')
		self.name = '%s - %s - %s' % (
		payslip_name, self.employee_id.name or '', format_date(self.env, self.date_from, date_format="MMMM y"))

		if date_to > date_utils.end_of(fields.Date.today(), 'month'):
			self.warning_message = _(
				"This payslip can be erroneous! Work entries may not be generated for the period from %s to %s." %
				(date_utils.add(date_utils.end_of(fields.Date.today(), 'month'), days=1), date_to))
		else:
			self.warning_message = False

		self.worked_days_line_ids = self._get_new_worked_days_lines()
