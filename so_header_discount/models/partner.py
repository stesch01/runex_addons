# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2016-TODAY Linserv Aktiebolag, Sweden (<http://www.linserv.se>).
#
##############################################################################

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class ResPartner(models.Model):
    _inherit = "res.partner"

    so_discount = fields.Float('Discount %', digits_compute=dp.get_precision('Account'))
    