# Plex-Auto-Stream-Swap

A Plex Script I wrote to update an entire season's audio/subtitle settings, without having to leave plex.

This works by constantly polling active plex sessions using the `plexapi` module.

As you watch shows on plex, the script caches what media that active clients are watching. This includes information like the selected Audio and Subtitle streams.

If your audio/subtitle stream has changed since the last update, but you're still watching the same episode, the script will attempt to update the entire season.


# Setup & Installation
Make sure you have Python 3 installed before continuing.

1. Clone this repository using `git clone`.
2. Modify `config.ini` to match your setup.
    - It's recommended to keep the script locally on your plex server. The script executes much faster.
    - For help with finding your plex token, visit [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)
3. Run `pip install -r requirements.txt` to install the required modules. You can do this in a [virtual environment](https://docs.python.org/3/tutorial/venv.html) as well.
4. Run `app.py`. Having the script run at startup is ideal, but I haven't tried that just yet.

## Docker Setup & Installation (Optional)
If you want to run this within a docker container, it's pretty straightforward.

1. Clone this repository using `git clone`.
2. Modify `config.ini` to match your setup. Leave the Plex API Token field as-is if you want to use environment variables.
    - It's recommended to keep the script locally on your plex server. The script executes much faster.
    - In the case of docker for Windows, you can use `host.docker.internal` as your plex host.
    - For help with finding your plex token, visit [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)
3. Build the docker image using `docker build -t screwage/plex-scripts:auto-stream-swap .`
4. Start up and run the container using `docker container run -d -e PLEX_API_TOKEN=<PLEX_TOKEN_HERE> --restart always --name plex-stream-swap screwage/plex-scripts:auto-stream-swap`

# TODO
- Clean up stale sessions
- Add support for multiple plex tokens
- Research ways to perform similar functionality without requiring tokens from each user
- Add logging to file
- Improve logging to include client identifier
- Rename this project to... literally anything else
- Check that the sessions picked up belong to the current user
