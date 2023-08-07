#!/usr/bin/env python3
import subprocess
from pathlib import Path

import click
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track
from selenium import webdriver
from time import sleep

console = Console()


def get_video_urls(driver, username, reload_page=True):
    if reload_page:  # can be false for CAPTCHA retries
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


def get_video_urls_retry(driver, username):
    video_urls = get_video_urls(driver, username)
    if not video_urls:
        console.print(f"No videos found for {username}. Maybe you need to solve a CAPTCHA?", style="red")
    while not video_urls:
        with console.status(f"Monitoring page for changes…", spinner="dots"):
            video_urls = get_video_urls(driver, username, reload_page=False)
            sleep(1)  # can be fast, because this causes no interaction with the site

    return video_urls


@click.command()
@click.argument("usernames", nargs=-1)
def download_user(usernames):
    with webdriver.Firefox() as driver:
        for username in usernames:
            video_urls = get_video_urls_retry(driver, username)
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
