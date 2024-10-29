import os
from google.cloud import firestore

# Firestoreクライアントの作成
db = firestore.Client(project=os.environ['PROJECT_ID'])

# 特定の個人が今まで飲んできたお酒を表示する関数
def display_alcohol_history_for_person(person_name):
    # 指定された名前のドキュメントを取得
    person_ref = db.collection('drinking_records').document(person_name)
    doc = person_ref.get()

    if doc.exists:
        data = doc.to_dict()
        alcohol_name_list = data.get('alcohol_name_list', [])  # 飲んだお酒のリストを取得
        print(f"名前: {person_name}, 飲んだお酒: {', '.join(alcohol_name_list) if alcohol_name_list else '記録なし'}")
        
    else:
        print(f"名前 '{person_name}' の飲酒履歴は見つかりませんでした。")

# 名前を入力して飲酒履歴を表示
person_name = input("履歴を確認したい人の名前を入力してください: ")
display_alcohol_history_for_person(person_name)