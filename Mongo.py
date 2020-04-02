# importing client mongo to make the connection
# python -m easy_install pymongo
# MongoDB LocalHost Connection
# add plugin of MongoDB in pycharm from project setting as you added github plugin
from pymongo import MongoClient


class dal:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def getHost(self):
        return self.host

    def getPort(self):
        return self.port
    # def setCollection(collection):
    # self.collection = collection
    # def setDocument(document):
    # self.document = document


def main():
    dalHandler = dal('localhost', 27017)
    # Connection to MongoDB
    try:
        # client = MongoClient('localhost', 27017)
        client = MongoClient(dalHandler.getHost(), dalHandler.getPort())
        # Selection the Database i.e. recipes_db or one you created it
        db = client.recipes_db
        # Select the collection i.e. recipes collection or one you created it
        collection = db.recipes
        # Set up a document, and adding data into Recipes_db
        user = {"id": 1, "username": "Riken"}
        # insert one document into selected document
        # result = collection.insert(user)
        # insert_one or insert_many instead
        result = collection.insert_one(user)
        # Selection just one document from collection
        result = collection.find()
        # Print out all objects from the collection
        for x in result:
            print(x)
        # removing the document inserted
        # result = collection.remove(user)
    except:
        print("Cannot connect to the MongoDB")


if __name__ == "__main__":
    main()
