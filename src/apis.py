from decouple import config
import requests


class API:

    def climate(self, city):

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config('API_KEY_OPENWEATHERMAP')}&lang=pt_br"
        response = requests.get(url)
        data = response.json()
        return data
