import aiohttp
import requests
from bs4 import BeautifulSoup as bs


async def instagram_downloader(user_id, link):
    agent = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }
    main_url = "https://instagrabber.ru/"
    if len(link.split("/")[4]) == 11:
        r = requests.get(main_url + link.split("/")[4], headers=agent)
        soup = bs(r.content, 'html.parser')
        down_btn = soup.find('a', class_='download_link btn btn-default')
        if down_btn.text.split(" ")[-1].lower() == "видео":
            async with aiohttp.ClientSession() as session:
                async with session.get(down_btn['href'], allow_redirects=True) as get_video:
                    with open(f'media/videos/{user_id}.mp4', "wb") as file_to_save:
                        file_content = await get_video.content.read()
                        file_to_save.write(file_content)

            # d = requests.get(down_btn['href'], stream=True)
            # with open(f"media/videos/{user_id}.mp4", "wb") as f:
            #     f.write(d.content)
                    return f"media/videos/{user_id}.mp4"
        else:
            return 'false'
    else:
        return 'false'