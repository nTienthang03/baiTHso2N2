from flask import Flask, render_template
import requests

app = Flask(__name__)

CURRENCY_API_URL = 'https://v6.exchangerate-api.com/v6/5b87e99ce4e3f41c06ed7813/latest/USD'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/gold')
def gold_price():
    try:
        headers = {
            'x-access-token': 'goldapi-vyuzismadtfu83-io',
            'User-Agent': 'Mozilla/5.0'
        }
        response = requests.get("https://www.goldapi.io/api/XAU/USD", headers=headers)
        data = response.json()

        # Giá vàng 1 ounce (oz) theo USD
        price_per_ounce_usd = data['price']

        # Quy đổi: 1 lượng vàng = 1.20565 oz
        gold_price_usd = price_per_ounce_usd * 1.20565

        # Chuyển sang VND (giả sử tỷ giá ~24,500 VND/USD)
        gold_price_vnd = gold_price_usd * 24500
        formatted_price = f"{gold_price_vnd:,.0f} VND/lượng"

    except Exception as e:
        formatted_price = f"Lỗi khi lấy giá vàng: {e}"

    return render_template('gold.html', gold_price=formatted_price)

@app.route('/usd')
def usd_rate():
    try:
        url = 'https://v6.exchangerate-api.com/v6/5b87e99ce4e3f41c06ed7813/latest/USD'
        response = requests.get(url).json()
        vnd_rate = response['conversion_rates']['VND']
        usd_vnd = f"{vnd_rate:,.0f} VND/USD"
    except Exception as e:
        usd_vnd = f"Lỗi khi lấy dữ liệu: {e}"
    return render_template('usd.html', usd_rate=usd_vnd)

@app.route('/weather')
def weather_info():
    try:
        url = 'https://api.open-meteo.com/v1/forecast?latitude=21.5469&longitude=105.8472&current_weather=true&timezone=Asia%2FSingapore'
        response = requests.get(url).json()
        current = response['current_weather']

        # Bảng mã thời tiết
        weather_codes = {
            0: "Trời quang",
            1: "Phần lớn nắng",
            2: "Có mây",
            3: "U ám",
            45: "Sương mù nhẹ",
            48: "Sương mù dày",
            51: "Mưa phùn nhẹ",
            53: "Mưa phùn vừa",
            55: "Mưa phùn dày",
            61: "Mưa nhỏ",
            63: "Mưa vừa",
            65: "Mưa lớn",
            80: "Mưa rào nhẹ",
            81: "Mưa rào vừa",
            82: "Mưa rào mạnh",
            95: "Dông",
            96: "Dông kèm mưa nhỏ",
            99: "Dông kèm mưa lớn"
        }

        code = current['weathercode']
        condition_text = weather_codes.get(code, "Không rõ")

        weather = {
            "location": "Thái nguyên",
            "temperature": f"{current['temperature']}°C",
            "condition": f"{condition_text} - Gió: {current['windspeed']} km/h"
        }
    except Exception as e:
        weather = {
            "location": "Thái Nguyên",
            "temperature": "Không lấy được dữ liệu",
            "condition": str(e)
        }
    return render_template('weather.html', weather=weather)

if __name__ == '__main__':
    app.run(debug=True)
