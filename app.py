from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/api/compare')
def compare_prices():
    results = []

    bulkory_products = [
        {"name": "Nike Dunk Low Panda", "price": 130},
        {"name": "Adidas Campus 00s Grey", "price": 85},
        {"name": "Supreme Box Logo Tee", "price": 65}
    ]

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for item in bulkory_products:
        query = item['name'].replace(' ', '%20')
        search_url = f"https://stockx.com/api/browse?_search={query}"

        try:
            r = requests.get(search_url, headers=headers)
            data = r.json()
            product = data['Products'][0]
            market_price = float(product['market']['lowestAsk']) if product['market']['lowestAsk'] else 0
            net_profit = round(market_price * 0.9 - item['price'], 2)

            results.append({
                "product": item['name'],
                "bulkory_price": item['price'],
                "stockx_price": market_price,
                "profit": net_profit
            })

        except Exception as e:
            results.append({
                "product": item['name'],
                "error": str(e)
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run()
