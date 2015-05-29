var getQuerystring, initCarousel, initEditorialLabel;

getQuerystring = function(key) {
  var regex, result, temp;
  regex = new RegExp('(?:\\?|&)' + key + '=(.*?)(?=&|$)', 'gi');
  result = [];
  while ((temp = regex.exec(document.location.search)) !== null) {
    result.push(temp[1]);
  }
  return result;
};

initCarousel = function() {
  $('.tabs-carousel').owlCarousel({
    items: 1,
    lazyLoad: true,
    animateOut: 'fadeOut',
    animateIn: 'fadeIn'
  });
  return $('.banner-carousel').owlCarousel({
    items: 1,
    lazyLoad: true,
    autoplay: true,
    loop: true,
    animateOut: 'fadeOut',
    animateIn: 'fadeIn',
    dots: true
  });
};

initEditorialLabel = function() {
  if (getQuerystring('editorial')) {
    return $('.posts-header .posts-header-title').show();
  } else if (getQuerystring('author')) {
    return $('.posts-header .posts-header-title').show();
  }
};

$(document).foundation();

$(document).ready(function() {
  initCarousel();
  $('.search input[type=text]').val(getQuerystring('keywords'));
  if (getQuerystring('editorial').length > 0 && getQuerystring('editorial')[0] !== "") {
    initEditorialLabel();
    return $('.search select').val(getQuerystring('editorial'));
  }
});

$('.dropdown .dropdown').hover(function() {
  return $(this).closest('.has-dropdown').find('a').eq(0).toggleClass("active");
});


$('.carousel__video').owlCarousel({
    items:1,
    merge:true,
    loop:true,
    margin:10,
    video:true,
    lazyLoad:true,
    center:true,
    videoWidth: 700,
    videoHeight: 394,
    autoplay: true,
    responsive:{
        480:{
            items:2
        },
        600:{
            items:4
        }
    }
})

var scrollHandler = function() {
    var scrollTop = $(window).scrollTop();
    var heroHeight = $('#header').outerHeight();

    if (scrollTop > heroHeight) {
        classie.remove(document.getElementById('header-fixed'), 'fadeOutUp');
        classie.add(document.getElementById('header-fixed'), 'appeared');
        classie.add(document.getElementById('header-fixed'), 'show');
        classie.add(document.getElementById('header-fixed'), 'fadeInDown');
    } else if (scrollTop < heroHeight) {
        classie.add(document.getElementById('header-fixed'), 'fadeOutUp');
        classie.remove(document.getElementById('header-fixed'), 'fadeInDown');
    }
};

$(window).scroll(scrollHandler);