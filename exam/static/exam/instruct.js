$(function () {

  var pk = $("[name='pk']").val();
  var duration_ms;

  $.ajax({
    type: 'POST',
    url: '/exam/timer/',
    data: { 
      pk: pk,
      csrfmiddlewaretoken: $("input[name= 'csrfmiddlewaretoken']").val(),
    },
    success: function (response) {
      var arr = response.split(':');
      var secs = 0, multiplier = 1;
      while (arr.length > 0){
        secs += multiplier * parseInt(arr.pop(),10)
        multiplier *= 60
      }
      duration_ms = secs * 1000;
    },
  });

  $('a#start').click(function (e) { 
      var start = new Date().getTime();
      var end = duration_ms + start;
      localStorage.setItem('start', start)
      localStorage.setItem('end', end)    
  });

});
