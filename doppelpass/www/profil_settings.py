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
	
	context["user"] = frappe.get_doc("DP User", frappe.session.user)
	context["primar_bg"] = context["user"].primar_bg
	context["sekundaer_bg"] = context["user"].sekundaer_bg
	context["team_ansicht"] = context["user"].team_ansicht
	context["strasse"] = context["user"].strasse
	context["ort"] = context["user"].ort
	context["geburtsdatum"] = context["user"].geburtsdatum
	context["telefon"] = context["user"].telefon
	context["plz"] = context["user"].plz
	context["fullname"] = context["user"].fullname
	
	return context
	
@frappe.whitelist()
def primebackground_change(color):
	frappe.db.sql("""UPDATE `tabDP User` SET `primar_bg` = '{color}' WHERE `name` = '{user}'""".format(color=color, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'
	
@frappe.whitelist()
def secbackground_change(color):
	frappe.db.sql("""UPDATE `tabDP User` SET `sekundaer_bg` = '{color}' WHERE `name` = '{user}'""".format(color=color, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'
	
@frappe.whitelist()
def team_ansicht_change(team_ansicht):
	frappe.db.sql("""UPDATE `tabDP User` SET `team_ansicht` = '{team_ansicht}' WHERE `name` = '{user}'""".format(team_ansicht=team_ansicht, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'
	
@frappe.whitelist()
def update_kontakt(fullname, plz, telefon, geburtsdatum, ort, strasse):
	frappe.db.sql("""UPDATE `tabDP User` SET `fullname` = '{fullname}',
												`plz` = '{plz}',
												`telefon` = '{telefon}',
												`geburtsdatum` = '{geburtsdatum}',
												`ort` = '{ort}',
												`strasse` = '{strasse}'
					WHERE `name` = '{user}'""".format(fullname=fullname, plz=plz, telefon=telefon, geburtsdatum=geburtsdatum, ort=ort, strasse=strasse, user=frappe.session.user), as_list=True)
	frappe.db.commit()
	return 'ok'