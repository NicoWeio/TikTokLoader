#!/usr/bin/env python3
import functools
import subprocess
from pathlib import Path
from time import sleep

import click
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import track
from selenium import webdriver

console = Console()


def _get_driver():
    """Returns a web driver and makes it play nicely with interrupt signals"""
    subprocess_Popen = subprocess.Popen
    subprocess.Popen = functools.partial(subprocess_Popen, process_group=0)
    driver = webdriver.Firefox()
    subprocess.Popen = subprocess_Popen  # undo the monkey patch
    return driver


def get_video_urls(driver, username, reload_page=True):
    if reload_page:  # can be false for CAPTCHA retries
        driver.get(f"https://www.tiktok.com/@{username}")

    # read the HTML into BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # check for existence
    # assert not any("Dieses Konto konnte nicht gefunden werden" in str(e) for e in soup.find_all(class_="emuynwa1")), f"User {username} not found"
    assert "Dieses Konto konnte nicht gefunden werden" not in soup.text, f"User {username} not found"

    # check for "definitely no videos available"
    # NOTE: We do this because we would otherwise wait for the user to solve a CAPTCHA – which does not exist in this case
    assert "Dieser Benutzer hat keine Videos veröffentlicht." not in soup.text, f"User {username} has no videos"

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
        with console.status(f"Monitoring page for changes (Ctrl+C to skip)…", spinner="dots"):
            while not video_urls:
                try:
                    video_urls = get_video_urls(driver, username, reload_page=False)
                    sleep(1)  # can be fast, because this causes no interaction with the site
                except KeyboardInterrupt:
                    raise Exception("Monitoring interrupted by user.")

    return video_urls


@click.command()
@click.argument("usernames", nargs=-1)
@click.option("--auto-discover", "-a", is_flag=True, help="Automatically discover users from the current directory")
def download_user(usernames, auto_discover):
    if auto_discover:
        assert not usernames, "Cannot use --auto-discover and specify usernames at the same time"
        usernames = [
            path.name
            for path in Path(".").iterdir()
            if (
                path.is_dir() and
                any(path.glob("*.mp4"))
            )
        ]
        console.print(f"Discovered {len(usernames)} users: {usernames}", style="green")

    with _get_driver() as driver:
        for username in usernames:
            try:
                video_urls = get_video_urls_retry(driver, username)
                print(f"Found {len(video_urls)} videos for {username}")
            except Exception as e:
                console.print(f"Could not download {username}: {e}", style="red")
                continue

            count_including_downloaded = len(video_urls)
            # TODO: This might not be 100% reliable as it does not check the file format etc.
            video_urls = [
                url
                for url in video_urls
                if not any(
                    f"[{url.split('/')[-1]}]" in str(f)
                    for f in Path(username).iterdir()
                )
            ]
            count = len(video_urls)
            if count != count_including_downloaded:
                console.print(f"Skipping {count_including_downloaded - count} already downloaded videos", style="yellow")

            user_subdir = Path(username)
            user_subdir.mkdir(exist_ok=True)
            for video_url in track(video_urls, description="Downloading videos", auto_refresh=False):
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
