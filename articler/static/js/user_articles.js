get_user_articles();

function get_user_articles(){
    $('.list-group div').empty();
    user_id = window.location.pathname.split('/')[2];
    $.ajax({
        url: "/api/user/" + user_id + "/articles",
        success: function(data){
            append_articles(data);
        }.bind(this),
        contentType: "application/json"
    });
}

function append_articles(data){
    var articles = data["articles"];
    username = articles[0]["username"]
    document.getElementById('heading').innerHTML = username + "'s articles"
    for(i in articles){
        article_name = articles[i]["name"];
        article_id = articles[i]["id"] 
        console.debug(article_name)
       
        $('.list-group').append('<a href="/article/' + article_id + '" class="list-group-item">' + article_name + '</a>');

    }
}