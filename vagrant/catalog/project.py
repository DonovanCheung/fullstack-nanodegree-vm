#!/usr/bin/env python3
from flask import Flask, render_template, request
from flask import redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc, func
from sqlalchemy.orm import sessionmaker, scoped_session
from database_setup import Base, Electronics, Device, User
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Electronics Catalog Application"

# Connect to Database and create database session
engine = create_engine('sqlite:///electronics.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = scoped_session(sessionmaker(bind=engine))

# Create anti-forgery state token
@app.route('/login/')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if (stored_access_token is not None and
       gplus_id == stored_gplus_id):
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;\
    -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

# Home Page
@app.route('/')
@app.route('/electronics')
@app.route('/electronics/')
def homePage():
    electronics = session.query(Electronics).order_by(asc(Electronics.name))
    devices = session.query(Device).order_by(asc(Device.name))
    if 'username' in login_session:
        return render_template('electronics.html', type="All Items",
                               electronics=electronics, devices=devices)
    else:
        return render_template('publicElectronics.html', type="All Items",
                               electronics=electronics, devices=devices)

# Show an Electronics List
@app.route('/electronics/<string:electronic_name>/')
@app.route('/electronics/<string:electronic_name>/items/')
def showElectronics(electronic_name):
    electronics = session.query(Electronics).order_by(asc(Electronics.name))
    electronics_type = session.query(Electronics).filter(
        Electronics.name.ilike(electronic_name)).one()
    devices = session.query(Device).filter_by(
        electronics_id=electronics_type.id).all()
    return render_template('electronics.html',
                           type=electronics_type.name.replace("-", " "),
                           electronics=electronics, devices=devices)

# Show a Device
@app.route('/electronics/<string:electronic_name>/<int:device_id>/')
def showDevice(electronic_name, device_id):
    device = session.query(Device).filter_by(
        id=device_id).one()
    if 'username' in login_session:
        return render_template('device.html', name=electronic_name,
                               device=device)
    else:
        return render_template('publicDevice.html', device=device)


def createUser(login_session):
    print(login_session)
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user.id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None

# Create a new device
@app.route('/devices/new/', methods=['GET', 'POST'])
def newDevice():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        electronic = session.query(Electronics).filter_by(
            name=str(request.form['category'])).one().id
        length = session.query(Device).order_by(Device.id.desc()).first().id+1
        newDevice = Device(name=request.form['name'], id=length,
                           brand=request.form['brand'],
                           year=request.form['year'],
                           description=request.form['description'],
                           price="$"+request.form['price'],
                           electronics_id=session.query(Electronics).filter_by(
                               name=str(request.form['category'])).one().id,
                           user_id=login_session['user_id'])
        session.add(newDevice)
        flash('New Device %s Successfully Created' % newDevice.name)
        session.commit()
        return redirect(url_for('homePage'))
    else:
        return render_template('newDevice.html')

# Edit a device
@app.route('/electronics/<string:electronic_name>/<int:device_id>/edit',
           methods=['GET', 'POST'])
def editDevice(electronic_name, device_id):
    editedDevice = session.query(
        Device).filter_by(id=device_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedDevice.user_id != login_session['user_id']:
        return """<script>function myFunction()\
               {alert('You are not authorized to edit this restaurant.\
               Please create your own restaurant in order to edit.');}\
               </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['name']:
            editedDevice.name = request.form['name']
            editedDevice.brand = request.form['brand']
            editedDevice.year = request.form['year']
            editedDevice.description = request.form['description']
            editedDevice.price = "$"+request.form['price']
            editedDevice.electronics_id = session.query(Electronics).filter_by(
                name=str(request.form['category'])).one().id
            session.commit()
            flash('Device Successfully Edited %s' % editedDevice.name)
            return redirect(url_for('showDevice',
                            electronic_name=electronic_name,
                            device_id=editedDevice.id))
    else:
        return render_template('editDevice.html', electronic=electronic_name,
                               device=editedDevice)

# Delete a device
@app.route('/electronics/<string:electronic_name>/<int:device_id>/delete',
           methods=['GET', 'POST'])
def deleteDevice(electronic_name, device_id):
    deviceToDelete = session.query(
        Device).filter_by(id=device_id).one()
    if request.method == 'POST':
        session.delete(deviceToDelete)
        session.commit()
        flash('%s Successfully Deleted' % deviceToDelete.name)
        return redirect(url_for('homePage'))
    else:
        return render_template('deleteDevice.html', device=deviceToDelete)


# JSON APIs to view Electronics Information
@app.route('/electronics/<string:electronic_name>/JSON')
def electronicsJSON(electronic_name):
    electronics = session.query(Electronics).filter_by(
        name=electronic_name).one()
    items = session.query(Device).filter_by(
        electronics_id=electronics.id).all()
    return jsonify(Electronics=[i.serialize for i in items])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
