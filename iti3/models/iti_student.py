from datetime import date
from odoo import api, models , fields
from odoo.exceptions import ValidationError

class ITIStudent(models.Model):
    _name = 'iti.student'
    name = fields.Char()
    birthdate = fields.Date() 
    age = fields.Integer(compute='compute_age')
    gender = fields.Selection([('Female', 'female') , ('Male', 'male')]) 
    accepted = fields.Boolean()  
    is_working = fields.Boolean()
    cv = fields.Binary()
    salary = fields.Float()
    
    track_id = fields.Many2one('iti.track')
    track_capacity = fields.Integer(related = 'track_id.capacity')
    
    level = fields.Selection([('level1', 'Prep'), ('level2', 'Sec'), ('level3', 'Graduate')])
    
    level_logs = fields.One2many('iti.student.log', 'student_id')


    def button_clicked(self):
        self.level = "level2"

    @api.onchange('track_id')
    def change_track(self):
        track_name = self.track_id.name
        return {
            'warning': {
               'title' : ('Track Changed'),
               'message' : 'Track is changed %s' %(track_name)
            }
        }
    
    @api.onchange('level')
    def create_log_level(self):
        vals = {
            'description' : 'Level changed to %s' %(self.level),
            'student_id' : self.id
        }
        self.env['iti.student.log'].create(vals)

    @api.constrains('age')
    def check_age(self):
        if self.age <= 0 :
            raise ValidationError('Age Can not be negative number')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This Name Is Already Exist'),
        ('age_constrain', 'CHECK(age > 0)', 'Age can not be Negative Number')
    ]    
        
    # @api.constrains('name')
    # def check_unique_name(self):
    #    duplicate_name = self.env['iti.student'].search([('name', '=', self.name)])

    #    if len(duplicate_name) > 1:
    #       raise ValidationError("Name Exist Before")
    
    @api.depends('birthdate')
    def compute_age(self):
        for rec in self:
            if rec.birthdate:
                today = date.today()
                rec.age = today.year - rec.birthdate.year - (
                    (today.month, today.day) < (rec.birthdate.month, rec.birthdate.day))
            else :
                rec.age = 0


        