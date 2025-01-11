from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "login test"

@auth.route('/logout')
def logout():
    return "test logout"

@auth.route('/sign-up')
def sign_up():
    return "test sign-up"
