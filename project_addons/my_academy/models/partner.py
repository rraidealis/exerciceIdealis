from odoo import fields, models


class Partner (models.Model):
    _inherit = 'res.partner'

    instructor = fields.Boolean(string="Instructor", default=False)
    session_ids = fields.Many2many('models.session','table' , 'champ1', 'champ2', string="Attended Sessions", readonly=True)
