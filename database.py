import os
import sys
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, PyMongoError
from dotenv import load_dotenv
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
def get_env_path():
    """Get the path to the .env file, handling PyInstaller's temp path."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, ".env")

load_dotenv(get_env_path())
mongodb_uri = os.getenv("MONGODB_URI")

# MongoDB client singleton
_client = None
_db = None
_scores_collection = None


def get_database_connection():
    """
    Get or create a MongoDB connection with proper error handling.
    Returns the scores collection or None if connection fails.
    """
    global _client, _db, _scores_collection

    try:
        # Create new connection if it doesn't exist
        if _client is None:
            logger.info("Creating new MongoDB connection...")
            _client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                connectTimeoutMS=5000,
                socketTimeoutMS=5000,
                maxPoolSize=10,
                retryWrites=True
            )
            _db = _client['spaceship_game']
            _scores_collection = _db['high_scores']

            # Test the connection
            _client.admin.command('ping')
            logger.info("MongoDB connection successful")

        return _scores_collection

    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        logger.error(f"MongoDB connection failed: {e}")
        # Reset connection variables to force reconnection on next attempt
        _client = None
        _db = None
        _scores_collection = None
        return None

    except Exception as e:
        logger.error(f"Unexpected error connecting to MongoDB: {e}")
        _client = None
        _db = None
        _scores_collection = None
        return None


def load_top_scores():
    """
    Retrieve the top 5 scores sorted by high_score in descending order.
    Returns a list of dictionaries with high_score, initials, and scored_at.
    Returns an empty list if the database is unavailable.
    """
    try:
        collection = get_database_connection()

        if collection is None:
            logger.warning("Database unavailable, returning empty scores list")
            return []

        # Retrieve the top 5 scores
        top_scores = list(collection.find({}, sort=[("high_score", -1)]).limit(5))
        logger.info(f"Successfully loaded {len(top_scores)} top scores")
        return top_scores

    except PyMongoError as e:
        logger.error(f"Error loading top scores: {e}")
        # Reset connection on error
        global _client, _db, _scores_collection
        _client = None
        _db = None
        _scores_collection = None
        return []

    except Exception as e:
        logger.error(f"Unexpected error loading top scores: {e}")
        return []


def save_high_score(score, initials):
    """
    Save a high score to the database if it qualifies for the top 5.
    Returns True if the score was saved successfully, False otherwise.
    """
    try:
        collection = get_database_connection()

        if collection is None:
            logger.warning("Database unavailable, cannot save high score")
            return False

        # Load the top 5 scores
        top_scores = load_top_scores()

        # Check if the player's score is higher than the lowest in the top 5
        if len(top_scores) < 5 or score > top_scores[-1]['high_score']:
            # Insert the new score
            collection.insert_one({
                "high_score": score,
                "initials": initials,
                "scored_at": datetime.utcnow()  # Save the date and time in UTC
            })
            logger.info(f"Successfully saved high score: {initials} - {score}")
            return True

        return False

    except PyMongoError as e:
        logger.error(f"Error saving high score: {e}")
        # Reset connection on error
        global _client, _db, _scores_collection
        _client = None
        _db = None
        _scores_collection = None
        return False

    except Exception as e:
        logger.error(f"Unexpected error saving high score: {e}")
        return False


def close_database_connection():
    """
    Close the MongoDB connection gracefully.
    Should be called when the application exits.
    """
    global _client, _db, _scores_collection

    try:
        if _client is not None:
            _client.close()
            logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")
    finally:
        _client = None
        _db = None
        _scores_collection = None
