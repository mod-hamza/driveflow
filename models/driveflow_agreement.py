from odoo import api, models, fields
from odoo.exceptions import UserError

class DriveflowAgreement(models.Model):
    _name               = "driveflow.agreement"
    _description        = "Drive Flow Agreements"
    _inherit            = ["mail.thread", "mail.activity.mixin"]

    name                = fields.Char(required=True)
    customer_id         = fields.Many2one("res.partner", string="Customer", required=True)
    car_id              = fields.Many2one(
                            "driveflow.car", string="Car",
                            domain=[("status", "=", "available")],
                        )
    date_start          = fields.Date(string="Start Date", required=True)
    date_end            = fields.Date(string="End Date", required=True)
    duration            = fields.Integer(compute="_compute_duration")
    salesperson_id      = fields.Many2one("res.user", string="Agent", default=lambda self: self.env.user)
    extra_charge_ids    = fields.One2many("driveflow.extra.charge", "agreement_id", string="Extra Charges")
    state               = fields.Selection([
                            ("draft", "Draft"),
                            ("ongoing", "Ongoing"),
                            ("returned", "Returned"),
                            ("invoiced", "Invoiced"),
                        ], default="draft")
    invoice_id          = fields.Many2one("account.move", string="Invoice", readonly=True)

    # Used AI for this
    @api.depends("date_start", "date_end")
    def _compute_duration(self):
        for record in self:
            if record.date_start and record.date_end:
                record.duration = (record.date_end - record.date_start).days
            else:
                record.duration = 0

    def action_hand_over(self):
        for record in self:
            if record.state != "draft":
                raise UserError("Only draft agreements can be handed over.")
            if record.car_id.status != "available":
                raise UserError("You cannot dispatch a car that is rented or in maintenance.")
            record.car_id.status = "rented"
            record.state = "ongoing"

    def action_return_car(self):
        for record in self:
            if record.state != "ongoing":
                raise UserError("Only ongoing agreements can be returned.")
            record.car_id.status = "available"
            record.state = "returned"

    def action_generate_invoice(self):
        for record in self:
            if record.state != "returned":
                raise UserError("Only returned agreements can be invoiced.")
            for charge in record.extra_charge_ids:
                if not charge.description:
                    raise UserError("Every extra charge must have a description.")
            record._generate_invoice()
            record.state = "invoiced"

    def _generate_invoice(self):
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

    def action_view_invoice(self):
        self.ensure_one()
        return self.invoice_id.get_formview_action()
