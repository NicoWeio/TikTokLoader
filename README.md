> [!WARNING]
> This uses a very basic approach. It waits for the user to solve captchas and doesn't try to scroll to load more videos. If run regularly, that shouldn't be a problem, though.

# What is this?
Using _selenium_ (i. e. web scraping) and _yt-dlp_, this script semi-automatically downloads ~~all~~ some videos of a given list of TikTok users.
Born out of frustration, it is inspired by [Instaloader](https://github.com/instaloader/instaloader/) and should more or less match its basic functionality for TikTok. A tiny project created out of frustration.

# Setup and usage
- `pip install -r requirements.txt` (but you probably don't need these specific versions)
- `/path/to/main.py username1 username2 ...` will download the videos of the given users into subdirectories named after their usernames

# Why not X?
- https://github.com/davidteather/TikTok-Api
  - requires playwright, which complains about missing dependencies on my (Arch) system (and I don't want to `playwright install-deps` with superuser privileges)
- https://github.com/drawrowfly/tiktok-scraper
  - [broken: does not find any videos](https://github.com/drawrowfly/tiktok-scraper/issues/799)

# Todo
- Nicer output / integration with yt-dlp via its Python API
