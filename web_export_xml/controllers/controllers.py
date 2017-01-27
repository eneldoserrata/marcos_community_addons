# -*- coding: utf-8 -*-
##############################################################################
#
# OpenERP, Open Source Management Solution, third party addon
# Copyright (C) 2004-2015 Vertel AB (<http://vertel.se>).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

try:
    import json
except ImportError:
    import simplejson as json

import openerp.http as http
from openerp.http import request
from openerp.addons.web.controllers.main import ExcelExport


from fnmatch import fnmatch,fnmatchcase
from lxml import etree


import logging
_logger = logging.getLogger(__name__)


def export_xml(lines):
    document = etree.Element('openerp')
    data = etree.SubElement(document,'data')
    for line in lines:
        if line.id:
            k,id = line.get_external_id().items()[0] if line.get_external_id() else 0,"%s-%s" % (line._name,line.id)
            _logger.info("Reporting Block id = %s" % id)          
            record = etree.SubElement(data,'record',id=id,model=line._name)
            names = [name for name in line.fields_get().keys() if fnmatch(name,'in_group*')] + [name for name in line.fields_get().keys() if fnmatch(name,'sel_groups*')]
            for field,values in line.fields_get().items():
                if not field in ['create_date','nessage_ids','id','write_date','create_uid','__last_update','write_uid',] + names:
                    if values.get('type') in ['boolean','char','text','float','integer','selection','date','datetime']:
                        _logger.info("Simple field %s field %s values %s" % (values.get('type'),field,values))
                        try:
                        #if eval('line.%s' % field):
                            etree.SubElement(record,'field',name = field).text = "%s" % eval('line.%s' % field)
                        except:
                            pass
                    elif values.get('type') in ['many2one']:
                        if eval('line.%s' % field):                                     
                            k,id = eval('line.%s.get_external_id().items()[0]' % field) if eval('line.%s.get_external_id()' % field) else (0,"%s-%s" % (eval('line.%s._name' % field),eval('line.%s.id' % field)))
                            if id == "":
                                id = "%s-%s" % (eval('line.%s._name' % field),eval('line.%s.id' % field))
                            etree.SubElement(record,'field',name=field,ref="%s" % id)
                    elif values.get('type') in ['one2many']:  # Update from the other end
                        pass
                    elif values.get('type') in ['many2many']: # TODO
                            # <field name="member_ids" eval="[(4, ref('base.user_root')),(4, ref('base.user_demo'))]"/>
                        m2mvalues = []
                        for val in line:
                            id,external_id = 0,'' if not val.get_external_id() else val.get_external_id().items()[0]
                            _logger.info("External id %s -> %s" % (id,external_id[1]))
                            if len(external_id)>0:
                                m2mvalues.append("(4, ref('%s'))" % external_id[1])
#                            m2mvalues.append("(4, ref('%s'))" % val.get_external_id().items()[0] or '')
                        if len(m2mvalues)>0:
                            etree.SubElement(record,'field',name=field,eval="[%s]" % (','.join(m2mvalues)))
                        
                        #~ _logger.info("M2M values = %s -> %s" % (field,values))                                      
                        #~ for val in line:
                            #~ _logger.info("M2M = %s" % val)     
                            #~ 
                        #~ m2mvalues = []
                        #~ for val in eval('line.%s' % field):
                            #~ _logger.info('many2many %s ext-id %s' % (val,val.get_external_id().items()[0]))
                            #~ m2mvalues.append("(4,ref='%s')" % val.get_external_id().items()[0])
                        #~ etree.SubElement(record,'field',name=field,eval="[%s]" % (','.join(m2mvalues)))
            
         
    return document

def get_related(models,depth):
    objects = set()
    if depth < 4:
        for model in models:
            _logger.info('Get related model %s id %s' % (model._name,model.id))
            for field,values in model.fields_get().items(): 
                if not field in ['create_date','nessage_ids','id','write_date','create_uid','__last_update','write_uid']:
                    if values.get('type') in ['many2one']:
                        for related in get_related(eval("model.%s" % field),depth+1):
                            objects.add(related)
                    if values.get('type') in ['many2many']:
                        for related in get_related(eval("model.%s" % field),depth+1):
                            objects.add(related)
            objects.add(model)
    return list(objects)


class XMLExport(http.Controller):




    @http.route('/web/export/xml', type='http', auth='user')
    def export_xls_view(self, data, token):
        
        _logger.info("XMLEport data %s " % (data)) 

        data = json.loads(data)
        model = data.get('model', [])
        rows = data.get('rows', [])
    
        _logger.info("XMLEport model %s rows %s" % (model,rows)) 

        document = etree.tostring(export_xml(get_related(request.registry[model].browse(request.cr,request.uid,rows),0)),pretty_print=True,encoding="utf-8")
        
        return request.make_response(
            document,
            headers=[
                ('Content-Disposition', 'attachment; filename="%s.xml"'
                 % model),
                ('Content-Type', 'application/rdf+xml'),
                ('Content-Length', len(document)),
            ]
        )
        

    #~ @http.route('/model/<model("ir.model"):model>/all/xml', type='http', auth='public')
    #~ def export_xls_view(self, model=False, res_id=None):     
        #~ document = etree.tostring(export_xml(get_related(request.registry[model.model].browse(request.cr,request.uid,request.registry[model.model].search(request.cr,request.uid,[])),0)),pretty_print=True,encoding="utf-8")
        #~ return request.make_response(
            #~ document,
            #~ headers=[
                #~ ('Content-Disposition', 'attachment; filename="%s.xml"' % model.model),
                #~ ('Content-Type', 'application/rdf+xml'),
                #~ ('Content-Length', len(document)),
            #~ ]
        #~ )

        
    @http.route('/model/<model("ir.model"):model>/<int:res_id>/xml', type='http', auth='public')
    def export_xls_view(self, model=False, res_id=None):
        records =  res_id if res_id else request.registry[model.model].search(request.cr,request.uid,[])
        document = etree.tostring(export_xml(get_related(request.registry[model.model].browse(request.cr,request.uid,records),0)),pretty_print=True,encoding="utf-8")
        return request.make_response(
            document,
            headers=[
                ('Content-Disposition', 'attachment; filename="%s.xml"' % model.model),
                ('Content-Type', 'application/rdf+xml'),
                ('Content-Length', len(document)),
            ]
        )

    @http.route('/mod/<string:model>/<int:res_id>/xml', type='http', auth='public')
    def export_xls_view(self, model=False, res_id=None):
        records =  res_id if res_id else request.registry[model].search(request.cr,request.uid,[])
        document = etree.tostring(export_xml(get_related(request.registry[model].browse(request.cr,request.uid,records),0)),pretty_print=True,encoding="utf-8")
        return request.make_response(
            document,
            headers=[
                ('Content-Disposition', 'attachment; filename="%s.xml"' % model),
                ('Content-Type', 'application/rdf+xml'),
                ('Content-Length', len(document)),
            ]
        )

