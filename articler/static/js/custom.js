var user = null;
var id = null;


get_current_user();

function callback(data){
    if(data["username"]){
        user = data["username"];
        id = data["id"];
        pass = data["password"];
    } 

    if(user == null){
        $('form[name="loginForm"]').show();
    }
    else{
        document.getElementById('name').innerHTML = "Hello " + user;
        $("#my_articles").attr('href', '/user/' + id + "/articles");
        $("#user").show();
    }
}


function get_current_user(){
    return $.ajax({
        url: "/api/current_user",
        success: function(data){
            callback(data);
        }.bind(this),
        contentType: "application/json"
    });
};

function loginUser(){
    var username = document.forms['loginForm'].elements['inputUsername'].value;
    var password = document.forms['loginForm'].elements['inputPassword'].value;
    data = {"username": username, "password": password};
    $.ajax({
        type: "POST",
        url: "/api/login",
        data: JSON.stringify(data),
        success: function(data){
            if(data["success"] == true){
                $('form[name="loginForm"]').hide();
            }
        }.bind(this),
        dataType: "json",
        contentType: "application/json"
    });
}

function save_password(password){
    pass = password;
}


function saveArticle(){
    var name = $('#article_name').val();
    var text = $('#article_text').val();

    data = {"name": name, "text": text, "user_id": id};
    $.ajax({
        type: "POST",
        url: "/api/articles",
        data: JSON.stringify(data),
        username: user,
        password: pass,
        success: function(data){
            $("#myModal").modal('hide');
            get_articles();
        }.bind(this),
        dataType: "json",
        contentType: "application/json"
    });
}
