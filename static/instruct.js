$(function () {
  var pk = () => $("[name='pk']").val();
  
  $('#exam_questions').click(function (e) {
    $.ajax({
      type: 'POST',
      url: '/exam/timer/',
      data: {
        pk: pk(),
        csrfmiddlewaretoken: $("input[name= 'csrfmiddlewaretoken']").val(),
      },
    });
  });

  // success: function (response) {
  //     var stoppage = response;
  //     var x = setInterval(() => {
  //       var now = new Date().getTime();
  //       var duration = stoppage - now;

  //       var days = Math.floor(duration / (1000 * 60 * 60 * 24));
  //       var hours = Math.floor(
  //         (duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
  //       );
  //       var minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
  //       var seconds = Math.floor((duration % (1000 * 60)) / 1000);

  //       $('#timer').text(
  //         days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's '
  //       );

  //       if (duration < 0) {
  //         clearInterval(x);
  //         $('#timer').html = 'EXPIRED';
  //       }
  //     }, 1000);
  //   },
});
