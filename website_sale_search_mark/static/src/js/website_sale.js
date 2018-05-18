$(document).ready(function () {

    if(! $("input.search-query").length){
        return;
    }
    function isCharacterKeyPress(evt) {
        if (typeof evt.which == "undefined") {
            // This is IE, which only fires keypress events for printable keys
            return true;
        } else if (typeof evt.which == "number" && evt.which > 0) {
            // In other browsers except old versions of WebKit, evt.which is
            // only greater than zero if the keypress is a printable key.
            // We need to filter out backspace and ctrl/alt/meta key combinations
            return !evt.ctrlKey && !evt.metaKey && !evt.altKey && evt.which != 8;
        }
        return false;
    }
    function CharOffset(el) {
        var caretOffset = 0;
        if (typeof window.getSelection != "undefined") {
            var range = window.getSelection().getRangeAt(0);
            var preCaretRange = range.cloneRange();
            preCaretRange.selectNodeContents(el);
            preCaretRange.setEnd(range.endContainer, range.endOffset);
            caretOffset = preCaretRange.toString().length;
        } else if (typeof document.selection != "undefined" && document.selection.type != "Control") {
            var textRange = document.selection.createRange();
            var preCaretTextRange = document.body.createTextRange();
            preCaretTextRange.moveToelText(el);
            preCaretTextRange.setEndPoint("EndToEnd", textRange);
            caretOffset = preCaretTextRange.text.length;
        }
        return caretOffset;
    }
    function setCursor(node,pos){
        if(!node){
            return false;
        } else if(document.createRange) {
          range = document.createRange();
          range.selectNodeContents(node);
          range.setStart(node, pos);
          range.setEnd(node, pos);
          selection = window.getSelection();
          selection.removeAllRanges();
          selection.addRange(range);
        } else if(node.createTextRange) {
            var textRange = node.createTextRange();
            textRange.collapse(true);
            textRange.moveEnd(pos);
            textRange.moveStart(pos);
            textRange.select();
            return true;
        } else if(node.setSelectionRange) {
            node.setSelectionRange(pos,pos);
            return true;
        }
        return false;
    }
    var $search = $('input.search-query');
    var search_width = $search[0].getBoundingClientRect().width;
    $editable = $('<div/>')
        .attr('contenteditable', 'true')
        .attr('placeholder', $search.attr('placeholder'))
        .addClass($search.attr('class'))
        .addClass('highlighted single-line')
        .css({
            'width':search_width,
        })
        .text($search.val());
    $search.after($editable).hide();
    function _update_marks($search, $editable, noRange){
        var editable = $editable.get(0);
        $search.val($editable.text());
        var divText = $editable.text().split('');
        var pattern = /(\d|\w)/;
        var replaceWith = '<span class="highlight">$1</span>';
        var highlighted = divText.map(function(char) {
          if (pattern.test(char))
              return $(char.replace(pattern, replaceWith));
          else
              return document.createTextNode(char);
        });
        if (noRange){
            $editable.empty().append(highlighted);
            return;
        }
        var Position = CharOffset(editable);
        $editable.empty().append(highlighted);
        setCursor(editable, Position);
    }
    _update_marks($search, $editable, true);
    $editable.on('keyup', function(e){
        // space (keycode 32) fix for firefox
        if(navigator.userAgent.indexOf("Firefox") != -1){
            if (e.which == 32) return;
        }
        // Mimmic input enter click: submit on enter clicked
        if (e.which == 13) $editable.closest('form').submit();
        _update_marks($search,$editable);
    });
    // copy text in case user typped in searchbox before it got hidden
    $search.on('keyup', function(e){
        $editable.text($search.val());
    });
//    FIX to show placeholder on div
    $editable.on('focusout keyup', function(){
        var element = $(this);
        if (!element.text().trim().length) {
            element.empty();
        }
    });
});
