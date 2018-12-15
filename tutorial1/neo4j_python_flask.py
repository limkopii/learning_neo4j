#!/usr/bin/python

from neo4j.v1 import GraphDatabase, basic_auth
import os
from json import dumps
from flask import Flask, g, Response, request

password = "neo4j" #use env to protect this when go to production
driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("neo4j", password))

# connects to db
db = driver.session()

# apps
app = Flask(__name__, static_url_path='/static/')

def serialize_tag(tag):
    return {
        'name': tag["name"],
    }

def serialize_user(user):
    return {
        'name': user["name"]
    }

def serialize_subscribe(subscribe):
    return {
        'name': subscribe["user"],
        'link': subscribe["link"]
    }

def serialize_recommendation(recommend):
    return {
        'user': recommend["user"],
        'link': recommend["link"],
        'count': recommend["count"],
    }


@app.route("/recommendations/<user>")
def get_recommendation(user):
    # get some graphs
    results = db.run("MATCH (user:User {name: {user}})-[:LOVE]->(tag:Tag {name:'food'}) "
                    "MATCH (website:Website)-[:TAG]->(tag) WHERE NOT (user)-[:SUBSCRIBE]->(website) and website.subscriber > 20000 "
                    "return user.name as user, tag.name as tag, website.name as link, website.subscriber as count", {"user": user})
    
    dump = [serialize_recommendation(record) for record in results]

    return Response(dumps(dump), mimetype="application/json")

@app.route("/")
def get_index():
    return app.send_static_file('index.html')

@app.route("/users/subscribe")
def get_user_subscribe():
    results = db.run("MATCH (user:User)-[:SUBSCRIBE]->(website:Website) "
                    "RETURN user.name as user, website.name as link")
 
    return Response(dumps([serialize_subscribe(record) for record in results]), mimetype="application/json")

@app.route("/users/")
def get_user():
    results = db.run("MATCH (user:User) "
                    "RETURN user")
 
    return Response(dumps([serialize_user(record["user"]) for record in results]), mimetype="application/json")


@app.route("/tags/")
def get_tag():
    results = db.run("MATCH (tag:Tag) "
                    "RETURN tag")
 
 
    return Response(dumps([serialize_tag(record["tag"]) for record in results]), mimetype="application/json")


if __name__ == '__main__':
    app.run(port=8080)