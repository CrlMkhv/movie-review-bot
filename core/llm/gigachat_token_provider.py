import os
from dotenv import load_dotenv
import requests
import uuid


load_dotenv()

from dataclasses import dataclass


@dataclass
class GigachatTokenResponse:
    access_token: str
    expires_at: int

class GigachatTokenProvider:
    def __init__(self):
        self.credentials=os.getenv("GIGACHAT_CREDENTIALS")
        self.scope=os.getenv("GIGACHAT_SCOPE")


    def get_api_key(self) -> GigachatTokenResponse:
        url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
        myuuid = uuid.uuid4()
        payload = f'scope={self.scope}'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': str(myuuid),
            'Authorization': f'Basic {self.credentials}'
        }

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        data = response.json()
        return GigachatTokenResponse(
            access_token=data["access_token"],
            expires_at=data["expires_at"]
        )

if __name__ == "__main__":
    gigachat = GigachatTokenProvider()
    print(gigachat.get_api_key())