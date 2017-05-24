.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

Export Current Model as XML
===========================

One of the best Odoo's features is exporting custom data as CSV. That 
feature is as great and advanced as limited for an everyday experience.
A lot of users want simply to export the tree view they are looking to
without bother what related records there are and what fields you need.

Exporting to XML are much easier as long as yout target system handles this
format. This export creates XML-records the pointed records and for all related 
records. The method tries to use external identifiers and when its missing it 
creates new ones.


Usage
=====

1) /model/<model-id>/<record_id>/xml
# http://stage.smart-eu.org/model/93/6/xml = exports all res.users id=6
2) /model/<model-id>/all/xml
# http://stage.smart-eu.org/model/93/all/xml = exports all res.users

# Example
# se_demo05 res.user id=93

You can find the model id in settings/database structure/models (technical settings)
and the record id for each instance of a model using the tree-view.

Many2many fields are not correctly exported yet.

not yet:
After you installed it, you'll find an additional link 'Export current Model'
right below the 'Export' one. By clicking on it you'll get a XML file contains
the same data of the Model you are looking at.

The methods
===========

This module consists of two methods/functions. 

export_xml([records])  # returns each record with all fields for that model as an xml-record
get_related([records]) # returns all related records for the list of records recursively

example:
    document = etree.tostring(export_xml(get_related(request.registry[model.model].browse(request.cr,request.uid,records),0)),pretty_print=True,encoding="utf-8")


Credits
=======

Vertel AB

Contributors
------------

 * Anders Wallenquist <anders.wallenquist@vertel.se>
