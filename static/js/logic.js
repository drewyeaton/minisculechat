$(document).ready(function() {
    var uid = Math.round(Math.random() * 9999);
    var d = new Date();
    s = d.getTime();

    chat_loop(s, uid);
    
    $("#chat_form").submit(function() {
        author = $("#author").val();
        message = $("#message").val();
        
        if(author == "" || message == "") {
            alert("Please enter a name and a message.");
            return false;   
        }
        
        msg = {'message': message, 'author': author};
        msg_element = render_message(msg, true);
        
        $("#message").val("");        
        $.post("/message/", {author: author, message: message, uid: uid}, mark_as_sent(msg_element));

        return false;
    });
});

var mark_as_sent = function(msg_element) {
    return function(data, status) {
        $(msg_element).removeClass("is_sending");
    };
};

function chat_loop(s, uid){
    $.get("/message/?s=" + s + "&uid=" + uid, function(data) {      
        if(!data) {
            return false;
        } else {
            for(i in data) {
                render_message(data[i], false);
                s = data[i].timestamp;
            }
            chat_loop(s, uid); 
        }
    });
}

function render_message(message, is_sending) {
    message = $("#message_tpl").jqote({message: message.message, author: message.author});
    
    if(is_sending)
        $(message).addClass("is_sending");
    
    if(!is_sending)
        $(message).addClass("from_friend");
    
    message.appendTo($("#chat")).hide().fadeIn("fast");
    $("#chat").animate({ scrollTop: $("#chat").attr("scrollHeight") }, 750);
    
    return message;
}