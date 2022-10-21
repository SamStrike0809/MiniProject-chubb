$(document).ready(function () {
  $('#example').DataTable({ searching: false, paging: false, info: false});
});



// $("form").submit((e) => {
//   var name = $("#name").val();
//   var address = $("#address").val();
//   var phonenumber = $("#phonenumber").val();
//   var plate = $("#licenseplate").val();
//   console.log(name, address, phonenumber, plate);
//   data = {
//     name: name,
//     address: address,
//     phonenumber: phonenumber,
//     licenseplate: plate,
//   };
//   $.ajax({
//     url: "/savedetails1",
//     type: "POST",
//     dataType: "json",
//     contentType: "application/json; charset=utf-8",
//     data: JSON.stringify(data),
//     success: function (result) {
//       console.log(result);
//     },
//   });
// });

$("td i").click((e) => {
  plate = e.target.id;
  $.ajax({
    url: "/deleterecord1",
    type: "POST",
    data: JSON.stringify({ platenumber: plate }),
    dataType: "json",
    contentType: "application/json; charset=utf-8",
    success: function (result) {
      console.log("DELETED: ", plate);
      location.href = "/add1"
      $(".tr").load();
      $('table');
    }
  });
  console.log("clicked", e.target.id);
});

$(document).ready(function () {
  $("#myInput").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#myTable tr").filter(function () {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});

$('#restore').click(() => {
  $.ajax({
    url: "/restore1",
    success: function (res) {
      console.log(res);
      location.href = "/add1"
    }
  })
})

$('#example').on( 'click', 'tbody td:not(:first-child)', function (e) {
  console.log(e.target)
  editor.inline( this );
} );
