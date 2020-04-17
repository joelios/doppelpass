# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

@frappe.whitelist()
def add(team, datum, ort, details=None):
	training = frappe.get_doc({
		"doctype": "Training",
		"team": team,
		"datum": datum,
		"ort": ort,
		"details": details or ''
	})
	training.insert(ignore_permissions=True)
	return training.name