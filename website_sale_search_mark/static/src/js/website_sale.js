$(document).ready(function () {

    if(! $("input.search-query").length){
        return;
    }
    var $input = $('input.search-query');
    $input.tokenfield({
        'delimiter': ' ',
    });
    var $tokenfield = $input.data('bs.tokenfield');
    var $input_token = $tokenfield.$input;
    var $input_wrapper = $tokenfield.$wrapper;
    $input_token.on('keydown', function(e){
        // if enter is pressed , submit
        if(e.keyCode == 13 || e.which == 13) { //if enter key is pressed
            setTimeout(function(){
                $input_token.closest('form').submit();
            }, 0);
        }
    });
    var $submitBtn = $input_token.closest('form').find('a.a-submit');
    $submitBtn.off('click');
    $submitBtn.on('click', function(e){
        e.preventDefault();
        $tokenfield.createTokensFromInput(e, $input_token.data('edit'));
        setTimeout(function(){
            $input_token.closest('form').submit();
        }, 0);
    });
    // Fix force focus on input after delete tocken
    $input_token.on('keyup', function(e){
        if(e.keyCode == 8 || e.which == 8) {
            $tokenfield.focus(e);
            $tokenfield.remove(e);
            $input_token.focus();
            $tokenfield.focus(e);
        }
    });


});
