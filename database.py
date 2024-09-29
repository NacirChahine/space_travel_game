import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
mongodb_uri = os.getenv("MONGODB_URI")

# MongoDB connection
client = MongoClient(mongodb_uri)
db = client['spaceship_game']
scores_collection = db['high_scores']


def load_top_scores():
    # Retrieve the top 5 scores sorted by high_score in descending order
    top_scores = list(scores_collection.find({}, sort=[("high_score", -1)]).limit(5))
    return top_scores  # Returns a list of dictionaries with high_score, initials, and scored_at


def save_high_score(score, initials):
    # Load the top 5 scores
    top_scores = load_top_scores()

    # Check if the player's score is higher than the lowest in the top 5
    if len(top_scores) < 5 or score > top_scores[-1]['high_score']:
        # Insert the new score
        scores_collection.insert_one({
            "high_score": score,
            "initials": initials,
            "scored_at": datetime.utcnow()  # Save the date and time in UTC
        })
