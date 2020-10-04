$(function () {

  function finish() {
    var start = localStorage.getItem('start')
    var time_spent = (new Date().getTime() - start)
    var hours = Math.floor(
      (time_spent % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((time_spent % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((time_spent % (1000 * 60)) / 1000);
    var time_used = ((hours < 10 ? '0' : '') + hours) + ':' + ((minutes < 10 ? '0' : '') + minutes) + ':' + ((seconds < 10 ? '0' : '') + seconds)
    $("input[name= 'elapse']").val(time_used)
  }

  var end = localStorage.getItem('end')
  var x = setInterval(() => {
    var now = new Date().getTime();
    var duration = end - now;

    var hours = Math.floor(
      (duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );
    var minutes = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((duration % (1000 * 60)) / 1000);

    $('#timer').text(
      ((hours < 10 ? '0' : '') + hours) + ':' + ((minutes < 10 ? '0' : '') + minutes) + ':' + ((seconds < 10 ? '0' : '') + seconds)
    );

    if (minutes < 1 && seconds < 10){
      $('span.badge').removeClass('badge-primary');
      $('span.badge').addClass('badge-danger');
    }

    if (duration < 1) {
      clearInterval(x);
      finish();
      $('input#finish').click();
    }
  }, 1000);

  $('input#finish').click(function (e) {
    finish();
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
