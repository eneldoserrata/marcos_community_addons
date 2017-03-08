# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Stage(models.Model):
    _inherit = 'note.stage'

    auto_close = fields.Boolean(
            string='Marks as archived',
            help='Marks notes in the stage as archived'
            )

    reverse_auto_close = fields.Boolean(
            string='Undo automatic archive',
            help='Restores a note if it was archived by the stage'
            )

    @api.multi
    def write(self, values):
        for record in self:
            ref = super(Stage, record).write(values)
            if ref:
                NoteNote = self.env['note.note']
                if record.auto_close:
                    notes = NoteNote.search([('stage_id', '=', record.id)])
                    for note in notes:
                        note.auto_close()
                elif record.reverse_auto_close:
                    notes = NoteNote.search([('stage_id', '=', record.id), ('auto_closed_stage_id', '!=', False)])
                    for note in notes:
                        note.auto_open()
        return True


class Note(models.Model):
    _inherit = 'note.note'

    auto_closed_stage_id = fields.Many2one(comodel_name='note.stage')

    @api.multi
    def auto_close(self):
        for record in self:
            record.action_close()
            record.write({'auto_closed_stage_id': record.stage_id.id})

    @api.multi
    def auto_open(self):
        for record in self:
            record.action_open()
            record.write({'auto_closed_stage_id': None})

    @api.multi
    def write(self, values):
        for record in self:
            ref = super(Note, record).write(values)
            if ref and 'stage_id' in values:
                stage = record.stage_id
                auto_close_stage = record.auto_closed_stage_id
                if stage.auto_close and record.open:
                    record.auto_close()
                elif auto_close_stage and auto_close_stage.reverse_auto_close and not record.open:
                    record.auto_open()
        return True
