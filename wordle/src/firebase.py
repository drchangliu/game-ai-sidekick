from datetime import datetime

import firebase_admin
import pytz
from firebase_admin import credentials, firestore


def initialize_firebase():
    from fb_env import keys

    cred = credentials.Certificate(keys)
    firebase_admin.initialize_app(cred)


def get_db():
    return firestore.client()


def add_retries(db, retries):
    est = pytz.timezone('US/Eastern')
    time = datetime.now(est)

    doc_ref = db.collection('game_retries').document()
    doc_ref.set({
        'count': retries,
        'date': time
    })
