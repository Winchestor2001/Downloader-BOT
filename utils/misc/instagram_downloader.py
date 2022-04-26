import json

import aiohttp
import requests
from bs4 import BeautifulSoup as bs


async def instagram_downloader(user_id, link):
    agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }
    main_url = "https://instadownloader.co/insta_downloader.php?url="+link
    try:
        r = requests.get(main_url)
        result = r.json()
        json_object = json.loads(result)
        if len(json_object["videos_links"]) != 0:
            down_url = json_object["videos_links"][0]["url"]
            async with aiohttp.ClientSession() as session:
                async with session.get(down_url, allow_redirects=True) as get_video:
                    with open(f'media/videos/{user_id}.mp4', "wb") as file_to_save:
                        file_content = await get_video.content.read()
                        file_to_save.write(file_content)


                    return f"media/videos/{user_id}.mp4"
        else:
            return 'false'

    except Exception:
        return 'false'
