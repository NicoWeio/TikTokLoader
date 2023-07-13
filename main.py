#!/usr/bin/env python3
import subprocess
from pathlib import Path

import click
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track
from selenium import webdriver

console = Console()


def get_video_urls(driver, username):
    driver.get(f"https://www.tiktok.com/@{username}")

    # TODO: check for HTTP 404

    # read the html into BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # find the video links
    CLASS_NAME = "eih2qak0"

    video_links = [
        a['href']
        for a in soup.find_all('a', class_=CLASS_NAME)
        if a['href'].startswith(f"https://www.tiktok.com/@{username}/video/")
    ]
    return video_links


@click.command()
@click.argument("usernames", nargs=-1)
def download_user(usernames):
    with webdriver.Firefox() as driver:
        for username in usernames:
            video_urls = get_video_urls(driver, username)
            print(f"Found {len(video_urls)} videos for {username}")

            user_subdir = Path(username)
            user_subdir.mkdir(exist_ok=True)
            for video_url in track(video_urls, description="Downloading videos", auto_refresh=False):
                # print()
                subprocess.run(
                    [
                        'yt-dlp',
                        video_url
                    ],
                    cwd=user_subdir,
                )
                # TODO: break if the video is already downloaded


if __name__ == "__main__":
    download_user()
