from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, jsonify
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir
import datetime, time
from helpers import *
from sqlalchemy import DATE, cast
from flask_jsglue import JSGlue
import os
import re
import json
import random

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///Nucleus.db")


@app.route("/")
@login_required
def index():


    today = datetime.date.today()
    #print(today)
    week_day = datetime.datetime.today().weekday()
    #print('WEEKDAYYYY' + str(week_day))
    #print(week_day - 1)



    now = datetime.datetime.now()
    #print('NOW' + str(now))
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)


    #secondundo is the amount of seconds away from midnight in UTC Time
    secondundo = int(((now - midnight).seconds) / 60)
    #print(str(secondundo)+'PIGS')

    #Time is based off UTC Time, which is 5 hours ahead (CHECK DAYLIGHT SAVINGS TIME, COULD CHANGE TO 4 Hours)
    #1440 minutes in day, this is saying if time between 1159pm and 5am, subtract the 5 hours
    #else need to add 19 hours forwards to account that it is between 7PM and Midnight (19HR to 24HR)
    #TO DO: When adding these forward, we are pulling deals from the following day, and we need to account for this by subtracting 1 from the given day

    if (secondundo < 1439 and secondundo > 300):
        seconds = int((((now - midnight).seconds) / 60) - 300)
    else:
        seconds = int((((now - midnight).seconds) / 60) + 1140)

        #Still dealing with UTC Time, so the day of week will always be one ahead during 7pm to midnight EST (midnight to 5 UTC)
        #Subtracting one if time is in this interval to account for that so correct deals appear from correct day
        if week_day != 0:
            week_day -= 1
            #print(week_day)
        else:
            week_day = 6

    #if (secondundo < 1439 and secondundo > 300):


    #print('SECONDS' +str(seconds))


    #steals = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week JOIN dailyhour AS d ON b.time_start = d.timehour JOIN hourdaily as e on b.time_end = e.hdaily WHERE :seconds >= minuteman AND :seconds <= mininterval AND daynum = :weekd ORDER BY time_start ASC", weekd = week_day, seconds=seconds)

    #upcomingdeals = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week JOIN dailyhour AS d ON b.time_start = d.timehour JOIN hourdaily as e on b.time_end = e.hdaily WHERE :seconds <= minuteman AND daynum = :weekd ORDER BY time_start ASC", weekd = week_day, seconds=seconds)


    #print('this is steals: ', steals)
    #print('this is json steals: ', json.dumps(steals))
    # cream = jsonify(steals)
    #print(cream)
    #barjson = json.dumps(steals)
    #print(barjson)
    #day_hour = datetime.datetime.today().time()
    #print(day_hour)

    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    seconds = int((((now - midnight).seconds) / 60) - 300)


    #timestuff = db.execute("SELECT * FROM deals AS a JOIN dailyhour AS b ON a.time_start = b.minuteman WHERE :seconds <= minutema ON ", seconds=seconds)
   # timestuff = db.execute("SELECT * FROM bars AS a Join deals AS b JOIN dailyhour AS c ON b.time_start = c.timehour JOIN hourdaily AS d ON b.time_end = d.hdaily WHERE :seconds >= minuteman AND :seconds <= mininterval ORDER BY time_start ASC", seconds=seconds)

    #asdf = cast(timestuff as datetime)ORDER BY time_start DESC
    #print(timestuff)

    #print(xyz)

    #asdf = db.execute("SELECT time_start FROM deals WHERE cast(time_start as datetime) > :timestuff", timestuff=datetime.datetime.today().time())
    #print(asdf)

    #mapadd(steals)

    if request.args.get("zipnasty") == None:
        return render_template("index.html")

    else:
        return render_template("review.html")

@app.route("/review")
def review():
    campaign = request.args.get("campaign")
    print(campaign)

    due = request.args.get("due")
    #hi970 = request.args.get("970x250")
    #print(hi970)
    #print(due)

    budget = request.args.get("budget")
    viewability = request.args.get("viewability")
    adunits = []
    targets= []
    geos = []
    starts = []
    ends = []
    conts = []

    note = request.args.get("note")
    if request.args.get("970x250") != None:
        adunits.append(request.args.get("970x250"))

    if request.args.get("300x600") != None:
        adunits.append(request.args.get("300x600"))

    if request.args.get("728x90") != None:
        adunits.append(request.args.get("728x90"))

    if request.args.get("300x250") != None:
        adunits.append(request.args.get("300x250"))

    if request.args.get("320x50") != None:
        adunits.append(request.args.get("320x50"))

    if request.args.get("Preroll") != None:
        adunits.append(request.args.get("Preroll"))

    if request.args.get("Native") != None:
        adunits.append(request.args.get("Native"))

    print(adunits)

    #publishers = []
    for i in range(1,16):
        demo = "demo" + str(i)
        geo = "geo" + str(i)
        contextual = "contextual" + str(i)
        start = "start" + str(i)
        end = "end" + str(i)
        print(demo)
        print(geo, contextual, start, due)
        if request.args.get(demo) != None and request.args.get(geo) != None and request.args.get(contextual) != None:
            targets.append(request.args.get(demo))
        geos.append(request.args.get(geo))
        ends.append(request.args.get(end))
        starts.append(request.args.get(start))
        conts.append(request.args.get(contextual))
    print(targets)
    length = len(targets)

    publishers = request.args.to_dict()
    #print(publishers)



    return render_template("review.html", campaign=campaign, note=note, adunits=adunits, conts=conts, ends=ends, starts=starts, length=length, geos=geos, due=due, budget=budget, viewability=viewability, publishers=publishers, targets=targets)


@app.route("/login", methods=["POST", "GET"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        #print(rows)
        #print("HELLLOOOOOO")

        #pass = db.execute("SELECT * FROM users WHERE ")

        # ensure username exists and password is correct
        if len(rows) != 1:
            return render_template("login.html")

        #if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
        #    return render_template("login.html")

        # remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        #print('TESSSSSS')
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("index"))

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/history")
def history():

    hist = db.execute("SELECT * FROM rfps")
    print(hist)

    return render_template("history.html", hist=hist)









    #steals = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week JOIN dailyhour AS d ON b.time_start = d.timehour JOIN hourdaily as e on b.time_end = e.hdaily WHERE :seconds >= minuteman AND :seconds <= mininterval AND daynum = :weekd ORDER BY time_start ASC", weekd = week_day, seconds=seconds)

    #barjson = json.dumps(steals)

    # redirect user to login form
    #return barjson




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        #ensure password confirmation submitted
        elif not request.form.get("confirm password"):
            return apology("must confirm password")

        # query db for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        #ensure username is available
        if len(rows) != 0:
            return apology("username not available, please try again")

        #ensure passwords match
        if request.form.get("password") != request.form.get("confirm password"):
            return render_template("register.html")

        #hash passwrod
        hash = pwd_context.encrypt(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash, email, zipcode) VALUES(:username, :hash, :email, :zipcode)", username=request.form.get('username'), hash=hash, email=request.form.get('email'), zipcode=request.form.get('zipcode'))

        #print(zipcode)
        #log user in automatically and remember who user is
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]

        return redirect(url_for("index"))


    else:
        return render_template("register.html")


@app.route("/mapadd", methods=["GET", "POST"])
def mapadd():
    #return json.dumps(x)

    """Log user out."""
    #return json.dumps(zipresults)
    #print("dickhead")
    today = datetime.date.today()
    #print(today)
    week_day = datetime.datetime.today().weekday()
    #print(request.args.get("keyword"))

    now = datetime.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    secondundo = int(((now - midnight).seconds) / 60)
    y = request.form.get("keyword")
    #print(y)
    #if y:
    #print(y)
    #print('mapadd')
    x = request.args.get("zipnasty")
    #print(str(x) + 'ABC123')
    #if x:
    #print(x)

    if (secondundo < 1439 and secondundo > 300):
        seconds = int((((now - midnight).seconds) / 60) - 300)
    else:
        seconds = int((((now - midnight).seconds) / 60) + 1140)

        #Still dealing with UTC Time, so the day of week will always be one ahead during 7pm to midnight EST (midnight to 5 UTC)
        #Subtracting one if time is in this interval to account for that so correct deals appear from correct day
        if week_day != 0:
            week_day -= 1
            #print(week_day)
        else:
            week_day = 6

    # forget any user_id
    #if request.args.get("zipnasty") != None:
    if x:
        x = request.args.get("zipnasty")  + "%"
        #print(x + "asdffdsa")
        zipresults = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week JOIN hoods AS d ON a.zip = d.codezip WHERE daynum = :weekd AND a.zip LIKE :search OR d.hood LIKE :search", weekd = week_day, search = x)
        #print(zipresults)
        return json.dumps(zipresults)

    elif request.args.get("keyword") != None:
        y = "%" + request.args.get("keyword")  + "%"
        zipresults = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week WHERE daynum = :weekd AND b.deal LIKE :search", weekd = week_day, search = y)
        return json.dumps(zipresults)
    else:
        zipresults = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week JOIN dailyhour AS d ON b.time_start = d.timehour JOIN hourdaily as e on b.time_end = e.hdaily WHERE :seconds >= minuteman AND :seconds <= mininterval AND daynum = :weekd ORDER BY time_start ASC", weekd = week_day, seconds=seconds)
        return json.dumps(zipresults)

#@app.route("/mapsearch")
#def mapsearch():
#    """Log user out."""
#
#    today = datetime.date.today()
#    #print(today)
#    week_day = datetime.datetime.today().weekday()


#    now = datetime.datetime.now()
#    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

#    secondundo = int(((now - midnight).seconds) / 60)
#    y = request.args.get("keyword")
    #if y:
    #    print(y)
#    x = request.args.get("zipnasty")
    #print(cheese)
    #if x:
        #print(x)

#    if (secondundo < 1439 and secondundo > 240):
##        seconds = int((((now - midnight).seconds) / 60) - 240)
#    else:
#        seconds = int((((now - midnight).seconds) / 60) + 1200)
    # forget any user_id
    #if request.args.get("zipnasty") != None:
#    if x:
#        x = request.args.get("zipnasty")  + "%"
        #print(x + "!")
#        zipresults = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week JOIN hoods AS d ON a.zip = d.codezip WHERE daynum = :weekd AND a.zip LIKE :search OR d.hood LIKE :search", weekd = week_day, search = x)
        #if zipresults == None:
#        return json.dumps(zipresults)
         #   zipresults = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week JOIN hoods AS d ON a.zip = d.codezip WHERE daynum = :weekd AND d.hood LIKE :search", weekd = week_day, search = x)
        #zipresults = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week JOIN dailyhour AS d ON b.time_start = d.timehour JOIN hourdaily as e on b.time_end = e.hdaily WHERE :seconds >= minuteman AND :seconds <= mininterval AND daynum = :weekd AND a.zip LIKE :search ORDER BY time_start ASC", weekd = week_day, seconds=seconds, search = x)
#    elif request.args.get("keyword") != "":
#        y = "%" + request.args.get("keyword")  + "%"
#        print(y)
#        zipresults = db.execute("SELECT * FROM bars AS a JOIN deals AS b ON a.bar_id = b.id_bar JOIN weekday AS c ON b.day_of_week = c.day_week WHERE daynum = :weekd AND b.deal LIKE :search", weekd = week_day, search = y)
#        return json.dumps(zipresults)


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


    #bucks = db.execute("SELECT * FROM places WHERE postal_code LIKE :q OR place_name LIKE :q OR admin_name1 LIKE :q LIMIT 10 ", q=q)

   # placed = jsonify(bucks)

    #return placed