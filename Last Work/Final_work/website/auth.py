# Importing necessary libraries to work on
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User,WasteCollection, RecyclingEffort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .form import ScheduleCollectionForm, TrackRecyclingForm



# Creating a Blueprint object 'auth'
auth = Blueprint("auth", __name__)

# Route for the login page
@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Route for sign up
@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
# Conditioning
        if email_exists: 
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password1) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)

@auth.route("/logout") 
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

# Route to schedule a waste collection
@auth.route('/schedule', methods=['GET', 'POST'])
@login_required
def schedule_collection():
    form = ScheduleCollectionForm()
    if form.validate_on_submit():
        collection = WasteCollection(
            user_id=current_user.id,
            address=form.address.data,
            collection_date=form.collection_date.data,
            collection_time=form.collection_time.data,
            status='scheduled'
        )
        db.session.add(collection)
        db.session.commit()
        flash('Waste collection scheduled successfully!')
        return redirect(url_for('auth.schedule_collection'))
    return render_template('schedule.html', form=form)

# Route to track recycling efforts
@auth.route('/recycle', methods=['GET', 'POST'])
@login_required
def track_recycling():
    form = TrackRecyclingForm()
    if form.validate_on_submit():
        effort = RecyclingEffort(
            user_id=current_user.id,
            date=form.date.data,
            materials=form.materials.data,
            status=form.status.data)
        
        db.session.add(effort)
        db.session.commit()
        flash('Recycling effort tracked successfully!')
        return redirect(url_for('auth.track_recycling'))
    return render_template('recycle.html', form=form)
# Route for the admin dashboard
@auth.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('index'))
    return render_template('admin.html')






