from odoo import models, fields

class DriveflowExtraCharge(models.Model):
    _name = "driveflow.extra.charge"
    _description = "Drive Flow Extra Charges"

    description = fields.Char(string="Reason", required=True)
    amount = fields.Float()
    agreement_id = fields.Many2one("driveflow.agreement", string="Agreement")
