from flask import Blueprint, request, render_template
from app.models import Entry, User
from sqlalchemy import or_
from app import app

main = Blueprint('main', __name__)


@main.route("/")
def home():
    total_entries =  Entry.query.count()
    users = User.query.all()
    page = request.args.get('page', 1, type=int)
    entries = Entry.query.filter(or_(Entry.covid_status == 2, Entry.covid_status == 1)).order_by(Entry.date_posted.desc()).paginate(page=page, per_page=app.config['PAGINATION_PER_PAGE'])
    return render_template("home.html", title="Home", entries=entries, total_entries=total_entries, users=users)

@main.route("/api/locations")
def get_locations():
    entries = Entry.query.filter(or_(Entry.covid_status == 2, Entry.covid_status == 1)).all()
    locations = {}
    for entry in entries:
        location_dict = {}
        location_dict['center'] = {}
        location_dict['center']['lat'] = float(entry.last_visited_location_lat)
        location_dict['center']['lng'] = float(entry.last_visited_location_long)
        location_dict['color'] = "red" if entry.covid_status == 2 else "yellow"
        locations[str(entry.id)] = location_dict

    return locations

@main.route("/api/locations/user/<int:user_id>")
def get_locations_by_user(user_id):
    user = User.query.get(user_id)

    if user_id == 0 or not user:
        entries = Entry.query.filter(or_(Entry.covid_status == 2, Entry.covid_status == 1)).all()
    else:
        entries = Entry.query.filter(or_(Entry.covid_status == 2, Entry.covid_status == 1)).filter_by(user_id=user.id)
        
    locations = {}
    for entry in entries:
        location_dict = {}
        location_dict['center'] = {}
        location_dict['center']['lat'] = float(entry.last_visited_location_lat)
        location_dict['center']['lng'] = float(entry.last_visited_location_long)
        location_dict['color'] = "red" if entry.covid_status == 2 else "yellow"
        locations[str(entry.id)] = location_dict

    return locations

@main.route("/api/user/<int:user_id>")
def get_entries_by_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"message" : "not found"}
    entries = Entry.query.filter(or_(Entry.covid_status == 2, Entry.covid_status == 1)).order_by(Entry.date_posted.desc()).filter_by(user_id=user.id)

    output = {} 
    entries_list = []
    for entry in entries:
        result_dict = {}
        result_dict['id'] = entry.id
        result_dict['full_name'] = entry.full_name
        result_dict['age'] = entry.age
        result_dict['visited_date_time'] = entry.visited_date_time
        result_dict['last_visited_location'] = entry.last_visited_location
        result_dict['covid_status'] = entry.covid_status
        entries_list.append(result_dict)
    output['entries'] = entries_list

    return output

@main.route('/map')
def map_demo():
    return render_template('mapdemo.html')