from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    company_type = fields.Selection(
        selection_add=[
            ("hotel", "Hotel"),
        ],
        ondelete={"hotel": "set company"},
    )

    is_hotel = fields.Boolean(
        string="Is a Hotel",
        default=False,
        help="Check if the contact is a company and hotel",
    )

    @api.depends("is_company", "is_hotel")
    def _compute_company_type(self):
        for partner in self:
            default_value = "company" if partner.is_company else "person"
            partner.company_type = "hotel" if partner.is_hotel else default_value

    def _write_company_type(self):
        for partner in self:
            partner.is_company = partner.company_type in ["hotel", "company"]
            partner.is_hotel = partner.company_type == "hotel"

    @api.onchange("company_type")
    def onchange_company_type(self):
        value = self.company_type
        self.is_company = value in ["hotel", "company"]
        self.is_hotel = value == "hotel"
