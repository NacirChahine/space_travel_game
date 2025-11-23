import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, PyMongoError
from dotenv import load_dotenv
from datetime import datetime
import logging
from src.config import GAME_VERSION

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DBManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        load_dotenv()
        self.mongodb_uri = os.getenv("MONGODB_URI")
        self._client = None
        self._db = None
        self._scores_collection = None

    def get_connection(self):
        try:
            if self._client is None:
                logger.info("Creating new MongoDB connection...")
                self._client = MongoClient(
                    self.mongodb_uri,
                    serverSelectionTimeoutMS=5000,
                    connectTimeoutMS=5000,
                    socketTimeoutMS=5000,
                    maxPoolSize=10,
                    retryWrites=True
                )
                self._db = self._client['spaceship_game']
                self._scores_collection = self._db['high_scores']
                self._client.admin.command('ping')
                logger.info("MongoDB connection successful")
            return self._scores_collection
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"MongoDB connection failed: {e}")
            self._reset_connection()
            return None
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            self._reset_connection()
            return None

    def _reset_connection(self):
        self._client = None
        self._db = None
        self._scores_collection = None

    def load_top_scores(self, version=None):
        """
        Load top 5 scores for a specific game version.

        Args:
            version: Game version to filter by. If None, uses current GAME_VERSION.

        Returns:
            List of top 5 score documents for the specified version.
        """
        try:
            collection = self.get_connection()
            if collection is None:
                return []

            # Use current version if not specified
            if version is None:
                version = GAME_VERSION

            # Filter scores by version and get top 5
            query = {"version": version}
            top_scores = list(collection.find(query, sort=[("high_score", -1)]).limit(5))
            logger.info(f"Successfully loaded {len(top_scores)} top scores for version {version}")
            return top_scores
        except PyMongoError as e:
            logger.error(f"Error loading top scores: {e}")
            self._reset_connection()
            return []
        except Exception as e:
            logger.error(f"Unexpected error loading top scores: {e}")
            return []

    def save_high_score(self, score, initials, version=None):
        """
        Save a high score for a specific game version.

        Args:
            score: The player's score
            initials: The player's initials (3 letters)
            version: Game version to save under. If None, uses current GAME_VERSION.

        Returns:
            True if score was saved successfully, False otherwise.
        """
        try:
            collection = self.get_connection()
            if collection is None:
                return False

            # Use current version if not specified
            if version is None:
                version = GAME_VERSION

            # Load top scores for this version only
            top_scores = self.load_top_scores(version)

            # Check if score qualifies for top 5 in this version
            if len(top_scores) < 5 or score > top_scores[-1]['high_score']:
                collection.insert_one({
                    "high_score": score,
                    "initials": initials,
                    "version": version,
                    "scored_at": datetime.utcnow()
                })
                logger.info(f"Successfully saved high score: {initials} - {score} (version {version})")
                return True
            return False
        except PyMongoError as e:
            logger.error(f"Error saving high score: {e}")
            self._reset_connection()
            return False
        except Exception as e:
            logger.error(f"Unexpected error saving high score: {e}")
            return False

    def close_connection(self):
        try:
            if self._client is not None:
                self._client.close()
                logger.info("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {e}")
        finally:
            self._reset_connection()
