ACTIVE_USER_ID = None

def set_active_user(user_id: str):
    global ACTIVE_USER_ID
    ACTIVE_USER_ID = user_id

def get_active_user():
    return ACTIVE_USER_ID

def clear_active_user():
    global ACTIVE_USER_ID
    ACTIVE_USER_ID = None
