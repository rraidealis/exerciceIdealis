from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'add.attendees.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_session(self):
        return self.env['models.session'].browse(self._context.get('active_ids'))

    session_ids = fields.Many2many('models.session',
                                 string="Sessions", required=True, default=_default_session)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    @api.multi
    def subscribe(self):
        for session in self.session_ids:
            session.attendee_ids |= self.attendee_ids
        return {}
