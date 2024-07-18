from flask import Flask, request, jsonify
import requests
from PIL import Image
import base64
from io import BytesIO
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
api_key = os.getenv('API_KEY')


def get_nasa_apod(api_key, date):
    url = f"https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes
    data = response.json()
    return data


@app.route('/get_apod', methods=['POST'])
def get_apod():
    data = request.json
    if 'date' not in data:
        return jsonify({"error": "Date is required"}), 400

    date = data['date'].strip()

    try:
        apod_data = get_nasa_apod(api_key, date)
        if "url" in apod_data and "title" in apod_data:
            image_url = apod_data['url']
            event_name = apod_data['title']

            # Open the image from URL
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))

            # Convert image to base64
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Return response with event name and base64 encoded image
            return jsonify({
                "event_name": event_name,
                "image_data": img_str
            })
        else:
            return jsonify({"error": "No image or event found for this date."}), 404
    except requests.exceptions.HTTPError as err:
        return jsonify({"error": str(err)}), 500


if __name__ == "__main__":
    app.run(debug=True)
