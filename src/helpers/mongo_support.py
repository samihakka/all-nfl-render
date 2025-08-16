from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv


class MongoConnect:
    def __init__(self, db_name="NFL"):
        # Load .env only once when class is instantiated
        load_dotenv()
        uri = os.getenv("MONGO_URI")
        if not uri:
            raise ValueError("MONGO_URI not found in environment variables")

        # Create client
        self.client = MongoClient(uri, server_api=ServerApi("1"))
        self.db = self.client[db_name]

        # Test connection
        try:
            self.client.admin.command("ping")
            print("✅ Connected to MongoDB successfully!")
        except Exception as e:
            print("❌ Connection failed:", e)

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def deploy(self, payload, collection_name="wins_and_losses"):
        collection = self.get_collection(collection_name)
        result = collection.insert_one(payload)
        print(f"Inserted document with _id={result.inserted_id}")
        return result

    def load(self, collection_name="getting_there", season=2023):
        collection = self.get_collection(collection_name)
        document = collection.find_one({"season": season})
        return document

    def load_with_year(self, collection_name, year):
        collection = self.get_collection(collection_name)
        document = collection.find_one({"season": year})
        return document

    def close(self):
        self.client.close()
        print("🔒 MongoDB connection closed.")
