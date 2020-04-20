# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import now_datetime

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	
	try:
		context["event"] = frappe.db.sql("""SELECT
												`tabDP Event`.`typ`,
												`tabDP Event`.`start`,
												`tabDP Event`.`ort`,
												`tabDP Event`.`name`
											FROM `tabDP Event`
											WHERE `start` >= '{nowdate}'
											ORDER BY `start` ASC
											LIMIT 1""".format(nowdate=now_datetime()), as_dict=True)[0]
		event = frappe.get_doc("DP Event", context["event"]["name"])
		context["anwesend"] = False
		context["anzahl"] = len(event.anmeldungen)
		for teilnehmer in event.anmeldungen:
			if frappe.session.user == teilnehmer.user:
				context["anwesend"] = teilnehmer.name
	except:
		context["event"] = None
		context["anwesend"] = False
	
	return context
	
@frappe.whitelist()
def abmelden(ref):
	frappe.db.sql("""DELETE FROM `tabTeilnehmer` WHERE `name` = '{ref}'""".format(ref=ref), as_list=True)
	return True
	
@frappe.whitelist()
def anmelden(event):
	event = frappe.get_doc("DP Event", event)
	row = event.append('anmeldungen', {})
	row.user = frappe.session.user
	event.save(ignore_permissions=True)
	return True