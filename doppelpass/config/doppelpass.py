from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Spieler"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "DP User",
					"label": "Spieler / Trainer",
					"description": _("Spieler / Trainer"),
					"onboard": 1
				}
			]
		},
		{
			"label": _("Events und Abstimmungen"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "DP Event",
					"label": "Events",
					"description": _("Events"),
					"onboard": 1
				},
				{
					"type": "doctype",
					"name": "DP Abstimmung",
					"label": "Abstimmungen",
					"description": _("Abstimmungen"),
					"onboard": 1
				}
			]
		},
		{
			"label": _("Diverses"),
			"icon": "fa fa-star",
			"items": [
				{
					"type": "doctype",
					"name": "DP Nachricht",
					"label": "Nachrichten",
					"description": _("Nachrichten"),
					"onboard": 1
				},
				{
					"type": "doctype",
					"name": "DP Kasse",
					"label": "Kasse",
					"description": _("Kasse"),
					"onboard": 1
				}
			]
		}
	]
