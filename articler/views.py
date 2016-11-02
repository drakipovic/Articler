from main import app


@app.route('/articles', methods=['GET', 'POST'])
def articles():
    return 'List of articles'

