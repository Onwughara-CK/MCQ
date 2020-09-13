$(function () {
  $.ajax({
    type: 'GET',
    url: '/exam/timer/',
    success: function (response) {
      var deadline = response;
      var x = setInterval(() => {
        var now = new Date().getTime();
        var duration = deadline - now;

        var days = Math.floor(duration / (1000 * 60 * 60 * 24));
        var hours = Math.floor(
          (duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
        );
        var minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((duration % (1000 * 60)) / 1000);

        $('#timer').text(
          days + 'd ' + hours + 'h ' + minutes + 'm ' + seconds + 's '
        );

        if (duration <= 0) {
          clearInterval(x);
          $('input#finish').click();
        }
      }, 1000);
    },
  });

  $('#exam').on('change', function () {
    var selectedId = $('input[name=choice]:checked', '#exam').attr('id');
    data = {
      [selectedId]: $('input[name=choice]:checked', '#exam').attr('value'),
      csrfmiddlewaretoken: $("input[name= 'csrfmiddlewaretoken']").val(),
    };

    $.ajax({
      type: 'POST',
      url: '/exam/result/',
      data: data,
    });
  });

  $.ajax({
    type: 'GET',
    url: '/exam/result/',
    success: function (response) {
      for (var key in response) {
        $('input[name=choice][value =' + response[key] + ']').prop(
          'checked',
          true
        );
      }
    },
  });
});
