from datetime import timedelta
from odoo import models, fields, api, exceptions, _
# from odoo.exceptions import ValidationError


class Course(models.Model):
    _name = 'models.course'
    _description = "OpenAcademy Courses"

    # SQL checks  : name != description && name UNIQUE
    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "The course title should not be in the description"),

        ('name_unique',
         'UNIQUE(name)',
         "The course title should be unique!"),
    ]

    name = fields.Char(string="Title", required=True)
    description = fields.Text(string="Description")

    responsible_id = fields.Many2one('res.users', ondelete='set null', string="Responsible", index=True)
    session_ids = fields.One2many('models.session', 'course_id', string="Session")
    
    # duplicate option because name is UNIQUE
    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        
        copied_count = self.search_count(
            [('name', '=like', _(u"Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _(u"Copy of {}").format(self.name)
        else:
            new_name = _(u"Copy of {} ({})").format(self.name, copied_count)
            
        default['name'] = new_name
        return super(Course, self).copy(default)
    

class Session (models.Model):
    _name = 'models.session'
    _description = "OpenAcademy Sessions"

    name = fields.Char(string="Session name", required=True)
    start_date = fields.Date(string="Start date", default=fields.Date.today)
    duration = fields.Float(string="Duration", digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="Number of seats")
    active = fields.Boolean(string="Active", default=True)
    color = fields.Integer(string="Color")

    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=[('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('models.course', ondelete='cascade', string="Course", required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")

    # Computed fields
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')
    end_date = fields.Date(string="End date", store=True, compute='_get_end_date', inverse='_set_end_date')
    hours = fields.Float(string="Duration (hours)", compute='_get_hours', inverse='_set_hours')
    attendees_count = fields.Integer(string="Attendees count", compute='_get_attendees_count', store=True)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for session in self:
            if not session.seats:
                session.taken_seats = 0.0
            else:
                session.taken_seats = 100.0 * len(session.attendee_ids) / session.seats

        if session.taken_seats > 100:
            raise exceptions.ValidationError(_("Too much attendees compared to the available seats!"))

    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for session in self:
            if not (session.start_date and session.duration):
                session.end_date = session.start_date
                continue

            duration = timedelta(days=session.duration, seconds=-1)
            session.end_date = session.start_date + duration

    def _set_end_date(self):
        for session in self:
            if not (session.start_date and session.end_date):
                continue

            session.duration = (session.end_date - session.start_date).days + 1

    @api.depends('duration')
    def _get_hours(self):
        for session in self:
            session.hours = session.duration * 24

    def _set_hours(self):
        for session in self:
            session.duration = session.hours / 24

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for session in self:
            session.attendees_count = len(session.attendee_ids)

    # ONCHANGE

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Less than 0 seats "),
                    'message': _("Incorrect seat amount"),
                }
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("It's full!"),
                    'message': _("It's already full, stop entering!"),
                }
            }
