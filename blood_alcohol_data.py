import os
from google.cloud import firestore

# Firestoreクライアントの作成
db = firestore.Client(project=os.environ['PROJECT_ID'])

# 各参加者のblood_alcohol_levelを表示する関数
def display_blood_alcohol_levels():
    participants_ref = db.collection('drinking_records')
    docs = participants_ref.stream()  # コレクション内の全ドキュメントを取得

    print("各参加者の血中アルコール濃度:")
    for doc in docs:
        data = doc.to_dict()
        name = doc.id  # ドキュメントIDを名前として使用
        blood_alcohol_level = data.get('blood_alcohol_level', 0)  # blood_alcohol_levelフィールドを取得
        evaluation = evaluate_blood_alcohol(blood_alcohol_level)  # 評価を取得
        print(f"名前: {name}, 血中アルコール濃度: {blood_alcohol_level}, 評価: {evaluation}")

# 血中アルコール濃度の評価関数
def evaluate_blood_alcohol(blood_alcohol_level):
    # パーセンテージ形式で基準を比較
    if 0 <= blood_alcohol_level <= 20:
        return "いっぱい飲むぞ～"

    elif 20 < blood_alcohol_level <= 40:
        return "まだまだ飲める！"
    
    elif 40 < blood_alcohol_level <= 100:
        return "少し酔ってきたなかな～"
    
    elif 100 < blood_alcohol_level <= 150:
        return "よっ払いの仲間入り"
    
    elif 150 < blood_alcohol_level <= 300:
        return "明日早いならもうやめておいた方が…"
    
    elif 300 < blood_alcohol_level <= 400:
        return "べろべろだ～"
    
    elif blood_alcohol_level > 400:
        return "もう飲んじゃダメ！救急車呼んで！"

# 各参加者の血中アルコール濃度と評価を表示
display_blood_alcohol_levels()