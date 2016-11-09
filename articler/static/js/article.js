get_article();


function get_article(){
    var article_id = window.location.pathname.split('/')[2];
    $.ajax({
        url: "/api/article/" + article_id,
        success: function(data){
            $.when(get_current_user()).done(function(a1){
                append_article(data);
            });
        }.bind(this),
        contentType: "application/json"
    });
}

function append_article(data){
    var article = data["article"];

    document.getElementById('article_name').innerHTML = article["name"];
    document.getElementById('text').innerHTML = article["text"];
    document.getElementById('author').innerHTML = "Written by: " + article["username"];
    document.getElementById('date').innerHTML = article["date"];

    if(id == article["user_id"]){
        $("#buttons").show();
    }

    $("#articleName").val(article["name"]);
    $("#article_text").val(article["text"]);

}

function deleteArticle(){
    var article_id = window.location.pathname.split('/')[2];
    $.ajax({
        type: "DELETE",
        url: "/api/article/" + article_id,
        success: function(data){
            window.location.replace('/');
        }.bind(this),
        dataType: "json",
        contentType: "application/json"
    });
}

function editArticle(){
    var name = $('#articleName').val();
    var text = $('#article_text').val();
    var article_id = window.location.pathname.split('/')[2];

    data = {"name": name, "text": text};
    $.ajax({
        type: "PUT",
        url: "/api/article/" + article_id,
        data: JSON.stringify(data),
        success: function(data){
            $("#editModal").modal('hide');
            article = data["article"];
            console.debug(article);
            document.getElementById('article_name').innerHTML = article["name"];
            document.getElementById('text').innerHTML = article["text"];
        }.bind(this),
        dataType: "json",
        contentType: "application/json"
    });
}