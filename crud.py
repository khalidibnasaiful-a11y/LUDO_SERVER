from models import User

def create_user(db, data):
    user = User(username=data.username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db, username):
    return db.query(User).filter(User.username == username).first()

def update_coins(db, user_id, coins):
    user = db.query(User).filter(User.id == user_id).first()
    user.coins = coins
    db.commit()
