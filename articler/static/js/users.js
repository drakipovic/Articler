get_users();


function get_users(){
    $('.list-group div').empty();
    $.ajax({
        url: "/api/users",
        success: function(data){
            append_users(data);
        }.bind(this),
        contentType: "application/json"
    });
}

function append_users(data){
    var users = data["users"];

    for(i in users){
        username = users[i]["username"];
        user_id = users[i]["id"];

        $('.list-group').append('<a href="/user/' + user_id + '/articles" class="list-group-item">' + username + '</a>');

    }
}