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
	
	context["saldo"] = frappe.db.get_single_value('DP Kasse', 'saldo')
	context["bezahlt"] = frappe.db.get_single_value('DP Kasse', 'bezahlt')
	context["offen"] = frappe.db.get_single_value('DP Kasse', 'offen')
	context["bussen"] = frappe.db.sql("""SELECT
											`tabDP Bussen`.`betrag`,
											`tabDP User`.`fullname`,
											`tabDP Bussen`.`begruendung`
										FROM `tabDP Bussen`
										INNER JOIN `tabDP User`
										ON `tabDP Bussen`.`user` = `tabDP User`.`name`""", as_dict=True)
	
	return context