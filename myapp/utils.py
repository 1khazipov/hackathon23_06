import pytube
import asyncio
from .Exceptions.exceptions import ResourceUnavailableException

def download_yotube_video(url, destination):
    youtube = pytube.YouTube(url)
    details = youtube.vid_info['videoDetails']
    if youtube.vid_info['playabilityStatus']['status'] != 'OK' or details['isPrivate']:
        raise ResourceUnavailableException()

    id = details['videoId']  # or video.download().video_id
    title = details['title']

    # todo: среднее качесвто 720 или 1080 на выбор
    video = youtube.streams.get_highest_resolution()
    video.download(destination)

    return {
        'id': id,
        'title': title,
        'directory': destination
    }


async def download_yotube_video_async(url, destination):
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

    #todo: среднее качесвто 720 или 1080 на выбор
    video = youtube.streams.get_highest_resolution()
    def download_async():
        return video.download(destination)
    await loop.run_in_executor(None, download_async)

    return {
        'id': id,
        'title': title,
        'directory': destination
    }