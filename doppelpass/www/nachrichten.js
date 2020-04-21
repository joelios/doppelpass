function toggle_hidden() {
	$('#to_hide_1').toggleClass("hidden");
	$('#to_hide_2').toggleClass("hidden");
	$('#to_hide_3').toggleClass("hidden");
	$('#to_show_1').toggleClass("hidden");
	$('#to_show_2').toggleClass("hidden");
}

function nachricht_speichern() {
	var _text = $('#details').val();
	if ((!_text)) {
		frappe.msgprint("Bitte tragen Sie eine Nachricht ein!", "Fehlende Angaben");
		return
	} else {
		frappe.call({
			method: 'doppelpass.www.nachrichten.add',
			args: {
				nachricht: _text
			},
			callback: function(r) {
				if(r.message) {
					$('#details').val('');
					toggle_hidden();
					location.reload();
				} 
			}
		});
	}
}