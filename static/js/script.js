// window.parseISOString = function parseISOString(s) {
//   var b = s.split(/\D+/);
//   return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
// };
$(document).ready(function() {
  $('#nutrients').click(function(e) {
    e.preventDefault();
    event_target = e.target
    // target = $(event_target).prop('tagName');
    selected_value = event_target.text;
    $(".loader").css("display", "block"); 
    $.ajax({
      url: '/lookup/'+selected_value,
      type: 'GET',
      dataType: 'json',
      success: function(data) {
        // alert(data.data)
        $("#info-title").html(selected_value.split(',')[0])
        $(".loader").css('display', 'none');
        $("#info-text").html(data.data)
        $("#info-box").css("display", "block");

      }
    });

  });
});
