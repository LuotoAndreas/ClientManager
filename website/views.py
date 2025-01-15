from flask import Blueprint, flash, render_template, request, url_for, jsonify
from flask_login import login_required, current_user
from .models import Client
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        client = request.form.get('client')

        if len(client) < 1:
            flash('Client is too short', catgory='error')
        else:
            new_client = Client(data=client, user_id=current_user.id)
            db.session.add(new_client)
            db.session.commit()
            flash('Client added!', category='success')

    return render_template("home.html", user=current_user)

@views.route('/delete-client', methods=['POST'])
def delete_client():
    client = json.loads(request.data)
    clientId = client['clientId']
    client = Client.query.get(clientId)
    if client:
        if client.user_id == current_user.id:
            db.session.delete(client)
            db.session.commit()
           
    return jsonify({})