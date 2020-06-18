# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DPEvent(Document):
	def validate(self):
		if not self.anmeldungen:
			users = frappe.db.sql("""SELECT `name`, `fullname` FROM `tabDP User`""", as_dict=True)
			for user in users:
				row = self.append('anmeldungen', {})
				row.user = user.name
				row.fullname = user.fullname
				
@frappe.whitelist()
def add_spieler(spieler, fullname):
	try:
		events = frappe.db.sql("""SELECT `name` FROM `tabDP Event` WHERE `start` >= NOW()""", as_dict=True)
		for _event in events:
			event = frappe.get_doc("DP Event", _event.name)
			found = False
			for _spieler in event.anmeldungen:
				if _spieler == spieler:
					found = True
			if not found:
				row = event.append('anmeldungen', {})
				row.user = spieler
				row.fullname = fullname
				event.save()
		return 'ok'
	except Exception as e:
		return e