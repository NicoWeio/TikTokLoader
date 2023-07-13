> **Warning**
> This is a very basic approach. It doesn't solve captchas and thus will probably not download all the videos of a user. If run regularly, that shouldn't be a problem, though.


# Setup and usage
- `pip install -r requirements.txt` (but you probably don't need these specific versions)
- `/path/to/main.py username1 username2 ...` will download the videos of the given users into subdirectories named after their usernames

# Why not X?
- https://github.com/davidteather/TikTok-Api
  - requires playwright, which complains about missing dependencies on my (Arch) system (and I don't want to `playwright install-deps` with superuser privileges)
- https://github.com/drawrowfly/tiktok-scraper
  - [broken: does not find any videos](https://github.com/drawrowfly/tiktok-scraper/issues/799)

# Todo
- Copy Instaloader's `--fast-update` option: Stop downloading a user's videos once we encounter one we've already downloaded before.
- Nicer output / integration with yt-dlp via its Python API
