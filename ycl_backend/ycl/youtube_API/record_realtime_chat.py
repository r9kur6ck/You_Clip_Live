import time
import requests
import json
from pathlib import Path
import environ
from datetime import datetime
from dateutil import parser

#事前に取得したYouTube API key
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(Path(BASE_DIR, ".env"))

YT_API_KEY = env("YOUTUBE_API_KEY")


def get_chat_id(yt_url):
    '''
    https://developers.google.com/youtube/v3/docs/videos/list?hl=ja
    '''
    video_id = yt_url.replace('https://www.youtube.com/watch?v=', '')
    print('video_id : ', video_id)

    url    = 'https://www.googleapis.com/youtube/v3/videos'
    params = {'key': YT_API_KEY, 'id': video_id, 'part': 'liveStreamingDetails'}
    data   = requests.get(url, params=params).json()

    liveStreamingDetails = data['items'][0]['liveStreamingDetails']
    if 'activeLiveChatId' in liveStreamingDetails.keys():
        chat_id = liveStreamingDetails['activeLiveChatId']
        print('get_chat_id done!')
    else:
        chat_id = None
        print('NOT live')

    return chat_id


def get_chat(chat_id, pageToken, log_file, clips, clip_word):
    '''
    https://developers.google.com/youtube/v3/live/docs/liveChatMessages/list
    '''
    url    = 'https://www.googleapis.com/youtube/v3/liveChat/messages'
    params = {'key': YT_API_KEY, 'liveChatId': chat_id, 'part': 'id,snippet,authorDetails'}
    if type(pageToken) == str:
        params['pageToken'] = pageToken

    data   = requests.get(url, params=params).json()

    try:
        count_with_clip_word = sum(1 for d in data['items'] if clip_word in d['snippet']['displayMessage'])
        comment_len = len(data['items'])

        if count_with_clip_word >= 0.1 * comment_len:
            start = parser.isoparse(data['items'][0]['snippet']['publishedAt'])
            end = parser.isoparse(data['items'][-1]['snippet']['publishedAt'])

            clips.append({"start": start, "end": end, "word": clip_word})
        
        for item in data['items']:
            channelId = item['snippet']['authorChannelId']
            msg       = item['snippet']['displayMessage']
            usr       = item['authorDetails']['displayName']
            #supChat   = item['snippet']['superChatDetails']
            #supStic   = item['snippet']['superStickerDetails']
            log_text  = '[by {}  https://www.youtube.com/channel/{}]\n  {}'.format(usr, channelId, msg)
            with open(log_file, 'a') as f:
                print(log_text, file=f)
                print(log_text)
        with open(log_file, 'a') as f:
            print('start : ', data['items'][0]['snippet']['publishedAt'], file=f)
            print('end   : ', data['items'][-1]['snippet']['publishedAt'], file=f)
            print('start : ', data['items'][0]['snippet']['publishedAt'])
            print('end   : ', data['items'][-1]['snippet']['publishedAt'])

    except:
        pass

    return data['nextPageToken']


def clip_process(yt_url, clips, clip_word):
    slp_time        = 10 #sec
    iter_times      = 10 #回
    take_time       = slp_time / 60 * iter_times
    print('{}分後　終了予定'.format(take_time))
    print('work on {}'.format(yt_url))

    log_file = yt_url.replace('https://www.youtube.com/watch?v=', '') + '.txt'
    with open(log_file, 'a') as f:
        print('{} のチャット欄を記録します。'.format(yt_url), file=f)
    chat_id = get_chat_id(yt_url)

    nextPageToken = None
    for ii in range(iter_times):
        #for jj in [0]:
        try:
            print('\n')
            nextPageToken = get_chat(chat_id, nextPageToken, log_file, clips, clip_word)
            time.sleep(slp_time)
        except:
            break

def main():
    url = "https://www.youtube.com/watch?v=aXAsMcmtJTc" # アザラシのやつ
    clip_word = "ナイス"
    clips = []
    clip_process(url, clips, clip_word)
    with open("clips.txt", 'a') as f:
        for clip in clips:
            print(clip, file=f)

if __name__ == "__main__":
    main()