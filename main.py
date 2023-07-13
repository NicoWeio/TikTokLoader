#!/usr/bin/env python3
import subprocess
from pathlib import Path

import click
from bs4 import BeautifulSoup
from selenium import webdriver


def get_video_urls(username):
    driver = webdriver.Firefox()
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
# @click.option("--username", prompt="TikTok username", help="The TikTok username to download")
@click.argument("username")
def download_user(username):
    video_urls = get_video_urls(username)
    print(f"Found {len(video_urls)} videos for {username}")
    user_subdir = Path(username)
    user_subdir.mkdir(exist_ok=True)
    for video_url in video_urls:
        subprocess.run(
            [
                'yt-dlp',
                video_url
            ],
            cwd=user_subdir,
        )


if __name__ == "__main__":
    download_user()
