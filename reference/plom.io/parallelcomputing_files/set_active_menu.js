




/*
     FILE ARCHIVED ON 19:12:42 Aug 22, 2013 AND RETRIEVED FROM THE
     INTERNET ARCHIVE ON 14:28:11 Jul 22, 2014.
     JAVASCRIPT APPENDED BY WAYBACK MACHINE, COPYRIGHT INTERNET ARCHIVE.

     ALL OTHER CONTENT MAY ALSO BE PROTECTED BY COPYRIGHT (17 U.S.C.
     SECTION 108(a)(3)).
*/
//set the active class of the navbar
$(document).ready(function() {
  var pathname = window.location.pathname;

  var root = '/' + pathname.split('/')[1];

  if(root !== '/review' && root !== '/requests'){
    $('ul.nav li').removeClass('active');
  }


  $('ul.nav a[href= "' + root + '"]').parent().addClass('active');
})
