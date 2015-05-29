function GetURLParameter( sParam )
{
    var sPageURL = window.location.search.substring( 1 );
    var sURLVariables = sPageURL.split( '&' );
    for ( var i = 0; i < sURLVariables.length; i++ )
    {
        var sParameterName = sURLVariables[i].split( '=' );
        if ( sParameterName[0] == sParam )
        {
            return sParameterName[1];
        }
    }
}


$( document ).on( 'click', '[data-page]', function( ev ) {
  ev.preventDefault();

  var el = $( this );
  var loader = $('#load-more .load-more__loader');
  var end = $('#load-more .load-more__end');
  var page = parseInt( el.attr( 'data-page' ) );
  var next_page = page + 1;
  var num_pages = parseInt( el.attr( 'data-num-pages' ) );
  var url = window.location.href;
  var page = el.attr( 'data-page' );

  el.hide();
  loader.show();

  if (page < num_pages) {
    if ( url.indexOf( 'page=' ) >= 0 ) {
      value = GetURLParameter( 'page' );
      url = url.replace( 'page=' + value, 'page=' + page );
    } else if ( url.indexOf( "/?" ) >= 0 ){
      url = url + "&page=" + page;
    } else {
      url = url + "?page=" + page;
    }

    console.log(url)
    $.ajax( {
        url     : url,
        type    : 'get',
        cache   : false,
        success : function( data ){
          $( '.infinite-scroll__content' ).append( data );
        },
        error   : function( data ){
        },
        complete: function( data ){
          el.attr( 'data-page', next_page  );
          el.show();
          loader.hide();
        }
      } );
  } else {
    el.hide();
    loader.hide();
    end.show();
  }
} );
