from pymongo import MongoClient

client = MongoClient("mongodb+srv://RaulDelaRosa:Lepera69!@geometry.sopbp.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


def getDataFromMongo(db,coll,query={}):
    res = client[db][coll]

    return list(res.find(query))

