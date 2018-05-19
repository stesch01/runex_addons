$(document).ready(function () {

    if(! $("input.search-query").length){
        return;
    }
    // To make the words highlighted
    // Solution in a nutshell:
    // * Wrap the input and add a div "highlighted"  next to it
    //   with contenteditable activated to mimic its behaiviour
    // * Hide the input
    // * Add a new div "highlight" with same paddings , margin
    //   and border as the added "highlighted" editable div.
    // * The "highlight" copies values from "highlighted" div
    //   and wraps the text that should be marked in spans
    //   with a background and a transparent color for text.
    // * The text from "highlight" and "highlighted" are superposed
    //   --> "highlight" div have a transparent text color
    //       and "highlighted" div have transparent background.
    var $input = $('input.search-query');
    var width = $input.outerWidth();
    var height = $input.outerHeight();
    var $highlight_wrap = $('<div/>').addClass('highlight_wrap');
    var $highlight = $('<div/>').addClass('highlight');
    var $editable = $('<div/>')
        .addClass('highlighted')
        .attr('contenteditable', 'true')
        .attr('placeholder', $input.attr('placeholder'));
    $input.wrap($highlight_wrap);
    $input.before($highlight);
    $input.before($editable);
    $input.before($editable).hide();
    $highlight_wrap = $input.closest('.highlight_wrap');
    $highlight_wrap.css('width', width);
    $highlight_wrap.css('height', height);
    $highlight_wrap.addClass($input.attr('class'));
    $editable.text($input.val());
    var pattern = /(\S+)/g;
    var _scrolled_search = function(pattern, $input, $editable, $highlight){
        // regexp that match anything exept whitespaces
        var text = $editable.text();
        // replace &nbsp; with spaces to fix non valid submission
        $input.val(text.replace(/\u00a0/g, " "));
        if (!pattern.test(text)) {
            // Make it faster if no regex matched
            $highlight.text(text);
            return;
        }
        var replaceWith = '<span class="marker">$1</span>';
        $highlight.html(text.replace(pattern, replaceWith));
    };
    _scrolled_search(pattern, $input, $editable, $highlight);
    $editable.on('keyup', function(e){
        _scrolled_search(pattern, $input, $editable, $highlight);
    });
    // In case of user enters text before search input is hidden
    $input.on('input', function(){
        $editable.text($input.val());
    });
    //    FIX to show placeholder on div
    $editable.on('focusout keyup', function(){
        var element = $(this);
        if (!element.text().trim().length) {
            element.empty();
        }
    });
    $editable.on('keypress', function(e){
        // if enter is pressed , just submit
        // then cancel the keypress (no newline, we do not need it)
        if(e.keyCode== 13 || e.which== 13) { //if enter key is pressed
            $editable.closest('form').submit();
            // cancel the keypress
            return false;
        }
    });

});
