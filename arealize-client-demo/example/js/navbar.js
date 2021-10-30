var navbar = $("#navbar");

navbar.click(function() {
     var modal = $("#modal")
    var bar1 = $("#bar1")
    var bar2 = $("#bar2")
    var bar3 = $("#bar3")

     if (navbar.hasClass("modal-open")){
         navbar.removeClass("modal-open")
         bar1.removeClass("active1")
         bar2.removeClass("active2")
         bar3.removeClass("active3")
         modal.hide()

         
         
     } else {
         navbar.addClass("modal-open")
         bar1.addClass("active1")
         bar2.addClass("active2")
         bar3.addClass("active3")
         modal.show()
     }
     
});