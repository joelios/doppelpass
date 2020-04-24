# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import nowdate

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	
	user = frappe.get_doc("DP User", frappe.session.user)
	context["primar_bg"] = user.primar_bg
	context["sekundaer_bg"] = user.sekundaer_bg
	
	try:
		# heutiger event
		context["event"] = frappe.db.sql("""SELECT
												`tabDP Event`.`typ`,
												`tabDP Event`.`start`,
												`tabDP Event`.`ort`,
												`tabDP Event`.`name`,
												`tabDP Event`.`gegner`
											FROM `tabDP Event`
											WHERE DATE(`start`) = '{nowdate}'
											ORDER BY `start` ASC
											LIMIT 1""".format(nowdate=nowdate()), as_dict=True)[0]
		event = frappe.get_doc("DP Event", context["event"]["name"])
		context["anwesend"] = False
		context["anzahl"] = len(event.anmeldungen)
		for teilnehmer in event.anmeldungen:
			if frappe.session.user == teilnehmer.user:
				context["anwesend"] = teilnehmer.name
	except:
		context["event"] = None
		context["anwesend"] = False
				
	# alle events in zukunft
	context["events_in_zukunft"] = frappe.db.sql("""SELECT
													`tabDP Event`.`typ`,
													`tabDP Event`.`start`,
													`tabDP Event`.`ort`,
													`tabDP Event`.`name`,
												`tabDP Event`.`gegner`
												FROM `tabDP Event`
												WHERE DATE(`start`) > '{nowdate}'
												ORDER BY `start` ASC""".format(nowdate=nowdate()), as_dict=True)
	context["details_zu_events"] = {}
	for _event in context["events_in_zukunft"]:
		_event = frappe.get_doc("DP Event", _event.name)
		context["details_zu_events"][_event.name] = {}
		context["details_zu_events"][_event.name]["anwesend"] = False
		context["details_zu_events"][_event.name]["anzahl"] = len(_event.anmeldungen)
		for teilnehmer in _event.anmeldungen:
			if frappe.session.user == teilnehmer.user:
				context["details_zu_events"][_event.name]["anwesend"] = teilnehmer.name
	
	return context