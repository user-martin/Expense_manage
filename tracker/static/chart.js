$(document).ready(function(){
$( "#selection-button" ).click(function() {
var airlineSelected = $('#airline-selected').find(":selected").val();


$.ajax({
     url: "/tracker",
     method: 'GET',
     data : {
             filter_category: parseInt(airlineSelected)
     },success: function(data){
         $('#main_content').empty().html(data);
     }, error: function(xhr, errmsg, err){
         console.log("error")
         console.log(error_data)
     }
});
});
});
