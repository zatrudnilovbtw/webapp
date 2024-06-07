from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '736ecdd2b0adfe0fc9fcc686c178fc1f'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    return response.json()

def get_exchange_rates():
    try:
        crypto_url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,the-open-network&vs_currencies=rub'
        crypto_response = requests.get(crypto_url)
        crypto_data = crypto_response.json()

        usd_to_rub = get_usd_to_rub()
        eur_to_rub = get_eur_to_rub()

        exchange_rates = {
            'usd': usd_to_rub,
            'eur': eur_to_rub,
            'btc': crypto_data['bitcoin']['rub'],
            'eth': crypto_data['ethereum']['rub'],
            'ton': crypto_data['the-open-network']['rub'],
        }
        return exchange_rates
    except KeyError as e:
        print(f"KeyError: {e}")
        return None

def get_usd_to_rub():
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    response = requests.get(url)
    data = response.json()
    return data['rates']['RUB']

def get_eur_to_rub():
    url = 'https://api.exchangerate-api.com/v4/latest/EUR'
    response = requests.get(url)
    data = response.json()
    return data['rates']['RUB']

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    exchange_rates = get_exchange_rates()
    if request.method == 'POST':
        city = request.form.get('city')
        weather = get_weather(city)
    return render_template('index.html', weather=weather, exchange_rates=exchange_rates)

if __name__ == '__main__':
    app.run(debug=True)
