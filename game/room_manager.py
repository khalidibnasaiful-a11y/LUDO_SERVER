from config import MAX_PLAYERS

class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, room_id, entry_fee):
        self.rooms[room_id] = {
            "room_id": room_id,
            "entry_fee": entry_fee,
            "players": [],
            "is_full": False
        }

    def join_room(self, room_id, user_id):
        room = self.rooms[room_id]

        if user_id not in room["players"]:
            room["players"].append(user_id)

        if len(room["players"]) >= MAX_PLAYERS:
            room["is_full"] = True

        return room
