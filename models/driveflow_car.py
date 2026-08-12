from odoo import models, fields

class EstateProperty(models.Model):
    _inherit = 'estate.property'
    invoice_id = fields.Many2one("account.move", string="Invoice", readonly=True)

    def sell_property(self):
        res = super().sell_property()

        for record in self:
            invoice = self.env['account.move'].create({
                "partner_id": record.buyer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    fields.Command.create({
                        "name": "6% commission",
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06
                    }),
                    fields.Command.create({
                        "name": "Admin fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ]
            })
            record.invoice_id = invoice.id
            return res

    def action_view_invoice(self):
        self.ensure_one()
        return self.invoice_id.get_formview_action()
