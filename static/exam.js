$(function () {
  $('#exam').on('change', function () {
    var selectedId = $('input[name=choice]:checked', '#exam').attr('id');
    var selectedValue = $('input[name=choice]:checked', '#exam').attr('value');
    data = {
      [selectedId]: selectedValue,
      csrfmiddlewaretoken: $("input[name= 'csrfmiddlewaretoken']").val(),
    };

    console.log(data);
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
