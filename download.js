return (function download( url, filename ) {
	var link = document.createElement('a');
	link.setAttribute('href',url);
	link.setAttribute('download',filename);
	var event = document.createEvent('MouseEvents');
	event.initMouseEvent('click', true, true, window, 1, 0, 0, 0, 0, false, false, false, false, 0, null);
	link.dispatchEvent(event);
})(arguments[0], arguments[1]);