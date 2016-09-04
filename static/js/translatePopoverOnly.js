"use strict";

$(document).ready(function() {

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
        $('body').mousedown(function(){
            $('.popover').remove();
            });         
        //listens for the mouseup event on the element of class 'article.' When
        //this happens, run the function getSelectedText. 
        $('#article-body').mouseup(function(event){
            getSelectedText();
            event.stopPropagation();
        });





});