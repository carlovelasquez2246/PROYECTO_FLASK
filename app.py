from flask import Flask, render_template, url_for, request, redirect, abort
from forms import SignupForm, PostForm, LoginForm
from flask_login import login_user, current_user, LoginManager, login_required, logout_user
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5433/miniblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager(app)
login_manager.login_view = "login"

db = SQLAlchemy()
db.init_app(app)

with app.app_context():  # ← Activa el contexto de la app
    db.create_all()

#from models import User, Post
import models as m

@app.route("/")
def index():
    posts = m.Post.get_all()
    return render_template("index.html",  posts=posts)

@app.route("/p/<string:slug>/")
def show_post(slug):
    post = m.Post.get_by_slug(slug)
    if post is None:
        abort(404)
    return render_template("post_view.html" , post=post)


@app.route("/admin/post/", methods=['GET' , 'POST'] , defaults={'post_id': None})
@app.route("/admin/post/<int:post_id>" , methods=['GET' , 'POST'])
@login_required
def post_form(post_id):
    form = PostForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        post = m.Post(user_id=current_user.id, title=title , content=content)
        post.save()

        return redirect(url_for("index"))
    return render_template("admin/post_form.html" , form=form)


@app.route("/signup/" , methods=["GET" , "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    error = None #inicializamas error para evitar problemas.

    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data

        #Comprobando que no hay otro usuario con el mismo email.
        user = m.User.get_by_email(email)
        if user is not None:
            error = f'El email {email} ya esta siendo utilizado por otro usuario'
        else:
            #Creando el usuario y lo guardamos.
            user = m.User(name=name, email=email)
            user.set_password(password)
            user.save()
            #Dejamos al usuario logueado.
            login_user(user, remember=True)

            next_page = request.args.get('next' , None)
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
    return render_template("signup_form.html" , form=form, error=error)

@login_manager.user_loader
def load_user(user_id):
    return m.User.get_by_id(user_id)   


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    error = None #inicializamas error para evitar problemas.

    if form.validate_on_submit():
        user = m.User.get_by_email(form.email.data)
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            error = "Usuario o Contraseña incorrecta"

    return render_template('login_form.html', form=form , error=error)

@app.route('/logout')
#@login_required #Evitar que los ususarios no registrados intenten hacer logout.
def logout():
    logout_user()
    return redirect(url_for('index'))



if (__name__ == "__main__"):
    app.run(debug=True)