from odoo import models, fields, api
from odoo.exceptions import UserError

class DriveflowCar(models.Model):
    _name        = "driveflow.car"
    _description = "Drive Flow Cars"

    name            = fields.Char(required=True)
    car_type_id     = fields.Many2one("driveflow.car.type", string="Car Type")
    status          = fields.Selection([
                        ("available", "Available"),
                        ("rented", "Rented"),
                        ("maintenance", "In Maintenance"),
                    ], string="Status", default="available")
    rental_rate     = fields.Float(string="Rental Rate (per day)")
    agreement_ids   = fields.One2many("driveflow.agreement", "car_id")
    agreement_count = fields.Integer(compute="_compute_agreement_count")
    

    @api.depends("agreement_ids")
    def _compute_agreement_count(self):
        for record in self:
            record.agreement_count = len(record.agreement_ids)

    def action_car_maintainance(self):
        for record in self:
            if record.status != "available":
                raise UserError("Only available cars can be sent for maintenance.")
            record.status = "maintenance"

    def action_car_available(self):
        for record in self:
            if record.status not in "maintenance,rented":
                raise UserError("Only cars in maintenance or rented can be made available.")
            record.status = "available"

    def action_car_rented(self):
        for record in self:
            if record.status != "available":
                raise UserError("Only available cars can be rented.")
            record.status = "rented"