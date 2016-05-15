from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'secretKey'
DB_NAME = 'blog'

DATABASE = MongoClient()[DB_NAME]
POSTS_COLLECTION = DATABASE.posts
USERS_COLLECTION = DATABASE.users
SETTINGS_COLLECTION = DATABASE.settings

DEBUG = True
