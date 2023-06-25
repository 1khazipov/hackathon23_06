import yt_dlp
import pytube
import asyncio
import os.path
from django.core.cache import cache
import re

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from .Exceptions.exceptions import ResourceUnavailableException
from .tasks import ml_pipeline

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip


def run(url, id, options):
    key = f'{id}_status'
    registered = cache.get(key)
    if registered and registered['status'] == 'pending':
        return

    cache.set(key, {'status': 'pending'})
    try:
        source = download_youtube_video(url, id, './Downloads')
        #trim_if_requested(source, options)
        ml_pipeline(source, id, options)
    except:
        cache.set(key, {'status': "failed"})

def trim_if_requested(source, options):
    duration = get_video_duration(source)
    start, stop = 0, duration
    if options.get('start') and 0<= options.get('start') < duration:
        start = options.get('start')
    if options.get('stop') and 0 < options.get('stop') <= duration and start <= stop:
        stop = options.get('stop')
    trim_video(source, start, stop, targetname=f'{source[:-4]}_{start}_{stop}.mp4')

def get_video_duration(video_path):
    video = VideoFileClip(video_path)
    duration = video.duration
    video.close()
    return duration

def trim_video(input_file, output_file, start_time_sec, end_time_sec):
    ffmpeg_extract_subclip(input_file, start_time_sec, end_time_sec, targetname=output_file)

def download_youtube_video(url, video_id, destination):
    destination = os.path.join(destination, f'{video_id}.mp4')

    if not os.path.exists(destination):
        ydl_opts = {
            'format': 'best[ext=mp4]',
            'outtmpl': destination,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    return destination

def extract_video_id(url):
    if url is not None:
        regex = r"(?:https?:\/\/(?:www\.)?youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/)|https?:\/\/(?:www\.)?youtu\.be\/)([a-zA-Z0-9_-]{11})"
        match = re.search(regex, url)
        if match:
            video_id = match.group(1)
            return video_id

    return None