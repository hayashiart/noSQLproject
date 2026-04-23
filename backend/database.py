from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")

if not mongo_uri:
    raise ValueError("MONGODB_URI non trouvée dans le fichier .env")

client = MongoClient(mongo_uri)
db = client[os.getenv("DB_NAME", "user_profiles_db")]
users_collection = db["users"]

print(" Connexion à MongoDB reussie (database.py chargé)")