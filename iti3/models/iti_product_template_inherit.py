from odoo import models, fields, api

class ITIProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    barcode2 = fields.Char()  
    
      