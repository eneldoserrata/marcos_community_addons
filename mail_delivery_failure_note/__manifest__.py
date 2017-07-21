# -*- coding: utf-8 -*-
# © 2017 Tobias Zehntner
# © 2017 Niboo SPRL (https://www.niboo.be/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Mail - Delivery Failure Notification',
    'category': 'Mail',
    'summary': 'Notifications for delivery failures on emails from records',
    'description': """
If an email sent from a record (Invoice, SO etc) has a delivery failure
caused from:
- a subscriber having their notifications set to Never
- an exception during sending
it will be mentioned as an Internal Note on the record.
        """,
    'license': 'AGPL-3',
    'version': '10.0.1.0.0',
    'author': 'Niboo',
    'website': 'https://www.niboo.be',
    'depends': [
        'mail',
    ],
    'data': [
    ],
    'installable': True,
    'application': False,
}
