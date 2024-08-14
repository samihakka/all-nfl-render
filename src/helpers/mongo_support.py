from pymongo import MongoClient
from pymongo.server_api import ServerApi

class MongoConnect:
    def __init__(self) -> None:
        pass
    def connect_collecion(self):
        uri = "mongodb+srv://shakka32:chickendinner@nfl.uvhq9b9.mongodb.net/?retryWrites=true&w=majority&appName=NFL"
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        return client


    def deploy(self, payload):

        client = self.connect_collecion()

        db = client.get_database("NFL")
        collection = db.get_collection("wins_and_losses")
        print(collection)

        collection.insert_one(payload)
        client.close()

    def load(self, collection):
        client = self.connect_collecion()

        db = client.get_database("NFL")
        collection = db.get_collection("getting_there")

        document = collection.find_one({"season": 2023})
        return document
