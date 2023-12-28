from odoo import models, fields, api

class ITIStudentLog(models.Model):
    _name = 'iti.student.log'

    description = fields.Text()

    student_id = fields.Many2one('iti.student')    