import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, PyMongoError
from dotenv import load_dotenv
from datetime import datetime
import logging

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

    def load_top_scores(self):
        try:
            collection = self.get_connection()
            if collection is None:
                return []
            return list(collection.find({}, sort=[("high_score", -1)]).limit(5))
        except PyMongoError as e:
            logger.error(f"Error loading top scores: {e}")
            self._reset_connection()
            return []
        except Exception as e:
            logger.error(f"Unexpected error loading top scores: {e}")
            return []

    def save_high_score(self, score, initials):
        try:
            collection = self.get_connection()
            if collection is None:
                return False
            
            top_scores = self.load_top_scores()
            if len(top_scores) < 5 or score > top_scores[-1]['high_score']:
                collection.insert_one({
                    "high_score": score,
                    "initials": initials,
                    "scored_at": datetime.utcnow()
                })
                logger.info(f"Successfully saved high score: {initials} - {score}")
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
