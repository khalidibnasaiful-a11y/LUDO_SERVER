from config import ENTRY_FEES, MAX_PLAYERS

class MatchManager:
    def __init__(self):
        self.matches = {}

    def start_match(self, room_id, players, entry_fee):
        prize = ENTRY_FEES[entry_fee]["prize"]
        self.matches[room_id] = {
            "room_id": room_id,
            "players": players,
            "prize": prize,
            "winner": None
        }
        return self.matches[room_id]

    def set_winner(self, room_id, winner_id):
        match = self.matches[room_id]
        match["winner"] = winner_id
        return match
