$(document).ready(function(){
    $(".card").click(function(evt){
        console.log($(this).attr("id"));  
        location.pathname =  $(this).attr("id");    
    });
 });
