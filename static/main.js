// $(function () {
//   function tag(params) {
//     var data = {
//       'form-TOTAL_FORMS': $("[name = 'form-TOTAL_FORMS']").val(),
//       'form-INITIAL_FORMS': $("[name = 'form-INITIAL_FORMS']").val(),
//       'form-MAX_NUM_FORMS': $("[name = 'form-MAX_NUM_FORMS']").val(),
//       'form-MIN_NUM_FORMS': $("[name = 'form-MIN_NUM_FORMS']").val(),
//       quiz_title: $("[name = 'quiz_title']").val(),
//       quiz_text: $("[name = 'quiz_text']").val(),
//       question_text: $("[name = 'question_text']").val(),
//       'form-0-choice_text': $("[name = 'form-0-choice_text']").val(),
//       'form-1-choice_text': $("[name = 'form-1-choice_text']").val(),
//       'form-2-choice_text': $("[name = 'form-2-choice_text']").val(),
//       'form-3-choice_text': $("[name = 'form-3-choice_text']").val(),
//       'form-0-mark': $("[name = 'form-0-mark']").val(),
//       'form-1-mark': $("[name = 'form-1-mark']").val(),
//       'form-2-mark': $("[name = 'form-2-mark']").val(),
//       'form-3-mark': $("[name = 'form-3-mark']").val(),
//       duration: $("[name = 'duration']").val(),
//       csrfmiddlewaretoken: $("[name= 'csrfmiddlewaretoken']").val(),
//       url: $(location).attr('href'),
//     };
//     for (var property in data) {
//       if (!data[property]) {
//         delete data[property];
//       }
//     }
//     return data;
//   }

//   $('#move > #move1 > #finish').click(function (e) {
//     data = tag();
//     data['finish'] = true;
//     $.ajax({
//       type: 'POST',
//       url: data['url'],
//       data: data,
//       success: function (response) {
//         window.location.replace('/dashboard/quizzes/');
//         console.log(response);
//       },
//       error: function () {
//         console.error('error');
//       },
//     });
//   });

//   $('#move > #move1 > #continue').click(function (e) {
//     data = tag();
//     data['continue'] = true;
//     $.ajax({
//       type: 'POST',
//       url: data['url'],
//       data: data,
//       success: function (response) {
//         window.location.replace(
//           '/dashboard/quiz/' + response + '/create-question-choice/'
//         );
//         console.log(data);
//       },
//       error: function () {
//         console.error('error');
//       },
//     });
//   });
// });
