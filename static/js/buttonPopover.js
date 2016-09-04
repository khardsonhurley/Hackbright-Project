"use strict";

    window.onload = function() {
        checkSpans();
    }

    function checkSpans(){
        $.get('/checkspans', function(result){
            console.log(result.result[23]);
            for (var i = 0; i<result.result.length; i++){
                console.log('make span')
                makeSpans(result.result[i]);
                console.log('im back')
            }
            }); 
    }
      

function makeSpans(coordinates){
    console.log(coordinates)
    var start = coordinates['start'];
    var end = coordinates['end'];

    var anchorNode = $('.my-node');

    var commentData = [];
    commentData.push(start);
    commentData.push(end);

    var beforeText = anchorNode.text().slice(0,start);
    console.log(beforeText);
    var selection = anchorNode.text().slice(start,end);
    console.log(selection);
    var afterText = anchorNode.text().slice(end);
    console.log(afterText);

    var firstSpan = $("<span>");
    firstSpan.append(beforeText);
    var secondSpan = $("<span>");
    secondSpan.attr("class","commentedText")
    var innerSecondSpan = $("<a>")
    innerSecondSpan.attr("class", "commentLink");
    innerSecondSpan.attr("id", commentData)
    innerSecondSpan.append(selection);
    secondSpan.html(innerSecondSpan);
    var thirdSpan = $("<span>");
    thirdSpan.append(afterText);

    var kidList = [firstSpan, secondSpan, thirdSpan];

    anchorNode.replaceWith(kidList);


}

$(document).ready(function() {

    //global variable 
    var template = `<button class="btn btn-default translate-button">
            <span class='glyphicon glyphicon-transfer' aria-hidden='true'</span></button>` 
            + " " + 
            `<div class="btn btn-default comment-button">
            <span class='glyphicon glyphicon-comment' aria-hidden='true'</span></div>`+ " "+
            `<div class="btn btn-default twilio-button">
            <span class='glyphicon glyphicon-send' aria-hidden='true'</span></div>`;

///////////////////////////////////////////////////////////////////////////////
///////////////////////////////    FUNCTIONS    ///////////////////////////////
///////////////////////////////////////////////////////////////////////////////
        
//////////////////////////////    TRANSLATION    //////////////////////////////        

        function getText(){
            //on the window, this gets the translated text from the window. 
            var selection = window.getSelection();  

            var text = selection.toString();

            return {
                    'selection': selection,
                    'text':text
            }
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
            $.post("/translate", translationInput, function(result){
                showTranslation(result);
                addToVocabList(translationInput["phrase"], result);
            });
        }

//////////////////////////////    POPOVERS    //////////////////////////////

        function createPopover(content, selection){
            // get the position of the selection. This instantiates an object
            //of the class ClientRect that has all information about the position
            //of the rectangle placed around the selection. 
            var position = selection.getRangeAt(0).getBoundingClientRect();
            console.log(position);
            var thePopover = $('<span>');
            var length = selection.toString().length

            //sets the tooltip data. 
            thePopover.data({'content': content , 'toggle':'popover', 'placement': 'top', 'html': true});

            //add the span to the html. 
            $('body').append(thePopover);

            //puts the popover right above the position of the selection. 
            thePopover.offset({top: (position.top) + $(window).scrollTop(), left: position.left + (7*length)/2});

            //initializes the popover, without this it will not show. 
            thePopover.popover('show');

        }

        function firstPopover(){
            // returns an object with {'text':text, 'selection':selection}
            var textSelection= getText();
            // gets the selection from the object. 
            var selection = textSelection['selection'];
            var text = textSelection['text'];
            //Only want to create a popover if there is text in the selection.
            if (text){
                //create the popover that has the buttons(template - global var) in it. 
                createPopover(template, selection);
            }
        }
        
        function showTranslation(translation){
            //had to make this in html because the tooltip's html value was set
            //to true so it now only takes html. Is there a better way to do this? 
            var htmlTranslation = '<p>'+translation+'</p>';
            //Changes the html to display the translation. Also moves the popover
            //over slightly. Why is this? 
            $('.popover-content').html(htmlTranslation);

        }

//////////////////////////////    COMMENT WINDOW    //////////////////////////////

        function getCommmentData(){
            var selection = window.getSelection();
            var anchorNode = selection.anchorNode;
            var startOfSelection = selection.getRangeAt(0).startOffset;
            var endOfSelection = selection.getRangeAt(0).endOffset;

            var commentData = {
                'start':startOfSelection,
                'end':endOfSelection,
            }

            checkForComments(commentData);
        }

        function checkForComments(commentData){
            $.post('/checkcomments', commentData, function(result){
                displayComments(result);
                showCommentWindow();
            });
        }

        function addCommentFormatting(){

            var selection = window.getSelection();
            var anchorNode = selection.anchorNode;
            var startOfSelection = selection.getRangeAt(0).startOffset;
            var endOfSelection = selection.getRangeAt(0).endOffset;
            var commentData = [];
            commentData.push(startOfSelection);
            commentData.push(endOfSelection);

            var jQAnchorNode = $(anchorNode).parent();

            var beforeText = jQAnchorNode.text().slice(0,startOfSelection);
            var afterText = jQAnchorNode.text().slice(endOfSelection);

            var firstSpan = $("<span>");
            firstSpan.append(beforeText);
            var secondSpan = $("<span>");
            secondSpan.attr("class","commentedText")
            var innerSecondSpan = $("<a>")
            innerSecondSpan.attr("class", "commentLink");
            innerSecondSpan.attr("id", commentData)
            innerSecondSpan.append(selection.toString());
            secondSpan.html(innerSecondSpan);
            var thirdSpan = $("<span>");
            thirdSpan.append(afterText);
            var kidList = [firstSpan, secondSpan, thirdSpan];


            jQAnchorNode.replaceWith(kidList);
        }

        function showCommentWindow(){
            //Get the User's selection
            var textSelection = getText();
            //get the selection object
            var selection = textSelection['selection'];
            //find the position using the selection object
            var position = selection.getRangeAt(0).getBoundingClientRect();
            
            var text = textSelection['text'];
            
            //This just moves the comment-window that already exists in the DOM
            //to the position on the same line as the selection. 
            $('#comment-window').offset({top:(position.top) + $(window).scrollTop()});
            $('.commentReference').replaceWith('"'+ text+ '"');
            $('.comment-sidebar').css('visibility', 'visible');

        }

        function addComment(evt){
            evt.preventDefault(); 
            //Gets the text from the input field. 
            var inputText= $('input').val();
            //removes input value
            $('input').val("");

            var commentInput = {
                "comment": inputText
            }

            //sends an Ajax request to server where the comment should be stored
            //in the database. The server returns all comments with that comment_id
            $.post('/comments', commentInput, function(result){
                displayComments(result);
            });
        }

        
        function displayComments(result){

            var commentObject = result.commentData

            for(var i=0; i<commentObject.length; i++){
                var comment = commentObject[i]['userComment'];
                var image = commentObject[i]['userImage'];
                var userName = commentObject[i]['userName'];
                var htmlComment = formatComment(image, userName, comment);
                $('.commentTemplate').append(htmlComment);

            }
        }

        function formatComment(imageUrl, userName, comment){

                var htmlComment= `<li class="">
                    <div class="commenterImage">
                    <img class= "userImage" src=` + imageUrl +
                    `/>
                    </div>
                <div class="commentText">
                    <h6 class='userName'>` + userName + `</h6>
                    <p class="commentBody">` + comment + `</p>
                    <span class="date sub-text">
                    </span>
                </div>
                </li>`

                return htmlComment;

        }


        function addToVocabList(text, translatedText){
            // add text and translatedText to the html panel vocab list area. 
            $('.panel-body').append(text + ': ' + translatedText+".");
        }
            


///////////////////////////////////////////////////////////////////////////////
/////////////////////////////    EVT LISTENERS    /////////////////////////////
///////////////////////////////////////////////////////////////////////////////

        $('#article-text').mouseup(function(event){
            firstPopover();
            event.stopPropagation(); 
        });


        $(document).on('click', '.translate-button', function(){
            var textSelection = getText();
            var text= textSelection['text'];
            // This function calls the showTranslation function. 
            var translatedText = translateText(text);
            console.log('in the translate click');
        });

        $('.article-body').on('mousedown', function(){
            if ($('.popover')){
                $('.popover').remove();
                }
            if ($('#comment-window')){
                $('.comment-sidebar').css('visibility', 'hidden');
                $('.commentTemplate').html("");
            }
        });

        $(document).on('click', '.comment-button', function(){
            $('.popover').remove();
            getCommmentData();

        });

        $(document).on('click', '#add-comment-button', function(evt){
            addComment(evt);
        });

        $(document).on('mousedown', '.form-control', addCommentFormatting);


        $(document).on('click', '.commentLink', function(event){
            var coordinatesString = event.target.id;
            var coordinatesArray = coordinatesString.split(',')
            var start = coordinatesArray[0];
            var end = coordinatesArray[1];


            // $('.commentReference').html(event.target.text);

            var commentData = {
                'start':start,
                'end':end,
            }

            checkForComments(commentData);
            $('.commentReference').html(event.target.text, 5000);

        });

        //Event listener that listens for user to his the 'X' button in the corner
        //of the comment window. 
        $(document).on('click', '.close', function(){
             $('.comment-sidebar').css('visibility', 'hidden');
             $('.commentTemplate').html("");
        });


        //PSEUDO-CODE: User enters a comment into the comment window and clicks
        //"add." This should make a ajax post request to the '/comment' route. 
        //Adding the comment to the DB and now displaying it as one of the comments.

        //PSEUDO-CODE: Another event listener for when the user clicks off the 
        //comment window. Comment window collapses into a icon that is located
        //at the same top position as the selection. Also would like to make 
        //the selection highlighted a light grey so other users can see that it 
        //has a comment on it. 

});

 
