import requests
from bs4 import BeautifulSoup
import json
import re

# 終了したライブアーカイブのURL
VIDEO_URL = 'https://www.youtube.com/watch?v=eLLcIVTxiG8'  # ここに終了したライブアーカイブのURLを入力

# YouTubeのリプレイページにアクセス
response = requests.get(VIDEO_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# コメントを含むスクリプトタグを抽出
script_tag = soup.find('script', string=lambda text: text and 'var ytInitialData =' in text)
if script_tag:
    # JSONデータを正しく抽出するために正規表現を使用
    json_text = re.search(r'var ytInitialData = ({.*?});', script_tag.string)
    if json_text:
        json_text = json_text.group(1)
        try:
            data = json.loads(json_text)
             # コメントを取得
            comments = []
            for item in data['contents']['twoColumnWatchNextResults']['results']['contents']:
                if 'videoPrimaryInfoRenderer' in item:
                    comments.append({
                        'text': item['videoPrimaryInfoRenderer']['videoOwner']['videoOwnerRenderer']['title']['runs'][0]['text'],
                        'time': item['videoPrimaryInfoRenderer']['videoOwner']['videoOwnerRenderer']['title']['runs'][0]['text']
                    })

            # コメントをテキストファイルに書き込む
            with open('replay_comments.txt', 'w', encoding='utf-8') as file:
                for comment in comments:
                    file.write(f"コメント: {comment['text']}\n")
                    file.write(f"時間: {comment['time']}\n")
                    file.write('-' * 40 + '\n')

            print("リプレイのコメントがテキストファイルに書き込まれました。")
        except json.JSONDecodeError as e:
            print(f"JSONデコードエラー: {e}")
    else:
        print("JSONデータが見つかりませんでした。")
else:
    print("スクリプトタグが見つかりませんでした。")
