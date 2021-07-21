from __future__ import absolute_import
from backend.celery import app
from .tendency import UserUpdateTendency

@app.task
def update_user_recommend():
    ut = UserUpdateTendency()
    ut.create_users_tendency()
    ut.create_recommend_list_by_users()
