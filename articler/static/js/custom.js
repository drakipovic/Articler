var user = null;
get_user();

function callback(data){
    if(data["username"]) user = data["username"];

    if(user == null){
        $('form[name="loginForm"]').show();
    }
    else{
        document.getElementById('user').innerHTML = "Hello " + user;
    }
}

function get_user(){
    $.ajax({
        url: "/api/current_user",
        success: function(data){
            callback(data);
        }.bind(this),
        contentType: "application/json"
    });
};

function loginUser(){
    
    var username = document.forms['loginForm'].elements['username'].value;
    var password = document.forms['loginForm'].elements['password'].value;
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