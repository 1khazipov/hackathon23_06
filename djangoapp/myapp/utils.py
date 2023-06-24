import yt_dlp
import pytube
import asyncio
import os.path
import re
from .Exceptions.exceptions import ResourceUnavailableException
from .tasks import ml_pipeline

class MLPipeLineService:
    async def register_computation_task_async(self, url, id) -> bool:
        #computed = cache.get(id)
        #if computed:

        #todo: начинать бэкграунд обработку или говорить, что в кжше уже есть данные.
        ml_pipeline.delay()
        return False


async def download_youtube_video_async(url, destination):
    loop = asyncio.get_event_loop()

    #todo: convert to lambda
    def do_async():
        return pytube.YouTube(url)
    youtube = await loop.run_in_executor(None, do_async)
    details = youtube.vid_info['videoDetails']
    if youtube.vid_info['playabilityStatus']['status'] != 'OK' or details['isPrivate']:
        raise ResourceUnavailableException()

    id = details['videoId'] #or video.download().video_id
    title = details['title']
    destination = os.path.join(destination, id)
    if not os.path.exists(destination):
        #todo: среднее качесвто 720 или 1080 на выбор
        video = youtube.streams.filter(progressive=True, file_extension='mp4', resolution='720p')\
                           .order_by('resolution').first()
        if not video:
            raise ResourceUnavailableException()

        def download_async():
            return video.download(destination)
        await loop.run_in_executor(None, download_async)

    return {
        'id': id,
        'title': title,
        'link': url,
        'directory': destination+id
    }

async def download_youtube_video_async(url, video_id, destination):
    loop = asyncio.get_event_loop()

    # todo: convert to lambda
    def do_async():
        return pytube.YouTube(url)

    #youtube = await loop.run_in_executor(None, do_async)
    #details = youtube.vid_info['videoDetails']
    details = {'videoId':video_id, 'title': "ffff"}
    #if details['isLiveContent'] or details['isPrivate']:
    #    raise ResourceUnavailableException()
    #pytube.cipher.get_throttling_function_name =
    id = details['videoId']  # or video.download().video_id
    title = details['title']
    destination = os.path.join(destination, f'{id}.mp4')
    if not os.path.exists(destination):
        # todo: среднее качесвто 720 или 1080 на выбор
        #video = youtube.streams.filter(progressive=True, file_extension='mp4', resolution='720p') \
        #    .order_by('resolution').first()
        #if not video:
        #    raise ResourceUnavailableException()

        def download_async():
            ydl_opts = {
                # 'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'format': 'best[ext=mp4]',
                'outtmpl': os.path.join(destination),
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

        await loop.run_in_executor(None, download_async)

    return {
        'id': id,
        'title': title,
        'link': url,
        'directory': destination + id
    }

def extract_video_id(url):
    if url is not None:
        regex = r"(?:https?:\/\/(?:www\.)?youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|https?:\/\/(?:www\.)?youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, url)
        if match:
            video_id = match.group(1)
            return video_id

    return None