from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse

# MongoDB credentials
username = "root"
password = "Chaitu895@"  # Replace with your actual password

# URL-encode the username and password
encoded_username = urllib.parse.quote_plus(username)
encoded_password = urllib.parse.quote_plus(password)

# Construct the MongoDB URI
uri = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster0.zklixmv.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)