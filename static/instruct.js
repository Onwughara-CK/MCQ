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
});
