// add items to the "Add Items" tab

$(document).ready(function() {
  var items = [
   {
      "name" : "Arbeidsrom",
      "image" : "models/thumbnails/work_room.jpg",
      "model" : "models/js/work_room.js",
      "type" : "1"
    }, 
    {
      "name" : "Moterom",
      "image" : "models/thumbnails/meeting_room.jpg",
      "model" : "models/js/meeting_room.js",
      "type" : "1"
    }, 
    {
      "name" : "Apen plass",
      "image" : "models/thumbnails/open_work.jpg",
      "model" : "models/js/open_work.js",
      "type" : "1"
    }, 
   /*     
   {
      "name" : "",
      "image" : "",
      "model" : "",
      "type" : "1"
    }, 
    */
  ]



  var itemsDiv = $("#items-wrapper")
  for (var i = 0; i < items.length; i++) {
    var item = items[i];
    var html = '<div class="col-sm-4">' +
                '<a style="font-size:24px;text-align:center" class="thumbnail add-item" model-name="' + 
                item.name + 
                '" model-url="' +
                item.model +
                '" model-type="' +
                item.type + 
                '"><img src="' +
                item.image + 
                '" alt="Add Item"> '+
                item.name +
                '</a></div>';
    itemsDiv.append(html);
  }
});