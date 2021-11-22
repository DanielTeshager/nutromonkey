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
        // scroll to the info-box div
        // $('html, body').animate({
        //   scrollTop: $("#info-box").offset().top
        // }, 2000);
        // set the info-box div title
        $("#info-title").html(selected_value.split(',')[0])
        // remove the loading animation
        $(".loader").css('display', 'none');
        // set the info-box div content and show it
        $("#info-text").html(data.data)
        $("#info-box").css("display", "block");
      }
    });

  });
// show hide wiki description
$(".wiki-description").on("click", function(e) {
  e.preventDefault();
  
  if (e.target.tagName == "A") {
    $(".additional-info").toggle();
    if ($(".additional-info").is(":visible")) {
      $("#show-more-less").html("Show Less");
    }
    else {
      $("#show-more-less").html("Show More");
    }

  }

});
  
});
