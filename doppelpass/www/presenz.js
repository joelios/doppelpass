function show_teilnehmer(event) {
	console.log(event);
	frappe.call({
		method: 'doppelpass.www.presenz.show_teilnehmer',
		args: {
			event: event
		},
		callback: function(r) {
			if(r.message) {
				console.log(r.message);
				var nachricht = '<table style="width: 100%;"><thead><tr><th>Spieler</th><th>Position</th></thead><tbody>';
				for (var i = 0; i < r.message.length; i++) {
					nachricht += '<tr><td>' + r.message[i][0] + '</td><td>' + r.message[i][1] + '</td></tr>';
				}
				nachricht += '</tbody></table>';
				frappe.msgprint(nachricht, 'Anmeldungen Event');
				//frappe.msgprint(nachricht, 'Anmeldungen Event <div class="pull-right"><i class="fas fa-times" onclick="location.reload();"></i></div>');
			} 
		}
	});
}