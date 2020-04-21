function abstimmen(abstimmung, antwort) {
	frappe.call({
		method: 'doppelpass.www.abstimmungen.abstimmen',
		args: {
			'abstimmung': abstimmung,
			'neue_antwort': antwort
		},
		callback: function(r) {
			if(r.message) {
				location.reload();
			} 
		}
	});
}