# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class DPNachricht(Document):
	def validate(self):
		if not self.ungelesen:
			users = frappe.db.sql("""SELECT `name` FROM `tabDP User`""", as_dict=True)
			for user in users:
				row = self.append('ungelesen', {})
				row.user = user.name
