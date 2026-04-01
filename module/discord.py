import requests

class DiscordAPI:
    def __init__(self, token):
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def claimHypeSquad(self, houseId: int):
        jsonData = {'house_id': houseId}
        response = self.session.post(
            'https://discord.com/api/v9/hypesquad/online',
            json=jsonData,
            timeout=10
        )
        return response

    def check(self):
        response = self.session.get(
            'https://discord.com/api/v9/users/@me',
            timeout=10
        )
        return response

    def closeSession(self):
        self.session.close()
