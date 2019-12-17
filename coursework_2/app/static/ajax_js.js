$(document).ready(function() {

  $("#add").on("click", function() {
    var clicked = $(this);
    var book_id = $("#add input").attr("id");
    console.log(clicked);

    $.ajax({
      url: '/add_book',

      type: 'POST',

      data: JSON.stringify({ book_id: book_id }),

      contentType: "application/json; charset=utf-8",

      dataType: "json",

      success: function(response){
        console.log(response);

        $("#success").text("Book successfully added to collection!")
      },

      error: function(error){
        console.log(error);
      }
    });
  });
});
