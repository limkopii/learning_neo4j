#!/usr/bin/python

from neo4j.v1 import GraphDatabase, basic_auth

password = "neo4j" #use env to protect this when go to production
driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("neo4j", password))

# connects to db
db = driver.session()

# get some graphs
results = db.run("MATCH (user:User {name: 'Alice'})-[:LOVE]->(tag:Tag {name:'food'}) "
                "MATCH (website:Website)-[:TAG]->(tag) WHERE NOT (user)-[:SUBSCRIBE]->(website) and website.subscriber > 20000 "
                "return user.name as user, tag.name as tag, website.name as link, website.subscriber as count")

for record in results:
    print record["user"], record["link"], record["count"]