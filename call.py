import os
from google.cloud import firestore
from playsound import playsound

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


# 血中アルコール濃度の差が50mg/dl以上の参加者をチェック
def check_blood_alcohol_difference():
    blood_alcohol_levels = get_blood_alcohol_levels()

    print(blood_alcohol_levels)
    
    if not blood_alcohol_levels:  # データが空の場合のチェック
        print("データが見つかりませんでした。")
        return

    participants = list(blood_alcohol_levels.items())  # (name, blood_alcohol_level) のリスト

    for i in range(len(participants)):
        for j in range(i + 1, len(participants)):
            name1, level1 = participants[i]
            name2, level2 = participants[j]

            # 血中アルコール濃度の差をチェック
            if abs(level1 - level2) >= 50:
                print(f"{name1}さんと{name2}さんの血中アルコール濃度の差が50mg/dl以上です！")
                # 50mg/dl以上の差があった場合、音声を再生
                playsound('alert_sound.mp3')  # 'alert_sound.mp3'を適切な音声ファイルに変更
                return  # 1つの差を見つけたら終了（すべての組み合わせを確認したい場合はこの行を削除）

# 各参加者の血中アルコール濃度と評価を表示
check_blood_alcohol_difference()