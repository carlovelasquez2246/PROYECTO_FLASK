from flask import Flask, render_template, url_for

app = Flask(__name__)

'''@app.route("/")
def holla():
    return "!hola Mundo¡"'''

posts = []

@app.route("/")
def index():
    '''return "{} posts".format(len(posts))'''
    return render_template("index.html" , nun_posts=len(posts))

@app.route("/p/<string:slug>/")
def show_post(slug):
    '''return "Mostrando el post {}".format(slug)'''
    return render_template("post_view.html" , slug_title=slug)

@app.route("/admin/post/")
@app.route("/admin/post/<int:post_id>")
def post_form(post_id=None):
    '''return "post_form {}".format(post_id)'''
    return render_template("admin/post_form.html" , post_id= post_id)

'''print(url_for("index"))'''
'''print(url_for("show_post", slug="leccion-1", preview=True))
'''
@app.route("/suma/<int:s1>/<int:s2>" , methods=["GET"])
def suma(s1 , s2):
    return (s1 + s2)

if (__name__ == "__main__"):
    app.run(debug=True)