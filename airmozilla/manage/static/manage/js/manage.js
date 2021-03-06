// used when we update a label about the status on vid.ly about
// a piece of media
function process_vidly_status_response(response, $element) {
    if (response.status) {
        $element.text(response.status);
        console.log(response.status);
        if (response.status == 'Finished') {
            $element.addClass('label-success');
        } else if (response.status == 'Finished') {
            $element.addClass('label-success');
        } else if (response.status == 'Processing') {
            $element.addClass('label-info');
        } else if (response.status == 'New') {
            $element.addClass('label-inverse');
        } else if (response.status == 'Error') {
            $element.addClass('label-important');
        }
    } else {
        $element.text("Unknown").addClass('label-warning');
    }
}


$(function() {

  var title = null;
  if ($('h1:visible').size()) {
    if ($('h1:visible').size() == 1) {
      title = $('h1:visible').text();
    }
  } else if ($('h2:visible').size()) {
    if ($('h2:visible').size() == 1) {
      title = $('h2:visible').text();
    }
  }
  if (title) {
    document.title = title + ' - ' + document.title;
  }


});
