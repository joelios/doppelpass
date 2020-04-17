# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

def get_context(context):
	context["trainings"] = frappe.db.sql("""SELECT `name`, `datum`, `team` FROM `tabTraining` ORDER BY `datum` ASC""", as_dict=True)
	return context
	
@frappe.whitelist()
def get(training):
	return frappe.db.sql("""SELECT `details`, `ort`, `datum`, `team` FROM `tabTraining` WHERE `name` = '{training}'""".format(training=training), as_dict=True)[0]
	
@frappe.whitelist()
def update(training, ort, datum, details, team):
	frappe.db.sql("""UPDATE `tabTraining` SET `details` = '{details}', `ort` = '{ort}', `datum` = '{datum}', `team` = '{team}' WHERE `name` = '{training}'""".format(training=training, details=details, ort=ort, datum=datum, team=team), as_list=True)
	return 'ok'