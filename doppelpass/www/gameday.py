# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils.data import now_datetime, nowdate
from doppelpass.swissunihockey import get_resultate, get_tabelle

no_cache = 1

def get_context(context):
	if frappe.session.user=='Guest':
		frappe.throw(_("You need to be logged in to access this page"), frappe.PermissionError)
	
	# allgemein
	user = frappe.get_doc("DP User", frappe.session.user)
	
	# event
	try:
		context["event"] = frappe.db.sql("""SELECT * FROM `tabDP Event`
											WHERE `start` >= '{nowdate}'
											ORDER BY `start` ASC
											LIMIT 1""".format(nowdate=now_datetime()), as_dict=True)[0]
											
		context["aufgebot"] = frappe.db.sql("""SELECT * FROM `tabTeilnehmer`
											WHERE `parent` = '{event}'""".format(event=context["event"].name), as_dict=True)
											
		context["starting_lines"] = frappe.db.sql("""SELECT * FROM `tabStart Linien`
											WHERE `parent` = '{event}' ORDER BY `linie` ASC""".format(event=context["event"].name), as_dict=True)
											
		context["match_linien"] = frappe.db.sql("""SELECT * FROM `tabMatch Linien`
											WHERE `parent` = '{event}' ORDER BY `linie` ASC""".format(event=context["event"].name), as_dict=True)
	except:
		context["event"] = None
		
	return context