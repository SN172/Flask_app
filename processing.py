
import pymongo
import os


client = pymongo.MongoClient("localhost", 27017)
db = client.demo


def do_calculation(title):
    query = {"title": {"$regex": title, "$options": "i"}}
    for item in db.democollection.find(query):
    # combine prep and cook times
        total_time = item["prep_time"]+item["cook_time"]
        output = "[{}]\n".format(item["title"])
        output += "DESCRIPTION: {}\n".format(item["desc"])
        output += "This recipe will take about {} minutes and be ".format(total_time)
        output += "~{} calories per serving\n".format(item["calories_per_serving"])
    return output
