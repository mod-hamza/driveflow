from odoo import models, fields, api
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property")
    state = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')])

    _check_price = models.Constraint("CHECK(price > 0)", "Offer price must be strictly positive.")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)
    
    def accept_offer(self):
        for record in self:
            if record.property_id.state == 'offer_accepted':
                raise UserError("This property already has an accepted offer.")
            if record.property_id.state == 'refused':
                raise UserError("You cannot accept an offer on a refused property.")
            record.state = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def refuse_offer(self):
        for record in self:
            if record.state == 'accepted':
                raise UserError("This property already has an accepted offer.")
            record.state = 'refused'
