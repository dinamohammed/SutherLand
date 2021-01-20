# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import Warning


# Ahmed Salama Code Start ---->


class PayslipXlsx(models.AbstractModel):
    _name = 'report.hr_custom_reports.report_payslip_employee'
    _inherit = 'report.report_xlsx.abstract'
    
    def generate_xlsx_report(self, workbook, data, payslips):
        report_name = "Raw Data"
        # One sheet by partner
        worksheet = workbook.add_worksheet(report_name[:31])
        format_left_to_right = workbook.add_format({'reading_order': 1})
        format_left_to_right.set_reading_order(1)

        cell_format_left = workbook.add_format()
        cell_format_left.set_align('left')

#         worksheet.left_to_right()
        worksheet.set_column('A:B', 15)
        worksheet.set_column('C:C', 40)
        worksheet.set_column('D:I', 15)
        worksheet.set_column('J:K', 25)
        worksheet.set_column('L:M', 15)
        worksheet.set_column('N:N', 40)

        bold = workbook.add_format({'bold': True})
        cell_format_header = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#808080'})
        cell_format_header_1 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FFFFFF'})
        cell_format_header_2 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#0000FF'})
        
        cell_format_header_3 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FF6600'})
        cell_format_header_4 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#008000'})
        cell_format_header_5 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FF00FF'})
        cell_format_header_6 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#FF0000'})
        cell_format_header_7 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#C0C0C0'})
        cell_format_header_8 = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter',
                                                  'border': 1, 'fg_color': '#00FF00'})
        
        cell_format_row = workbook.add_format({'bold': False, 'align': 'center', 'valign': 'vcenter',
                                               'border': 1, 'fg_color': '#D7E4BC'})
        cell_format_header.set_center_across()
        
        # Static Header
        worksheet.write(0, 0, 'Include', cell_format_header_1)
        worksheet.write(0, 1, 'S', cell_format_header_1)
        worksheet.write(0, 2, 'E-mail', cell_format_header_1)
        
        worksheet.write(0, 3, 'Insurance', cell_format_header)
        worksheet.write(0, 4, 'Status', cell_format_header)
        worksheet.write(0, 5, 'BankAccount#', cell_format_header)
        worksheet.write(0, 6, 'Bank', cell_format_header)
        worksheet.write(0, 7, 'DOJ', cell_format_header)
        worksheet.write(0, 8, 'Dep. ID', cell_format_header)
        worksheet.write(0, 9, 'Dep. Name', cell_format_header)
        worksheet.write(0, 10, 'PROGRAM', cell_format_header)
        worksheet.write(0, 11, 'Level', cell_format_header)
        worksheet.write(0, 12, 'ID#', cell_format_header)
        worksheet.write(0, 13, 'Employee Name', cell_format_header)
        worksheet.write(0, 14, 'Comp Offs from Site', cell_format_header)
        worksheet.write(0, 15, 'Comp Offs from Home', cell_format_header)
        worksheet.write(0, 16, 'Absent', cell_format_header)
        worksheet.write(0, 17, 'Overtime Hours from Site', cell_format_header)
        worksheet.write(0, 18, 'Overtime Hours from Home', cell_format_header)
        worksheet.write(0, 19, 'Night Shift allowance', cell_format_header)
        
        worksheet.write(0, 20, 'Basic', cell_format_header_2)
        worksheet.write(0, 21, 'Allowances', cell_format_header_2)
        worksheet.write(0, 22, 'Monthly VPP', cell_format_header_2)
        worksheet.write(0, 23, 'Total Basic & Allowances', cell_format_header_2)
        worksheet.write(0, 24, 'Productivity Bonus', cell_format_header_2)
        worksheet.write(0, 25, 'Language Bonus', cell_format_header_2)
        worksheet.write(0, 26, 'Performance Incentives', cell_format_header_2)
        worksheet.write(0, 27, 'Gross Salary', cell_format_header_2)
        worksheet.write(0, 28, 'Nightshift Allowance', cell_format_header_2)
        worksheet.write(0, 29, 'Annual VPP', cell_format_header_2)
        
        worksheet.write(0, 30, 'Salary without VPP', cell_format_header_3)
        worksheet.write(0, 31, 'VPP Percentage', cell_format_header_3)
        worksheet.write(0, 32, 'VPP added Amount', cell_format_header_3)
        worksheet.write(0, 33, 'Salary after KRA', cell_format_header_3)
        
        worksheet.write(0, 34, 'Other Additions', cell_format_header_4)
        worksheet.write(0, 35, 'Comp off from site amount', cell_format_header_4)
        worksheet.write(0, 36, 'Overtime from site Amount', cell_format_header_4)
        worksheet.write(0, 37, 'Comp off from Home amount', cell_format_header_4)
        worksheet.write(0, 38, 'Overtime from home Amount', cell_format_header_4)
        worksheet.write(0, 39, 'Night shift allowance', cell_format_header_4)
        worksheet.write(0, 40, 'Ramadan Allowance', cell_format_header_4)
        worksheet.write(0, 41, 'Total Additions', cell_format_header_4)
        worksheet.write(0, 42, 'Salary after additions', cell_format_header_4)
        
        worksheet.write(0, 43, 'Absent amount', cell_format_header_5)
        worksheet.write(0, 44, 'Social Insurance', cell_format_header_5)
        worksheet.write(0, 45, 'Health Insurance', cell_format_header_5)
        worksheet.write(0, 46, 'Other Deductions', cell_format_header_5)
        worksheet.write(0, 47, 'Ramadan Allowance Adjustments', cell_format_header_5)
        worksheet.write(0, 48, 'Total Deductions', cell_format_header_5)
        
        worksheet.write(0, 49, 'Net Taxable Salary', cell_format_header_6)
        worksheet.write(0, 50, 'Personal exemption', cell_format_header_6)
        worksheet.write(0, 51, 'Annual Salary', cell_format_header_6)
        worksheet.write(0, 52, 'Second bracket 2.5%', cell_format_header_6)
        worksheet.write(0, 53, 'Third Bracket 10%', cell_format_header_6)
        worksheet.write(0, 54, 'Fourth Bracket 15%', cell_format_header_6)
        worksheet.write(0, 55, 'Fifth Bracket 20%', cell_format_header_6)
        worksheet.write(0, 56, 'Sixth Bracket 22.5%', cell_format_header_6)
        worksheet.write(0, 57, 'Seventh Bracket 25%', cell_format_header_6)
        worksheet.write(0, 58, 'Total Brackets', cell_format_header_6)
        worksheet.write(0, 59, 'New Monthly Taxes', cell_format_header_6)
        
        worksheet.write(0, 60, 'Salary After Deductions', cell_format_header_7)
        worksheet.write(0, 61, 'Advanced Payments', cell_format_header_7)
        worksheet.write(0, 62, 'leave Balance', cell_format_header_7)
        worksheet.write(0, 63, 'Leave Balance encashment', cell_format_header_7)
        worksheet.write(0, 64, '1% solidarity contribution', cell_format_header_7)
        worksheet.write(0, 65, 'Net Salary', cell_format_header_7)
        
        worksheet.write(0, 66, 'Employer Share of SI', cell_format_header_8)
        worksheet.write(0, 67, 'Medical insurance', cell_format_header_8)
        worksheet.write(0, 68, 'New CTC', cell_format_header_8)
        
        row  = 1
        for payslip_id in payslips:
            col = 0
            worksheet.write(row,col,'',cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.registration_number,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.work_email,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.insurance_type,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.employee_status,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.bank_account_id.acc_number,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.bank_account_id.bank_id.name,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.contract_id.date_start,cell_format_row)
            col += 1
            worksheet.write(row,col,'',cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.department_id.name,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.work_location_id.name,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.level_id.name,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.registration_number,cell_format_row)
            col += 1
            worksheet.write(row,col,payslip_id.employee_id.name,cell_format_row)
            
            row += 1
        

            
# Ahmed Salama Code End.
