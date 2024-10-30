import os
from google.cloud import firestore

db = firestore.Client(project=os.environ['PROJECT_ID'])

#名前を入力するところ

# 飲み会に参加しているユーザーと性別を追加する関数
def add_user_to_drinking_record(user_name, gender):
    # 'drinking_records' コレクション内にユーザーごとのドキュメントを作成
    user_ref = db.collection('drinking_records').document(user_name)
    
    # 性別を 'gender' フィールドとして格納
    user_ref.set({
        'gender': gender,
        'blood_alcohol_level': 0,  # 初期値を0に設定
        'alcohol_name_list':[]
    })
    print(f"ユーザー '{user_name}' の性別 '{gender}' が 'drinking_records' コレクションに保存されました。")

# ユーザーの情報を保存

user_name=input("参加する人の名前を入力してください:")
user_gender=input("性別を選んでください(男or女):")


if user_gender =="男":
    gender=0

elif user_gender =="女":
    gender=1

else:
    print("入力した内容がおかしいです")
    exit()

add_user_to_drinking_record(user_name,gender)

#参加している人の名前と性別を表示

def display_participants():
    participants_ref = db.collection('drinking_records')
    docs = participants_ref.stream()  # コレクション内の全ドキュメントを取得

    print("飲み会に参加している人のリスト:")
    for doc in docs:
        data = doc.to_dict()
        name = doc.id  # ドキュメントIDを名前として使用
        gender = data.get('gender', '不明')  # genderフィールドを取得
        print(f"名前: {name}, 性別: {gender}")

# 実行例: 参加者リストを表示
display_participants()