import requests

BASE_URL = "https://node.alkowall.indigoingenium.ba"

class Api:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url

    def get_ad_url(self, device_id):
        # Function to get ad URL
        url = f"{self.base_url}/advertisment/get_ad_url"
        payload = {"device_id": device_id}
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            # Assuming the response JSON has an "ad_url" field
            ad_url = response.json().get("ad_url")
            if ad_url:
                return ad_url
            else:
                print("No ad URL found in the response.")
                return None
        else:
            print(f"Failed to fetch ad URL. Status code: {response.status_code}")
            return None
