from odoo import models, fields, api, _
from datetime import date,datetime
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError


class AccountMove(models.Model):

    _inherit = 'account.move'

    remarks = fields.Text(string = "Remarks")
    is_remarks = fields.Boolean(related="company_id.remark_for_move")
    is_remarks_mandatory = fields.Boolean(related="company_id.remark_mandatory_move")
    is_boolean = fields.Boolean()

    @api.onchange('invoice_date')
    def onchange_invoice_date(self):
        if str(self.invoice_date) < str(date.today()):
           self.is_boolean = True
        else:
            self.is_boolean = False

    def button_draft(self):
        for move in self:
            if move in move.line_ids.mapped('full_reconcile_id.exchange_move_id'):
                raise UserError(_('You cannot reset to draft an exchange difference journal entry.'))
            if move.tax_cash_basis_rec_id:
                raise UserError(_('You cannot reset to draft a tax cash basis journal entry.'))
            # We remove all the analytics entries for this journal
            move.mapped('line_ids.analytic_line_ids').unlink()

        self.mapped('line_ids').remove_move_reconcile()
        self.write({'state': 'draft', 'is_move_sent': False})


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    remarks = fields.Text(string = "Remarks",related = "move_id.remarks")
