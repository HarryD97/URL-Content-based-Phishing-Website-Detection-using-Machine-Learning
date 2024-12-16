from flask import Flask, request, jsonify
from flask_cors import CORS
from selenium import webdriver
from bs4 import BeautifulSoup
import joblib
from features_extraction import FeaturesExtraction

app = Flask(__name__)
CORS(app)

# 加载预训练模型
MODEL_PATH = 'model.pkl'
model = joblib.load(MODEL_PATH)


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

    try:
        result = check_if_phishing(url)
        return jsonify({
            'url': url,
            'is_phishing': result['is_phishing'],
            'confidence': result['confidence']
        })
    except Exception as e:
        return jsonify({
            'url': url,
            'error': str(e),
            'is_phishing': True,  # 发生错误时保守处理
            'confidence': 1.0
        })


def check_if_phishing(url):
    driver = None
    try:
        # 初始化WebDriver
        driver = initialize_driver()
        # 访问URL
        driver.get(url)
        # 获取页面源代码
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        # 提取特征
        feature_extractor = FeaturesExtraction(driver, soup, url)
        features = feature_extractor.create_vector()
        # 使用模型预测
        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0]

        confidence = probability[1] if prediction == 1 else probability[0]

        return {
            'is_phishing': bool(prediction),
            'confidence': float(confidence)
        }

    except Exception as e:
        raise e

    finally:
        if driver:
            driver.quit()


if __name__ == '__main__':
    app.run(debug=True)


