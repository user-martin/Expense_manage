$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-expense .modal-content").html("");
        $("#modal-expense").modal("show");
      },
      success: function (data) {
        $("#modal-expense .modal-content").html(data.html_form);
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
          $("#expense-table tbody").html(data.html_expense_list);
          $("#modal-expense").modal("hide");
        }
        else {
          $("#modal-expense .modal-content").html(data.html_form);
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
          $("#expense-table tbody").html(data.html_expense_list);
          $('#success_message').fadeIn().html("Submit Successfully");
				          setTimeout(function() {
					$('#success_message').fadeOut("slow");
				                  }, 2000 );
        }
        else {
          $("#modal-expense .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-expense").click(loadForm);
  $("#modal-expense").on("submit", ".js-expense-create-form", savenewForm);


  // Create formset
  $(".js-create-expense_set").click(loadForm);
  $("#modal-expense").on("submit", ".js-expense-create-formset", saveForm);


  // Update formset
  $(".js-update-expense_set").click(loadForm);
  $("#modal-expense").on("submit", ".js-expense-update-formset", saveForm);


  // Update book
  $("#expense-table").on("click", ".js-update-expense", loadForm);
  $("#modal-expense").on("submit", ".js-expense-update-form", saveForm);

  // Delete book
  $("#expense-table").on("click", ".js-delete-expense", loadForm);
  $("#modal-expense").on("submit", ".js-expense-delete-form", saveForm);

});
