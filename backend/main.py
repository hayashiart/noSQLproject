from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from bson import ObjectId
from datetime import datetime

from database import users_collection

app = FastAPI(title="Gestion Profils Utilisateurs")

app.mount("/static", StaticFiles(directory="static"), name="static")


# CRUD 

@app.post("/users")
async def create_user(user: dict):
    """Créer un utilisateur"""
    user.setdefault("premium", False)           
    user["created_at"] = user["updated_at"] = datetime.utcnow()
    
    result = users_collection.insert_one(user)
    
    # Retourner l'utilisateur créé avec id en string
    created = users_collection.find_one({"_id": result.inserted_id})
    created["id"] = str(created.pop("_id"))
    return created


@app.get("/users")
async def get_all_users():
    """Récupérer tous les utilisateurs"""
    users = list(users_collection.find())
    for u in users:
        u["id"] = str(u.pop("_id"))
    return users


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Récupérer un seul utilisateur par ID"""
    try:
        user = users_collection.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(status_code=400, detail="ID invalide")
    
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    user["id"] = str(user.pop("_id"))
    return user



# FRONTEND

@app.get("/", response_class=HTMLResponse)
async def home():
    """Serve the simple frontend"""
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()