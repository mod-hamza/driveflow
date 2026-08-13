from odoo import models, fields

class DriveflowAgreement(models.Model):
    _inherit = "driveflow.agreement"

    invoice_id = fields.Many2one("account.move", string = "Invoice", readonly = True)

    def action_generate_invoice(self):
        res = super().action_generate_invoice()

        for record in self:
            lines = [fields.Command.create({
                "name": f"{record.car_id.name} rental ({record.duration} days)",
                "quantity": record.duration,
                "price_unit": record.car_id.rental_rate,
            })]
            for charge in record.extra_charge_ids:
                lines.append(fields.Command.create({
                    "name": charge.description,
                    "quantity": 1,
                    "price_unit": charge.amount,
                }))
            record.invoice_id = self.env["account.move"].create({
                "partner_id": record.customer_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": lines,
            })

            return res

    def action_view_invoice(self):
        self.ensure_one()
        return self.invoice_id.get_formview_action()