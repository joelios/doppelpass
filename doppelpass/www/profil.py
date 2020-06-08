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
	context["strasse"] = context["user"].strasse
	context["ort"] = context["user"].ort
	context["geburtsdatum"] = context["user"].geburtsdatum
	context["telefon"] = context["user"].telefon
	context["plz"] = context["user"].plz
	
	return context