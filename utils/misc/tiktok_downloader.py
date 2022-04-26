import requests
import re
import asyncio
import aiohttp




async def download_tiktok(user_id, link):
    agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    }
    LINKS = re.compile("playAddr\":\"(.*?)\"")
    COOKIES = {}

    vid_page = requests.get(link, headers=agent, cookies=COOKIES)
    if not COOKIES:
        COOKIES = vid_page.cookies
        vid_page = requests.get(link, headers=agent, cookies=COOKIES)

    links = LINKS.findall(vid_page.text)
    if not links:
        return False
    download_link = links[0].encode().decode('unicode-escape')

    async with aiohttp.ClientSession() as session:
        async with session.get(download_link, headers={'Referer': link}, cookies=COOKIES, allow_redirects=True) as get_video:
            with open(f'media/videos/{user_id}.mp4', "wb") as file_to_save:
                file_content = await get_video.content.read()
                file_to_save.write(file_content)
    # vid_file = requests.get(download_link, headers={'Referer': link}, cookies=COOKIES)
    # with open(f'media/videos/{user_id}.mp4', 'wb') as f:
    #     f.write(vid_file.content)

    return f'media/videos/{user_id}.mp4'
