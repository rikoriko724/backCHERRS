import os
from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from dotenv import load_dotenv

# 環境変数のロード
load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Gemini APIエンドポイントとAPIキー
#API_KEYに自分のAPI KEYを入力
GEMINI_API_KEY = os.getenv('API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # 画像をGemini APIに送信して認識結果を取得
        with open(filepath, 'rb') as image_file:
            headers = {
                'Authorization': f'Bearer {GEMINI_API_KEY}'
            }
            files = {'file': image_file}
            response = requests.post(GEMINI_API_URL, headers=headers, files=files)

        if response.status_code == 200:
            recognition_result = response.json()
            alcohol_info = extract_alcohol_info(recognition_result)
            return render_template('result.html', result=alcohol_info, image_url=filepath)
        else:
            flash('Error with API: ' + response.text)
            return redirect(url_for('index'))

def extract_alcohol_info(api_response):
    """
    Gemini APIの結果からアルコールの種類、容量、アルコール濃度を抽出する
    """
    # ここでAPIレスポンスから必要な情報を抽出する
    # 仮の例として以下を使用：
    alcohol_type = api_response.get('alcohol_type', 'Not found')
    volume = api_response.get('volume', 'Not found')
    alcohol_content = api_response.get('alcohol_content', 'Not found')

    return {
        'type': alcohol_type,
        'volume': volume,
        'alcohol_content': alcohol_content
    }

if __name__ == "__main__":
    app.run(debug=True)
