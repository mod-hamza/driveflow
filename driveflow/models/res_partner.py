from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Drive Flow Driver"

    agreement_ids = fields.One2many("driveflow.agreement", "customer_id", string="Rental History")
