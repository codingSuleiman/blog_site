from flask import render_template, url_for, flash, redirect, session, request, abort
from proj import app,db
from proj.forms import RegistrationForm, LoginForm, UserForm, UpdateAccountForm, PostForm, SearchForm
from proj.models import User, Post
from proj.test import accessDatabase
from flask_login import login_user,current_user,logout_user, login_required
import secrets
import os
import random

    
@app.route('/')
@app.route('/home', methods=['POST', 'GET'])
def home():
    posts = Post.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('view_user',username=form.username.data))
    return render_template('home.html', posts=posts[::-1], form=form)

@app.route('/userid', methods=['POST', 'GET'])
@login_required  
def userid():
    form = UserForm()
    if not form.userid.data:
        form.userid.data = ''
    return render_template('user.html',form=form, posts=accessDatabase(form.userid.data))
        
@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))     
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if form.password.data == user.password:
                login_user(user, remember=form.remember.data)
                flash('login successful', 'success')
                return redirect(url_for('home'))           
            else:
                flash('Invalid password', 'danger')
        else:
            flash(f'{form.email.data} is not a registered email!', 'danger')     
    return render_template('login.html', form=form)
      
@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
        
    form = RegistrationForm()
    username_ = form.username.data
    email_ = form.email.data
    password_ = form.password.data
    if form.validate_on_submit():
        user = User(username=username_.lower().strip(), email=email_.lower().strip(), password=password_)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {username_}, you can now login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    flash('logout successful!','warning')
    logout_user()
    return redirect(url_for('home'))
    
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile', picture_fn)
    form_picture.save(picture_path)
    return picture_fn 
        
@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
            
        current_user.username = form.username.data.lower()
        current_user.email = form.email.data
        current_user.password = form.password.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))
             
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.password.data = current_user.password
    image_file = url_for('static', filename='profile/'+current_user.image_file)
     
    return render_template('account.html', title='Account',image_file=image_file, form=form)

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
   form = PostForm()
   if form.validate_on_submit():
       post = Post(title=form.title.data, content=form.content.data, author=current_user)
       db.session.add(post)
       db.session.commit()
       flash('Your post has been uploaded!', 'success')
       return redirect(url_for('home'))
   return render_template('create_post.html', title='New Post', form=form, legend='New Post')
   
@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
   post = Post.query.get_or_404(post_id)
   return render_template('post.html', title=post.title, post=post)
    
@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
   post = Post.query.get_or_404(post_id)
   if post.author != current_user:
       abort(403)
   form = PostForm()
   if form.validate_on_submit():
       post.title = form.title.data
       post.content = form.content.data
       db.session.commit()
       flash('Your post has been updated', 'warning')
       return redirect(url_for('home', post_id=post.id))
   elif request.method == 'GET':
       form.title.data = post.title
       form.content.data = post.content
   return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')
   
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'warning')
    return redirect(url_for('home'))

@app.route("/home/<username>", methods=['GET', 'POST'])
@login_required
def view_user(username):
    form = User.query.filter_by(username=username.lower().strip()).first()
    if form:
        return render_template('view_user.html', form=form, legend='Update Post')
    flash(f'{username} doesnt exist!', 'danger')
    return redirect(url_for('home'))