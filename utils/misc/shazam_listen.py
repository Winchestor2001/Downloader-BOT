import os
import sys

from shazamio import Shazam
import requests




async def workWithShazam(file_name):
    shazam = Shazam()
    result = []
    try:
        shazaming = await shazam.recognize_song(file_name)

        if  'track' in shazaming:
            title = shazaming['track']['title']
            subtitle = shazaming['track']['subtitle']
            result.append([title, subtitle])
        else:
            result.append('false')
            return result


        if 'actions' in shazaming['track']['hub']:
            audio_url = shazaming['track']['hub']['actions'][1]['uri']
            r = requests.get(audio_url, stream=True)
            # with open(f"media/songs/{b'title'} - {b'subtitle'}.mp3", mode='wb') as f:
            with open(f"media/songs/{title} - {subtitle}.mp3", mode='wb') as f:
                f.write(r.content)
            result.append(f"media/songs/{title} - {subtitle}.mp3")
            # result.append(f"media/songs/{b'title'} - {b'subtitle'}.mp3")

        else:
            result.append('false')



        if 'text' in shazaming['track']['sections'][1]:
            lyrics = shazaming['track']['sections'][1]['text']
            result.append(lyrics)
        else:
            result.append('false')
        # print(file_name)
        # os.unlink(rf"C:\Users\User\Desktop\MainFiles\ALL FILES\TELEGRAM BOTS\PoiskMuz BOT\{file_name}")
        return result
        # return [[title, subtitle], f"songs/{title} - {subtitle}.mp3", lyrics]
    except Exception as ex:
        print(ex)
        with open('errors.txt', 'a', encoding='utf-8') as f:
            f.write(f'{type(ex).__name__}: {ex} | Line: {sys.exc_info()[-1].tb_lineno}')
        result.clear()
