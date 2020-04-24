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
	
	context["offen"] = frappe.db.sql("""SELECT * FROM `tabDP Abstimmung` WHERE `ende` > '{nowdate}' ORDER BY `ende` ASC""".format(nowdate=nowdate()), as_dict=True)
	
	context["auswahl"] = {}
	for abstimmung in context["offen"]:
		context["auswahl"][abstimmung.name] = {}
		context["auswahl"][abstimmung.name]["fragen"] = frappe.db.sql("""SELECT * FROM `tabDP Abstimmung Auswahl` WHERE `parent` = '{abstimmung}'""".format(abstimmung=abstimmung.name), as_dict=True)
		context["auswahl"][abstimmung.name]["total"] = int(frappe.db.sql("""SELECT SUM(`anzahl`) FROM `tabDP Abstimmung Auswahl` WHERE `parent` = '{abstimmung}'""".format(abstimmung=abstimmung.name), as_list=True)[0][0])
		try:
			context["auswahl"][abstimmung.name]["antwort"] = frappe.db.sql("""SELECT `antwort` FROM `tabDP Abstimmung Antworten` WHERE `parent` = '{abstimmung}' AND `user` = '{user}'""".format(abstimmung=abstimmung.name, user=frappe.session.user), as_list=True)[0][0]
		except:
			context["auswahl"][abstimmung.name]["antwort"] = None
		
	context["beendet"] = frappe.db.sql("""SELECT * FROM `tabDP Abstimmung` WHERE `ende` <= '{nowdate}' ORDER BY `ende` ASC""".format(nowdate=nowdate()), as_dict=True)
	for abstimmung in context["beendet"]:
		context["auswahl"][abstimmung.name] = {}
		context["auswahl"][abstimmung.name]["fragen"] = frappe.db.sql("""SELECT * FROM `tabDP Abstimmung Auswahl` WHERE `parent` = '{abstimmung}' ORDER BY `anzahl` DESC LIMIT 1""".format(abstimmung=abstimmung.name), as_dict=True)
		context["auswahl"][abstimmung.name]["total"] = int(frappe.db.sql("""SELECT SUM(`anzahl`) FROM `tabDP Abstimmung Auswahl` WHERE `parent` = '{abstimmung}'""".format(abstimmung=abstimmung.name), as_list=True)[0][0])
	
	return context
	
@frappe.whitelist()
def abstimmen(abstimmung, neue_antwort):
	abstimmung = frappe.get_doc("DP Abstimmung", abstimmung)
	for antwort in abstimmung.antworten:
		if antwort.user == frappe.session.user:
			reset_antwort(antwort.antwort)
			break
	add_abstimmung(neue_antwort, abstimmung.name)
	return 'ok'
			
def reset_antwort(antwort):
	try:
		alte_antwort = frappe.db.sql("""SELECT `name` FROM `tabDP Abstimmung Antworten` WHERE `antwort` = '{antwort}' AND `user` = '{user}' LIMIT 1""".format(antwort=antwort, user=frappe.session.user), as_list=True)[0][0]
		frappe.db.sql("""DELETE FROM `tabDP Abstimmung Antworten` WHERE `name` = '{antwort}' AND `user` = '{user}'""".format(antwort=alte_antwort, user=frappe.session.user), as_list=True)
		frappe.db.commit()
		alte_anzahl = int(frappe.db.sql("""SELECT `anzahl` FROM `tabDP Abstimmung Auswahl` WHERE `name` = '{antwort}'""".format(antwort=antwort), as_list=True)[0][0])
		anzahl = alte_anzahl - 1
		frappe.db.sql("""UPDATE `tabDP Abstimmung Auswahl` SET `anzahl` = '{anzahl}' WHERE `name` = '{antwort}'""".format(antwort=antwort, anzahl=anzahl), as_list=True)
		frappe.db.commit()
		return 'ok'
	except:
		return 'ok'
	
def add_abstimmung(antwort, abstimmung):
	abstimmung = frappe.get_doc("DP Abstimmung", abstimmung)
	row = abstimmung.append('antworten', {})
	row.antwort = antwort
	row.user = frappe.session.user
	abstimmung.save(ignore_permissions=True)
	frappe.db.commit()
	update_anzahl(antwort)
	return 'ok'
	
def update_anzahl(antwort):
	alte_anzahl = int(frappe.db.sql("""SELECT `anzahl` FROM `tabDP Abstimmung Auswahl` WHERE `name` = '{antwort}'""".format(antwort=antwort), as_list=True)[0][0])
	anzahl = alte_anzahl + 1
	frappe.db.sql("""UPDATE `tabDP Abstimmung Auswahl` SET `anzahl` = '{anzahl}' WHERE `name` = '{antwort}'""".format(antwort=antwort, anzahl=anzahl), as_list=True)
	frappe.db.commit()
	return 'ok'
	