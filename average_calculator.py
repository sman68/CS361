from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import statistics

app = Flask(__name__)

def parse_data(data):
    """ Parses the input data and returns a list of values. """
    return [entry['value'] for entry in data]

@app.route('/average/daily', methods=['POST'])
def calculate_daily_average():
    data = request.get_json()  # Get data from request body
    if not data or 'data' not in data:
        return jsonify({'error': 'No data provided'}), 400

    values = [item['value'] for item in data['data']]  # Assuming 'data' is a list of dictionaries with a 'value' key
    if not values:
        return jsonify({'error': 'No values provided'}), 400

    try:
        daily_average = statistics.mean(values)
        return jsonify({'average': daily_average}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/average/weekly', methods=['POST'])
def calculate_weekly_average():
    data = request.json
    values = parse_data(data)
    if values:
        weekly_average = statistics.mean(values)
        return jsonify({'average': weekly_average}), 200
    else:
        return jsonify({'error': 'No data provided'}), 400

@app.route('/average/monthly', methods=['POST'])
def calculate_monthly_average():
    data = request.json
    values = parse_data(data)
    if values:
        monthly_average = statistics.mean(values)
        return jsonify({'average': monthly_average}), 200
    else:
        return jsonify({'error': 'No data provided'}), 400

if __name__ == '__main__':
    app.run(debug=True)