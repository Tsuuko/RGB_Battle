$(function(){
  $('a.fadelink').on("click",function() {
    var url = $(this).attr('href');
    if (url != '') {
      $('body').fadeOut(800);
      setTimeout(function(){
        location.href = url;
      }, 800);
    }
    return false;
  });
});