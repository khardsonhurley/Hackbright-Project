"use strict";

$(document).ready(function() {

///////////////////////////////////////////////////////////////////////////////
/////////////////////////////    NEW FUNCTIONS    /////////////////////////////
///////////////////////////////////////////////////////////////////////////////

        function getText(){
            //on the window, this gets the translated text from the window. 
            var selection = window.getSelection();  

            var text = selection.toString();

            return text; 
        }

        function translateText(text){

            // Request.form.get requires a dictionary to read it.
            var translationInput = {
                "phrase": text
            }
            //send a post request to the translate route, remember the middle 
            //value is the data you are sending to the route. This must be in 
            //dictionary format for request.form.get(). The result of that
            //is passed into the an anonymous function (because we wanted to
            // pass in two things: translated result and the location of it.)
            var result = $.post("/translate", translationInput);

            return result;
        }

        function popoverButtons(){
            //Buttons that will be placed into the tooltip
            var template = '<div class="btn btn-default" id="translate-button">Translate</div>' +
                        '<div class="btn btn-default">#I</div>' +
                        '<div class="btn btn-default">#K</div>' + 
                        '<div class="btn btn-default">#R</div>';

            return template;

        }

        function createPopover(content){

            var selection = window.getSelection();
            // get the position of the selection. This instantiates an object
            //of the class ClientRect that has all information about the position
            //of the rectangle placed around the selection. 
            var position = selection.getRangeAt(0).getBoundingClientRect();
            var thePopover = $('<span>');

            //sets the tooltip data. 
            thePopover.data({'content': content , 'toggle':'popover', 'placement': "top", "html": true});

            //add the span to the html. 
            $('body').append(thePopover);

            //puts the popover right above the position of the selection. 
            thePopover.offset({top: (position.top) + $(window).scrollTop(), left: position.left + (7*length)/2});

            //initializes the popover, without this it will not show. 
            thePopover.popover('show');

        }

        function replacePopoverContentWithTranslation(){
            //need even handler on the #translation-button element. 
            //clear 'content' in popover and replace with the translate on 
        }

        function addToVocabList(text, translatedText){
            // add the text and the translated text to the DB and to the html
            //panel vocab list area. 
        }

        function main(){
            var text= getText();
            var translation = translateText(text);
            addToVocabList(text,translation);
            




        }

///////////////////////////////////////////////////////////////////////////////
/////////////////////////////    EVT LISTENERS    /////////////////////////////
///////////////////////////////////////////////////////////////////////////////

        //removes any popovers that exist in the html. 
        $('body').mousedown(function(){
            $('.popover').remove();
        });    

        $('#article-body').mouseup(function(event){
                main();
                event.stopPropagation();
        });

        $('#translate-button').click(getSelectedText);
 
///////////////////////////////////////////////////////////////////////////////
/////////////////////////////    OLD FUNCTIONS    /////////////////////////////
///////////////////////////////////////////////////////////////////////////////

        function getSelectedText(){
            //on the window, this gets the translated text from the window. 
            var selection = window.getSelection();  

            //this changes the selection to a string.               
            var stringSelection = selection.toString();

            //get length of the selection. 
            var length = stringSelection.length;

            // Request.form.get requires a dictionary to read it. 
            var translationInput = {
                "phrase": stringSelection
            }

            $('.panel-body').append(stringSelection + ": ")

            //send a post request to the translate route, remember the middle 
            //value is the data you are sending to the route. This must be in 
            //dictionary format for request.form.get(). The result of that
            //is passed into the an anonymous function (because we wanted to
            // pass in two things: translated result and the location of it.)
            $.post("/translate", translationInput, function(result){
                createTooltip(result, selection, length);
                });
            } 
        
       

        function createTooltip(result, selection, length){


            // get the position of the selection. This instantiates an object
            //of the class ClientRect that has all information about the position
            //of the rectangle placed around the selection. 
            var position = selection.getRangeAt(0).getBoundingClientRect();
            // var position = selection.position();
            console.log(position);
            //create placeholder span. 
            var tooltip = $('<span>');
            //sets the tooltip data. 
            tooltip.data({'content': result, 'toggle':'popover', 'placement': "top", "html": true});
            // tooltip.data({'content': result, 'placement': "top"});
            //add the span to the html. 
            $('body').append(tooltip);

            //puts the tool tip right above the position of the selection. This 
            //does not work for small screens. Can you do a relative position 
            //based on screen size?
            tooltip.offset({top: (position.top) + $(window).scrollTop(), left: position.left + (7*length)/2});
            // tooltip.position({top: position.top, left: position.left});


            // tooltip.offset({top:position.top, left: position.left});
            //initializes the popover over, without is this it will not show. 
            tooltip.popover('show');
            // console.log(tooltip.top);
            $('.panel-body').append(result + '.')

           
        }

///////////////////////////////////////////////////////////////////////////////
///////////////////////////    OLD EVT LISTENERS    ///////////////////////////
///////////////////////////////////////////////////////////////////////////////

        //checks the body of html for an element of the class 'popover' and 
        //removes it on the event mousedown. 
        // $('body').mousedown(function(){
        //     $('.popover').remove();
        //     });         
        //listens for the mouseup event on the element of class 'article.' When
        //this happens, run the function getSelectedText. 
        // $('#article-body').mouseup(function(event){
        //     getSelectedText();
        //     event.stopPropagation();
        // });
        // $('body').mouseup(readyTooltip);
        // $('#translate-button').click(getSelectedText)

        //
        //createButtonTooltip 
        //showTranslationTooltip
        //addTextVocabList



});