from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DriveflowExtraCharge(models.Model):
    _name = "driveflow.extra.charge"
    _description = "Drive Flow Extra Charges"

    description = fields.Char(string="Reason", required=True)
    amount = fields.Float()
    agreement_id = fields.Many2one("driveflow.agreement", string="Agreement")

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError("Amount cannot be negative.")
