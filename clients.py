from models import ClientMediaInfo
from plex_accessor import get_media_templates, update_season


# A dictionary of active clients. Maps a client ID to class ClientMediaInfo.
clients = dict()


# Updates current episode and audio/subtitle settings for the cached client.
def update_client(client, rating_key, episode, season=None):
    global clients

    if not season:
        season = episode.season()

    audio_template, subtitle_template = get_media_templates(episode)
    client_info = ClientMediaInfo(
        rating_key, season, audio_template, subtitle_template)
    clients[client] = client_info


# Check if the client information is up to date.
# If audio/subtitles have changed since last check,
# update the cached client and update the entire season to match.
def check_client(client, rating_key, episode):
    global clients

    season = episode.season()
    client_info = clients[client]
    audio_template, subtitle_template = get_media_templates(episode)

    if client_info.rating_key == rating_key:
        if client_info.audio_template == audio_template and client_info.subtitle_template == subtitle_template:
            # Nothing to change
            return
        # Need to update all in season
        update_audio = client_info.audio_template != audio_template
        update_subtitles = client_info.subtitle_template != subtitle_template

        reset_subtitles = subtitle_template is None

        update_client(client, rating_key, episode, season)
        update_season(season, update_audio, update_subtitles,
                      audio_template, subtitle_template, reset_subtitles)

    else:
        # Now watching a different episode/show. Update cached client to match
        update_client(client, rating_key, episode, season)
