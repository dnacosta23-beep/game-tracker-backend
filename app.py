from flask import Flask, request
from flask_cors import CORS
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


@app.route("/")
def home():
    return {"message": "Online Game Player Tracker API is running"}


@app.route("/players", methods=["GET"])
def get_players():
    response = supabase.table("game_players").select("*").execute()
    return {"players": response.data}


@app.route("/players", methods=["POST"])
def add_player():
    data = request.get_json()

    new_player = {
        "username": data["username"],
        "email": data["email"],
        "game_name": data["game_name"]
    }

    response = supabase.table("game_players").insert(new_player).execute()

    return {
        "message": "Player added successfully",
        "player": response.data
    }, 201


if __name__ == "__main__":
    app.run(debug=True)