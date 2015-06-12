// Regex summary
// . Any character except newline.
// \.  A period (and so on for \*, \(, \\, etc.)
// ^ The start of the string.
// $ The end of the string.
// \d,\w,\s  A digit, word character [A-Za-z0-9_], or whitespace.
// \D,\W,\S  Anything except a digit, word character, or whitespace.
// [abc] Character a, b, or c.
// [a-z] a through z.
// [^abc]  Any character except a, b, or c.
// aa|bb Either aa or bb.
// ? Zero or one of the preceding element.
// * Zero or more of the preceding element.
// + One or more of the preceding element.
// {n} Exactly n of the preceding element.
// {n,}  n or more of the preceding element.
// {m,n} Between m and n of the preceding element.
// ??,*?,+?,
// {n}?, etc.  Same as above, but as few as possible.
// (expr)  Capture expr for use with \1, etc.
// (?:expr)  Non-capturing group.
// (?=expr)  Followed by expr.
// (?!expr)  Not followed by expr.

// Foundation JavaScript
// Documentation can be found at: http://foundation.zurb.com/docs
$(document).foundation({});

/*  [GLOBAL] Functions
*******************************************************************/
  
  String.prototype.capitalizeFirstLetter = function() {
      return this.charAt(0).toUpperCase() + this.slice(1);
  }

  function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  function lock_screen(){
  }

  function unlock_screen(){
  }

  function chain_of_events(el){
    if (el.attr('data-events-before-request')){
      var events = el.attr('data-events-before-request').split(' ');

      for (var i = 0;i < events.length; i++){
        e = events[i].toString();
        
        switch(e){
          case 'beActive':
            $('a[data-eventsBeforeRequest=beActive]').removeClass('active');
            el.addClass('active');

            break;
          case 'fadeOut':
            el.fadeOut();

            break;
          case 'addDataIndex':
            el = addDataIndex(el);

            break;
          case 'remove':
            if (events[i + 1]){
              $(events[i + 1]).fadeOut(1000, function(){ 
                $(this).remove();
              })
            } else {
              el.fadeOut(1000, function(){ 
                $(this).remove();
              })
            }
          default:
            break;
        }
      }
    }

    return el;
  }

  function process_data(data){
    console.log(data)
    if (data['alert-success']){
      alertify.success(data['alert-success']);
    } 

    if (data['alert-error']){
      alertify.error(data['alert-error']);
    }

    setTimeout(function() {
      if (data['redirect']){
        window.location.replace(data['redirect']);
      } else {
        if (data['href']){
          get(data['href']);        
        } else if (data['template']){
          if(data['target']){
            $(data['target']).html(data['template']);
          } else {
           $('#page').html(data['template']);
          }
        }

        // if (data['alert-success']){
        //   alertify.success(data['alert-success']);
        // } 

        // if (data['alert-error']){
        //   alertify.error(data['alert-error']);
        // }
      }
    }, 1000);
  }

  function before_load(){

  }

  function get(url, lock){
    var lock = (typeof lock === 'undefined') ? 'true' : lock;

    if (lock == 'true'){
      lock_screen();
    }

    $.ajax({
      url     : url,
      type    : 'get',
      cache   : false,
      success : function(data){
        process_data(data);
      },
      error   : function(data){
        alertify.error('Erro desconhecido, por favor entrar em contato com os administradores!');     
      },
      complete: function(data){
        before_load();

        if (lock == 'true'){
          unlock_screen();
        }
      }
    });
  }

  function post(form, lock){
    var lock = (typeof lock === 'undefined') ? 'true' : lock;   
    
    if (lock == 'true'){
      lock_screen(); 
    }

    if (form.attr('data-custom')){
      if (typeof window[form.attr('data-custom')] === 'function'){
        var data = window[form.attr('data-custom')](form);
      }
    } else {
      var data = form.serialize();
    }

    var content = (form.attr('data-content') == 'false') ? false : 'application/x-www-form-urlencoded; charset=UTF-8';
    var process = (form.attr('data-process') == 'false') ? false : true; 

    $.ajax({
      url     : form.attr('action'),
      type    : form.attr('method'),
      data    : data,
      cache   : false,
      contentType: content,
      processData: process,
      success : function(data){
        process_data(data);
      },
      error   : function(data){
        alertify.error('Erro desconhecido, por favor entrar em contato com os administradores!');    
      },
      complete: function(data){
        before_load();

        if (lock == 'true'){
          unlock_screen();
        }
      }
    });
  }

/*  [GLOBAL] Calls
*******************************************************************/

  $(document).on('click', 'a[data-get]', function(e){
    e.preventDefault();

    el = $(this);

    if (!el.hasClass('active')){

      if (el.attr('data-confirm')){
        alertify.set({ labels : { ok: "Sim", cancel: "NÃ£o" } });
        
        alertify.confirm(el.attr('data-confirm'), function (e) {
          if (e) {
            el = chain_of_events(el);

            get(el.attr('data-get'), el.attr('data-lock')); 
          } else {
            alertify.log('AÃ§Ã£o cancelada.')
          }
        });
      } else {
        el = chain_of_events(el);

        get(el.attr('data-get'), el.attr('data-lock'));
      }
    }
  });

  $(document).on('click', '[data-submit]', function(e){
    e.preventDefault();

    var el = $(this);
    var form = el.closest('form');
    var form_valid = true;
    var required_fields = form.find('[data-required]');

    required_fields.each(function(index){
      var field = $(this);
      var error_msg = field.attr('data-required');

      if (field.val() == '' || field.val() == 0){
        field.addClass('invalid');
        alertify.error(error_msg);
        form_valid = false;
      }
    });
    
    if (form.attr('data-default')){
      form.submit();
    } else if (form_valid){
      post(form, form.attr('data-lock'));
    } 

    return false;
  })

  $(document).on('submit', 'form', function(){
    var el = $(this);
    var form_valid = true;
    var required_fields = el.find('[data-required]');

    required_fields.each(function(index){
      var field = $(this);
      var error_msg = field.attr('data-required');

      if (field.val() == '' || field.val() == 0){
        field.addClass('invalid');
        alertify.error(error_msg);
        form_valid = false;
      }
    });
    
    if (el.attr('data-default')){
      return true;
    } else if (form_valid){
      post(el, el.attr('data-lock'));
    } 

    return false;
  });

  $('#visibility').change(function(){
       cb = $(this);
       cb.val(cb.prop('checked').toString().capitalizeFirstLetter());
   });  

  $(document).ready(function(){
    $('#page').css('min-height', $('body').height() - 100);

    $('.project-box').each(function(){
      // $(this).css('background-color', getRandomColor());
    });

    $('.datepicker').pickadate({
        formatSubmit: 'yyyy/mm/dd',
    });
  });

  $( window ).resize(function() {
    $('#page').css('min-height', $('body').height() - 100);
  });

  $(document).on('click', '.hero__meta-anchor-login', function() {
    $('.hero__forms-login form').stop().animate({
        width: "100%",
        opacity: 1,
      }, 1000);
    $('.hero__forms-signup form').stop().animate({
        width: "0",
        opacity: 0,
      }, 1000);
  });
  $(document).on('click', '.hero__meta-anchor-signup', function() {
    $('.hero__forms-signup form').stop().animate({
        width: "100%",
        opacity: 1,
      }, 1000);
    $('.hero__forms-login form').stop().animate({
        width: "0",
        opacity: 1,
      }, 1000);
  });