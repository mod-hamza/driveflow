from odoo import models, fields, api

class DriveflowCarType(models.Model):
    _name = "driveflow.car.type"
    _description = "Drive Flow Car Types"

    name = fields.Char(required=True)
    car_ids = fields.One2many("driveflow.car", "car_type_id")

    _check_unique_name = models.Constraint("UNIQUE(name)", "Car type name must be unique.")
    #SUV, Sedan, Hatchback, Limousine, Convertible, Coupe, Wagon, Van, Pickup Truck, Sports Car
