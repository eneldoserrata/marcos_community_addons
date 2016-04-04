from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
import StringIO
import base64
import csv
class dynamic_xls_report(osv.TransientModel):
    _name = 'dynamic.xls.report'
    
    _columns = {
                'model_name': fields.many2one('ir.model','Model',help="Select the model name."),
                'field_name':fields.many2many('ir.model.fields','rel_fields_model_rpt','wiz_id','rec_id','Field Name', help="Select the required fields."),
                'search_domain':fields.char('Domain'),
                'm2m_value' : fields.boolean('Value', help='Select if You want the value instead of id for Many2one field'),
                'filedata': fields.binary('File', readonly=True),
                'filename': fields.char('Filename', size = 64, readonly=True),
                'limit_rec': fields.integer('Limit', help="Limit your records"),
                'order_type':fields.boolean('Order',help='Check if you want the records in descending order'),
                'order_on_field' : fields.many2one('ir.model.fields','Order BY',domain="[('model_id','=',model_name)]",help="Select the field by which you want to sort."),
                'set_offset': fields.integer('Offset'),
                'domain_lines': fields.one2many('dynamic.domain.line','dynamic_rpt_id', 'Domain',help="Put the domain if any"),
                
                }
    def get_xls(self, cr, uid, ids, context=None):
        field_model = self.pool.get('ir.model.fields')
        for val in self.browse(cr, uid, ids):
            model = val.model_name.model
            model_obj = self.pool.get(model)
            field_sel = []
            for field_name in val.field_name:
                field_sel.append(field_name.name)
            if not len(field_sel):
                fld = field_model.search(cr, uid, [('model_id','=',val.model_name.id),('ttype','!=','binary')])
                if len(fld):
                    for f in field_model.browse(cr, uid, fld):
                       field_sel.append(f.name)
                else:
                    raise orm.except_orm(_('Error'), _('No column found to Export'))
            domain = []
            for d_line in val.domain_lines:
                temp = ()
                d_val = str(d_line.value) or False
                if d_val in ('false','False'):
                    d_val = False
                if d_val in ('true','True'):
                    d_val  = True
                temp = (str(d_line.field_name.name),str(d_line.operator),d_val)
                domain.append(temp)
            limit = val.limit_rec or None
            order_field = val.order_on_field and val.order_on_field.name or None
            if order_field and val.order_type:
                order = order_field +' desc'
            elif order_field:
                order = order_field
            else:
                order = None
            try:
                recs = model_obj.search_read(cr, uid, domain, field_sel, offset=val.set_offset, limit = limit, order =  order )
            except:
                mod_ids = model_obj.search(cr, uid, domain, offset=val.set_offset, limit = limit, order =  order )
                recs = model_obj.read(cr, uid, mod_ids,field_sel)
            if not field_sel:
                if recs:
                    field_sel = recs[0].keys()
                else:
                    raise orm.except_orm(_('Error'), _('No record found to Export'))
             
            result = []
            result.append(field_sel)
            for rec in recs:
                value = ''
                temp = []
                for key in field_sel:
                    v = rec.get(key)
                    if v:
                        if type(v) == tuple:
                            if val.m2m_value:
                                value = v[1]
                            else:
                                value = v[0]
                        else:
                            value = str(v)
                    else:
                        value = v
                    temp.append(value)
                result.append(temp)

            fp = StringIO.StringIO()
            writer = csv.writer(fp)
            for data in result:
                row = []
                for d in data:
                    if isinstance(d, basestring):
                        d = d.replace('\n',' ').replace('\t',' ')
                        try:
                            d = d.encode('utf-8')
                        except:
                            pass
                    if d is False: d = None
                    row.append(d)
                writer.writerow(row)
        fp.seek(0)
        data = fp.read()
        fp.close()
        out=base64.encodestring(data)
        file_name = str(val.model_name.name) + '.xls'
        self.write(cr, uid, ids, {'filedata':out, 'filename':file_name}, context=context)
        return {
                    'name':'Dynamic Report',
                    'res_model':'dynamic.xls.report',
                    'type':'ir.actions.act_window',
                    'view_type':'form',
                    'view_mode':'form',
                    'target':'new',
                    'nodestroy': True,
                    'context': context,
                    'res_id': ids and ids[0],
                    } 
dynamic_xls_report()

class dynamic_domain_line(osv.TransientModel):
    _name = 'dynamic.domain.line'
    _columns = {
                'dynamic_rpt_id': fields.many2one('dynamic.xls.report','Relation Field'),
                'field_name' : fields.many2one('ir.model.fields','Field Name',domain="[('model_id','=',parent.model_name)]"),
                'operator': fields.selection([('ilike','Contains'),('=','Equal'),('!=','Not Equal'),('<','Less Than'),('>','Greater Than'),('<=','Less Than Equal To'),('>=','Greater Than Equal To')],'Operator'),
                'value' : fields.char('Value',help='For relation use dot(.) with field name'),
                }