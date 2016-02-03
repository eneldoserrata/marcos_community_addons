# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2015 be-cloud.be
#                       Jerome Sonnet <jerome.sonnet@be-cloud.be>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Google Drive Attachment',
    'version': '1.0',
    'category': 'Tools',
    'description': """
Module that allows to attach a Google Drive Document.
    """,
    'author': "be-cloud.be (Jerome Sonnet)",
    'website': 'http://www.be-cloud.be',
    'license': 'AGPL-3',
    'depends': [
        'document',
    ],
    'data': [
        'res_config.xml',
        'view/document_gdrive_view.xml',
    ],
    'qweb': [
        'static/src/xml/gdrive.xml',
    ],
    "installable": True,
}
