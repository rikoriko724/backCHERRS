import os
from google.cloud import firestore
from PIL import Image

# Firestoreクライアントの作成
db = firestore.Client(project=os.environ['PROJECT_ID'])

# すべての参加者の血中アルコール濃度を取得する関数
def get_blood_alcohol_levels():
    participants_ref = db.collection('drinking_records')
    docs = participants_ref.stream()  # コレクション内の全ドキュメントを取得

    blood_alcohol_dict = {}  # 名前と血中アルコール濃度の辞書

    print("各参加者の血中アルコール濃度:")
    for doc in docs:
        data = doc.to_dict()
        name = doc.id  # ドキュメントIDを名前として使用
        blood_alcohol_level = data.get('blood_alcohol_level', 0)  # blood_alcohol_levelフィールドを取得
        print(f"名前: {name}, 血中アルコール濃度: {blood_alcohol_level}")

        # 名前と血中アルコール濃度の辞書を作成
        blood_alcohol_dict[name] = blood_alcohol_level

    return blood_alcohol_dict

# 血中アルコール濃度に基づいてジョッキを表示する関数
def display_beer_mugs(blood_alcohol_level, name):
    # 血中アルコール濃度から表示するジョッキ数を計算
    num_mugs = int(blood_alcohol_level // 5)

    # ジョッキ画像の読み込み
    mug_image = Image.open('images\empty.png')

    print(f"{num_mugs}")
    
    # ジョッキの表示
    for _ in range(num_mugs):
        mug_image.show()

# 各参加者の血中アルコール濃度に応じてジョッキ画像を表示
blood_alcohol_dict = get_blood_alcohol_levels()
for name, blood_alcohol_level in blood_alcohol_dict.items():
    display_beer_mugs(blood_alcohol_level, name)