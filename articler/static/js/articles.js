get_articles();


function get_articles(){
    $('.row div').empty();
    $.ajax({
        url: "/api/articles",
        success: function(data){
            append_articles(data);
        }.bind(this),
        contentType: "application/json"
    });
}

function append_articles(data){
    console.debug(data)
    var articles = data["articles"];
    for(i in articles){
        var name = articles[i]["name"];
        var text = articles[i]["text"];
        var username = articles[i]["username"];
        var timestamp = articles[i]["date"];
        var article_id = articles[i]["id"];

        $(".row").append('<div class="col-md-6 col-lg-6"> \
                            <div class="card"> \
                                <a href=/article/' + article_id + '><h2 class="card-header card-primary white-text">' + name + '</h2></a> \
                                    <div class="card-block"> \
                                        <p class="card-text">' + text + '</p> \
                                    </div> \
                                <div class="card-footer text-muted card-info white-text"> \
                                    <p>' + 'Written by ' + username + ' on ' + timestamp + '</p> \
                                </div> \
                            </div> \
                          </div>' 
                        );
    }
}


