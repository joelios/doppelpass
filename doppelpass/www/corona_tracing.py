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
	context["users"] = frappe.db.sql("""SELECT * FROM `tabDP User` ORDER BY `fullname` ASC""", as_dict=True)
	
	return context
	
@frappe.whitelist()
def get_corona_tracing(datum, spieler):
	corona_tracing = frappe.get_doc({
		"doctype": "Corona Tracing",
		"datum": datum,
		"spieler": spieler,
		"empfaenger": frappe.session.user
	})
	corona_tracing.insert(ignore_permissions=True)
	return corona_tracing.name