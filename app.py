from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from bs4 import BeautifulSoup
import joblib

from dataset.features_extraction import FeaturesExtraction

app = Flask(__name__)
CORS(app)

MODEL_PATH = 'Model/model.pkl'
model = joblib.load(MODEL_PATH)

# Initialize a cache dictionary
cache = {}


def initialize_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=options)


@app.route('/check_url', methods=['POST'])
def check_url():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    # Check if the URL is already in the cache
    if url in cache:
        if cache[url]['is_phishing'] == None:
            return jsonify({
                'url': url,
                'error': "Please wait for a moment!",
                'is_phishing': True,  # Conservative approach on error
                'confidence': 1.0
            })

        return jsonify({
            'url': url,
            'is_phishing': cache[url]['is_phishing'],
            'confidence': cache[url]['confidence']
        })

    # Immediately store a placeholder in cache to prevent duplicate processing
    cache[url] = {'is_phishing': None, 'confidence': None}

    try:
        result = check_if_phishing(url)
        # Update the cache with actual results
        cache[url] = result
        return jsonify({
            'url': url,
            'is_phishing': result['is_phishing'],
            'confidence': result['confidence']
        })
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        # Update the cache with an error state to prevent re-processing
        cache[url] = {'is_phishing': True, 'confidence': 1.0}
        return jsonify({
            'url': url,
            'error': str(e),
            'is_phishing': True,  # Conservative approach on error
            'confidence': 1.0
        })


def check_if_phishing(url):
    driver = None
    try:
        driver = initialize_driver()
        driver.get(url)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        feature_extractor = FeaturesExtraction(driver, soup, url)

        features = feature_extractor.create_vector()

        prediction = model.predict([features])[0]

        probability = model.predict_proba([features])[0]

        confidence = probability[1] if prediction == 1 else probability[0]

        return {'is_phishing': bool(prediction), 'confidence': float(confidence)}

    except Exception as e:
        raise e

    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    app.run(debug=True)
