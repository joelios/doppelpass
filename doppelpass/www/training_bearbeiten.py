# -*- coding: utf-8 -*-
# Copyright (c) 2020, msmr.ch and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

no_cache = 1

def get_context(context):
	context["trainings"] = frappe.db.sql("""SELECT `name`, `datum`, `team`, FROM `tabTraining`""", as_dict=True)
	return context