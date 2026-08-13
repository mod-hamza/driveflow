from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"
    _description = "Drive Flow Driver"

    driver_license = fields.Char(string="Driver License")
    agreement_ids = fields.One2many("driveflow.agreement", "customer_id", string="Rental History")
