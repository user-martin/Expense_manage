$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-income .modal-content").html("");
        $("#modal-income").modal("show");
      },
      success: function (data) {
        $("#modal-income .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#income-table tbody").html(data.html_income_list);
          $("#modal-income").modal("hide");
        }
        else {
          $("#modal-income .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  var savenewForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#income-table tbody").html(data.html_income_list);
          $('#success_message').fadeIn().html("Submit Successfully");
				          setTimeout(function() {
					$('#success_message').fadeOut("slow");
				                  }, 2000 );
        }
        else {
          $("#modal-income .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-income").click(loadForm);
  $("#modal-income").on("submit", ".js-income-create-form", savenewForm);

  // Update book
  $("#income-table").on("click", ".js-update-income", loadForm);
  $("#modal-income").on("submit", ".js-income-update-form", saveForm);

  // Delete book
  $("#income-table").on("click", ".js-delete-income", loadForm);
  $("#modal-income").on("submit", ".js-income-delete-form", saveForm);

});
