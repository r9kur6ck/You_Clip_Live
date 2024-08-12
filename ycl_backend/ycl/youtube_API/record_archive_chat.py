import requests
from pathlib import Path
import environ

#事前に取得したYouTube API key
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(Path(BASE_DIR, ".env"))

URL = "https://www.youtube.com/watch?v=eLLcIVTxiG8"

# YouTube Data APIキーとビデオIDを設定
API_KEY = env("YOUTUBE_API_KEY")
VIDEO_ID = URL.replace('https://www.youtube.com/watch?v=', '')

# ビデオの詳細を取得するAPIエンドポイント
video_url = f"https://www.googleapis.com/youtube/v3/videos?id={VIDEO_ID}&part=liveStreamingDetails&key={API_KEY}"
video_response = requests.get(video_url)
video_data = video_response.json()

# ビデオの終了時間を取得
end_time = None
if 'items' in video_data and len(video_data['items']) > 0:
    live_details = video_data['items'][0].get('liveStreamingDetails', {})
    end_time = live_details.get('actualEndTime', None)

# コメントを取得するAPIエンドポイント
comment_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={VIDEO_ID}&key={API_KEY}"

# テキストファイルに書き込む
with open('chat_comments.txt', 'w', encoding='utf-8') as file:
    # 終了時間の書き込み
    if end_time:
        file.write(f"ライブ配信の終了時間: {end_time}\n")
    else:
        file.write("ライブ配信の終了時間が取得できませんでした。\n")

    # コメントの取得と書き込み
    while True:
        comment_response = requests.get(comment_url)
        comment_data = comment_response.json()

        if 'items' in comment_data:
            for item in comment_data['items']:
                snippet = item['snippet']
                top_level_comment = snippet['topLevelComment']['snippet']
                comment_text = top_level_comment['textDisplay']
                comment_time = top_level_comment['publishedAt']

                # 書き込みフォーマット
                file.write(f"コメント: {comment_text}\n")
                file.write(f"送信時間: {comment_time}\n")
                file.write('-' * 40 + '\n')

        if 'nextPageToken' in comment_data:
            comment_url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={VIDEO_ID}&key={API_KEY}&pageToken={comment_data['nextPageToken']}"
        else:
            break

print("コメントと終了時間がテキストファイルに書き込まれました。")
