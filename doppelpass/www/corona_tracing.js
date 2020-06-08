function get_corona_tracing() {
	var datum = $('#datum').val();
	var spieler = $('#spieler').val();
	if (!datum||spieler == 'leer') {
		frappe.msgprint("Bitte wählen Sie ein Datum und einen Spieler!", "Fehlende Angaben");
	} else {
		console.log(datum);
		console.log(spieler);
		frappe.call({
			method: 'doppelpass.www.corona_tracing.get_corona_tracing',
			args: {
				datum: datum,
				spieler: spieler
			},
			callback: function(r) {
				if(r.message) {
					frappe.msgprint("Sie erhalten in Kürze ein Mail mit den angeforderten Daten.", "Siehe Mail");
				} 
			}
		});
	}
}