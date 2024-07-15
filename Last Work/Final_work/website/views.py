# Importing necessary models and forms from the current directory
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask import Flask  # Import Flask module

from .models import User, WasteCollection, RecyclingEffort, db
from .form import ScheduleCollectionForm, TrackRecyclingForm
# Creating a Blueprint object 'views'
views = Blueprint("views", __name__)


# @views.route('/check-data')
# def check_data():
#     users = User.query.all()
#     collections = WasteCollection.query.all()
#     return jsonify({
#         'users': [{'username': user.username, 'email': user.email, 'role': user.role} for user in users],
#         'collections': [{'address': c.address, 'date': c.collection_date, 'time': c.collection_time, 'status': c.status} for c in collections]
#     })


# Route for the home page
@views.route("/")
@views.route("/home")
@login_required # This decorator ensures that the user is logged in before accessing the home page
def home():
    schedule = ScheduleCollectionForm()
    track = TrackRecyclingForm()
    return render_template("home.html", user=current_user, schedule=schedule, track=track)

@views.route("/")
@views.route("/schedule")
@login_required
def schedule():
    return render_template("schedule.html", user=current_user, form=ScheduleCollectionForm()) # Render the schedule.html template with the current user and the ScheduleCollectionForm

@views.route("/")
@views.route("/recycle")
@login_required
def recycle():
    return render_template("recycle.html", user=current_user, form=TrackRecyclingForm()) # Render the recycle.html template with the current user and the TrackRecyclingForm

@views.route("/")
@views.route("/admin")
@login_required
def admin():
    return render_template("admin.html", user=current_user)

# Helper function to check if the current user is an admin
def admin_required(func):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.role != 'admin':
            flash('Access denied. Admins only.')
            return redirect(url_for('views.index'))  # or appropriate route
        return func(*args, **kwargs)
    return wrapper

@views.route('/system', methods=['GET'])
def systm_page():
    return render_template('system_performance.html', user=current_user) # Render the system_performance.html template with the current user

@views.route('/user_mgt', methods=['GET'])
def user_mgt_page():
    users = User.query.all() 
    return render_template('User_Mgt.html', user=current_user)

@views.route('/admin', methods=['GET'])
@admin_required
def admin_dashboard():
    users = User.query.all()
    collections = WasteCollection.query.all()
    return render_template('admin.html', users=users, collections=collections) # Render the admin.html template with the list of users and collections


# Route for the page
@views.route('/admin', methods=['GET'])
def admin_dashboard():
    total_users = User.query.count()
    print("Total users:", total_users)

    total_schedules = WasteCollection.query.count()
    print("Total schedules:", total_schedules)

    total_recycling = db.session.query(db.func.sum(RecyclingEffort.amount)).scalar() or 0
    print("Total recycling:", total_recycling)

    users = User.query.all()
    print("Users:", users)

    collections = WasteCollection.query.all()
    print("Collections:", collections)
# render the admin.html template with the total number of users, schedules, recycling efforts, and the list of users and collections
    return render_template('admin.html', 
                           total_users=total_users,
                           total_schedules=total_schedules,
                           total_recycling=total_recycling,
                           users=users,
                           collections=collections)
# Route for the about page 
def create_app():
    app = Flask(__name__)
   
    app.register_blueprint(views)
    return app # Return the apps instance
