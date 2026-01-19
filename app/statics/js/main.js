$(document).on('shown.bs.modal', '#modal-delete', function (event) {
  var element = $(event.relatedTarget);

  var name = element.data("name");
  var pk = element.data("pk");
  $("#modal-delete-text").text("Вы действительно хотите удалить " + name + " " + pk + " ?");

  $("#modal-delete-button").attr("data-url", element.data("url"));
});

$(document).on('click', '#modal-delete-button', function () {
  console.log($(this).attr('data-url'));
  $.ajax({
    url: $(this).attr('data-url'),
    method: 'DELETE',
    success: function (result) {
      window.location.href = result;
    },
    error: function (request, status, error) {
      alert(request.responseText);
    }
  });
});

$(document).on('click', '#search-button', function () {
  var searchTerm = encodeURIComponent($("#search-input").val());

  newUrl = "";
  if (window.location.search && window.location.search.indexOf('search=') != -1) {
    newUrl = window.location.search.replace(/search=[^&]*/, "search=" + searchTerm);
  } else if (window.location.search) {
    newUrl = window.location.search + "&search=" + searchTerm;
  } else {
    newUrl = window.location.search + "?search=" + searchTerm;
  }
  window.location.href = newUrl;
});

$(document).on('click', '#search-reset', function () {
  if (window.location.search && window.location.search.indexOf('search=') != -1) {
    window.location.href = window.location.search.replace(/search=[^&]*/, "");
  }
});

$(document).on('keypress', '#search-input', function (e) {
  if (e.which === 13) {
    $('#search-button').click();
  }
});

var timeout = null;

$(document).on('keyup', '#search-input', function (e) {
  clearTimeout(timeout);
  timeout = setTimeout(function () {
    $('#search-button').click();
  }, 1000);
});

$(':input[data-role="datepicker"]:not([readonly])').each(function () {
  $(this).flatpickr({
    enableTime: false,
    allowInput: true,
    dateFormat: "Y-m-d",
  });
});


$(':input[data-role="datetimepicker"]:not([readonly])').each(function () {
  $(this).flatpickr({
    enableTime: true,
    allowInput: true,
    enableSeconds: true,
    time_24hr: true,
    dateFormat: "Y-m-d H:i:s",
  });
});


$(':input[data-role="select2-ajax"]').each(function () {
  $(this).select2({
    minimumInputLength: 1,
    ajax: {
      url: $(this).data("url"),
      dataType: 'json',
      data: function (params) {
        var query = {
          name: $(this).attr("name"),
          term: params.term,
        }
        return query;
      }
    }
  });

  existing_data = $(this).data("json") || [];
  for (var i = 0; i < existing_data.length; i++) {
    data = existing_data[i];
    var option = new Option(data.text, data.id, true, true);
    $(this).append(option).trigger('change');
  }
});


$("#select-all").click(function () {
  $('input.select-box:checkbox').prop('checked', this.checked);
});


$("#action-delete").click(function () {
  var pks = [];
  $('.select-box').each(function () {
    if ($(this).is(':checked')) {
      pks.push($(this).siblings().get(0).value);
    }
  });

  $('#action-delete').data("pk", pks);
  $('#action-delete').data("url", $(this).data('url') + '?pks=' + pks.join(","));
  $('#modal-delete').modal('show');
});

$("[id^='action-custom-']").click(function () {
  var pks = [];
  $('.select-box').each(function () {
    if ($(this).is(':checked')) {
      pks.push($(this).siblings().get(0).value);
    }
  });

  window.location.href = $(this).attr('data-url') + '?pks=' + pks.join(",");
});

$(':input[data-role="select2-tags"]').each(function () {
  $(this).select2({
    tags: true,
    multiple: true,
  });

  existing_data = $(this).data("json") || [];
  for (var i = 0; i < existing_data.length; i++) {
    var option = new Option(existing_data[i], existing_data[i], true, true);
    $(this).append(option).trigger('change');
  }
});
