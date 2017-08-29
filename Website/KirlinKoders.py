# Video Game DB Flask application

import os
# Video Game DB Flask application
import sqlite3
from flask import Flask, request, render_template, g

app=Flask(__name__)

#Routes
@app.route("/homepage")
def homepage():
    return render_template("home.html")

@app.route("/browse")
def browse():
    db = get_db()
    rows = db.execute('select VGid,price,title,company,maxPlayer from VideoGame order by price')
    rowlist = rows.fetchall()
    return render_template('browse.html', entries=rowlist)

@app.route("/write", methods=['get', 'post'])	
def write():
    debug("form data=" + str(request.form))
    # Step 1, display form
    if "step" not in request.form:
        return render_template('write.html', step="compose_entry")
        
        
        
    #Step 2, add blog post to database.
    elif request.form["step"] == "add_entry":
        db = get_db()
        #get PW
        pwlist = db.execute('select password from Users where username = ?' , [request.form['username']])
        pwrow = pwlist.fetchone()
        try:
            dbpw = pwrow[0]
        except TypeError:
            return render_template("write.html", step="wrong")
        #get UN
        unrowlist = db.execute('select username from Users where username = ?' , [request.form['username']])
        unrow = unrowlist.fetchone()
        dbun = unrow[0]
        if (request.form["username"] == dbun and request.form["password"] == dbpw):
            db.execute("insert into VideoGame (title, company, maxPlayer, price) values (?, ?, ?, ?)",
                   [request.form['title'], request.form['company'], request.form["maxPlayer"], request.form["price"]])
            db.commit()
            return render_template("write.html", step="add_entry")
        
        return render_template("write.html", step="wrong")

        
        
@app.route("/edit", methods=['get', 'post'])
def edit():
    debug("form data=" + str(request.form))

    # Step 1, display form to select which entry to edit
    if "step" not in request.form:
        db = get_db()
        rows = db.execute('select VGid, price, title, company, maxPlayer from VideoGame order by price')
        rowlist = rows.fetchall()
        return render_template('edit.html', step="display_entries", entries=rowlist)
    
    elif request.form["step"] == "make_edits":
        db = get_db()
        # get the VGid from the form
        VGid = int(request.form["VGid"])
        row = db.execute("select VGid, price, title, company, maxPlayer from VideoGame where VGid=?", [VGid])
        therow = row.fetchone()
        return render_template("edit.html", step="make_edits", entry=therow)
    elif request.form["step"] == "update_database":
        db = get_db()
        VGid = int(request.form["VGid"])
        #get PW
        pwlist = db.execute('select password from Users where username = ?' , [request.form['username']])
        pwrow = pwlist.fetchone()
        try:
            dbpw = pwrow[0]
        except TypeError:
            return render_template("edit.html", step="wrong")
        #get UN
        unrowlist = db.execute('select username from Users where username = ?' , [request.form['username']])
        unrow = unrowlist.fetchone()
        try:
            dbun = unrow[0]
        except TypeError:
            return render_template("edit.html", step="wrong")
        if (request.form["username"] == dbun and request.form["password"] == dbpw):
            db.execute("update VideoGame set title = ?, company = ?, maxPlayer = ?, price = ? where VGid = ?", [request.form["title"],request.form["company"],request.form["maxPlayer"], request.form["price"], VGid])
            db.commit()
            return render_template("edit.html", step="update_database")        
                        
@app.route("/delete", methods=['get', 'post'])
def delete():
    debug("form data=" + str(request.form))
    
    # Step 1, display form to select which entry to delete
    if "step" not in request.form:
        db = get_db()
        rows = db.execute('select * from VideoGame order by price')
        rowlist = rows.fetchall()
        return render_template('delete.html', step="display_entries", entries=rowlist)
    elif request.form["step"] == "delete_entry":
        db = get_db()
        VGid = int(request.form["VGid"])
        #get PW
        pwlist = db.execute('select password from Users where username = ?' , [request.form['username']])
        pwrow = pwlist.fetchone()
        try:
            dbpw = pwrow[0]
        except TypeError:
            return render_template("delete.html", step="wrong")
        #get UN
        unrowlist = db.execute('select username from Users where username = ?' , [request.form['username']])
        unrow = unrowlist.fetchone()
        try:
            dbun = unrow[0]
        except TypeError:
            return render_template("delete.html", step="wrong")
        if (request.form["username"] == dbun and request.form["password"] == dbpw):
            db.execute("delete from VideoGame where VGid=?",[VGid])
            db.commit()
            return render_template("delete.html", step="delete_entry")

@app.route("/bonus", methods=['get', 'post'])
def bonus():
    db = get_db()
    rows = db.execute('select VGid, title, genre, plat, Rating, releaseYear from VideoGame natural join genre natural join Platform natural join Reviews natural join VGRelease order by VGid')
    rowlist = rows.fetchall()
    return render_template('bonus.html', entries=rowlist)

@app.route("/refresh")
def refresh():
    init_db()
    populate_db()
    return render_template('refresh.html')


@app.route("/", methods=['get', 'post'])	
def signup():
    debug("form data=" + str(request.form))
    if "step" not in request.form:
        return render_template('signup.html', step="new_user")
    elif request.form["step"] == "add_entry":
        db = get_db()
        uid = db.execute("select max(userid) from Users")
        for row in uid.fetchall():
            temp = row[0]
        new_uid = temp + 1
        db.execute("insert into Users (userid, name, username, password) values (?, ?, ?, ?)",
                       [new_uid, request.form['name'], request.form['username'], request.form['password']])
        db.commit()
        return render_template("signup.html", step="add_user")
        
@app.route("/signin", methods=['get', 'post'])
def signin():
    if "step" not in request.form:
        return render_template('signin.html', step="user_signin")
    elif request.form["step"] == "signed_in":
#        db = get_db()
#        user = request.form["username"]
#        pwds = db.execute('select password from users where username=?', (user,))
#        pwd = pwds.fetchone()
#        if pwd[0] == request.form["password"]:
#            return render_template("signin.html", step="signed_in")
#        else:
#            return render_template("signin.html", step="incorrect")
        db = get_db()
        pwlist = db.execute('select password from Users where username = ?' , [request.form['username']])
        pwrow = pwlist.fetchone()
        try:
            dbpw = pwrow[0]
        except TypeError:
            return render_template("signin.html", step="wrong")
        unrowlist = db.execute('select username from Users where username = ?' , [request.form['username']])
        unrow = unrowlist.fetchone()
        dbun = unrow[0]
        if (request.form["username"] == dbun and request.form["password"] == dbpw):
            return render_template("signin.html", step="signed_in")
        
        return render_template("userpage.html", step="wrong")

@app.route("/userpage", methods = ['get','post'])
def userpage():
    if "step" not in request.form:
        return render_template('userpage.html', step="user_page")
        
    elif request.form["step"] == "view_page":
        db = get_db()
        pwlist = db.execute('select password from Users where username = ?' , [request.form['username']])
        pwrow = pwlist.fetchone()
        try:
            dbpw = pwrow[0]
        except TypeError:
            return render_template("userpage.html", step="wrong")
        unrowlist = db.execute('select username from Users where username = ?' , [request.form['username']])
        unrow = unrowlist.fetchone()
        dbun = unrow[0]
        if (request.form["username"] == dbun and request.form["password"] == dbpw):
            rows = db.execute('select VGid, userid, Rating, Review from Reviews natural join Users where username = ?' , [request.form['username']])
            rowlist = rows.fetchall()
            rows2 = db.execute('select Videogame.VGid, StarRating.avgRate,Videogame.title, Videogame.price from StarRating natural join Videogame natural join WishList natural join Users  where username = ?' , [request.form['username']])
            rowlist2 = rows2.fetchall()
            rows3 = db.execute('select userid, username, name from Users where username = ?' , [request.form['username']])
            rowlist3 = rows3.fetchall()
            return render_template("userpage.html", step="view_page", entries=rowlist, entries2=rowlist2, entries3=rowlist3)
        
        return render_template("userpage.html", step="wrong")
        
####################################################################################### 
# Command line utilities   
def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def init_db_command():
    """Initializes the database."""
    print("Initializing DB.")
    init_db()
    
def populate_db():
    db = get_db()
    with app.open_resource('LargeScalePopulate.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('populate')
def populate_db_command():
    """Populates the database with sample data."""
    print("Populating DB with sample data.")
    populate_db()

##################################################################################
# Debugging

def debug(s):
    """Prints a message to the screen (not web browser) 
    if FLASK_DEBUG is set."""
    if app.config['DEBUG']:
        print(s)
###################################################################################
# Database handling 
  
def connect_db():
    """Connects to the database."""
    debug("Connecting to DB.")
    conn = sqlite3.connect(os.path.join(app.root_path, 'videogames.db'))
    conn.row_factory = sqlite3.Row
    return conn
    
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'db_connection'):
        g.db_connection = connect_db()
    return g.db_connection
    
@app.teardown_appcontext
def close_db(error):
    """Closes the database automatically when the application
    context ends."""
    debug("Disconnecting from DB.")
    if hasattr(g, 'db_connection'):
        g.db_connection.close()



