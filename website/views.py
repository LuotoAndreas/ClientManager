from flask import Blueprint, flash, render_template, request, url_for, jsonify, redirect
from flask_login import login_required, current_user
from .models import Client
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

@views.route('/update-client', methods=['POST'])
@login_required
def update_client():
    data = json.loads(request.data)
    client_id = data.get('clientId')
    field = data.get('field')
    value = data.get('value')

    # Get the client to update
    client = Client.query.get(client_id)
    if client and client.user_id == current_user.id:
        if hasattr(client, field):
            setattr(client, field, value)
            db.session.commit()
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Invalid field'})
    else:
        return jsonify({'success': False, 'message': 'Client not found or unauthorized'})


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        # Extracting form data
        pre_factura = request.form.get('pre_factura')
        documento = request.form.get('documento')
        fecha_emision = request.form.get('fecha_emision')  # This is a string
        pagado = request.form.get('pagado')  # This can be a date or None
        ruc = request.form.get('ruc')
        compania = request.form.get('compania')
        moneda = request.form.get('moneda')
        cantidad = request.form.get('cantidad', type=float)
        precio_unitario = request.form.get('precio_unitario', type=float)
        parcial = request.form.get('parcial', type=float)
        igv = request.form.get('igv', type=float)
        total = request.form.get('total', type=float)
        descripcion = request.form.get('descripcion')

        # Convert fecha_emision to a datetime object
        try:
            fecha_emision = datetime.strptime(fecha_emision, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format for Fecha Emision. Use YYYY-MM-DD.', category='error')
            return redirect(url_for('views.home'))

        # Convert pagado to a datetime object, or None if not provided
        if pagado:
            try:
                # Parse the datetime string into a datetime object
                pagado = datetime.strptime(pagado, '%Y-%m-%d').date()  # Handle datetime-local format
            except ValueError:
                flash('Invalid datetime format for Pagado. Use YYYY-MM-DD.', category='error')
                return redirect(url_for('views.home'))
        else:
            pagado = None  # If not provided, set it to None

        # Validate required fields
        if not pre_factura or not documento:
            flash('PRE FACTURA and DOCUMENTO are required.', category='error')
        else:
            # Add the new client to the database
            new_client = Client(
                pre_factura=pre_factura,
                documento=documento,
                fecha_emision=fecha_emision,
                pagado=pagado,
                ruc=ruc,
                compania=compania,
                moneda=moneda,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                parcial=parcial,
                igv=igv,
                total=total,
                descripcion=descripcion,
                user_id=current_user.id
            )
            db.session.add(new_client)
            db.session.commit()
            flash('Client added successfully!', category='success')
            return redirect(url_for('views.home'))

    # Render the home page with the user object
    return render_template("home.html", user=current_user)

@views.route('/delete-client', methods=['POST'])
def delete_client():
    client = json.loads(request.data)
    clientId = client.get('clientId')
    client = Client.query.get(clientId)
    if client and client.user_id == current_user.id:
        db.session.delete(client)
        db.session.commit()
    return jsonify({})
