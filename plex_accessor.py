import logging

from matcher import match_audio, matchSubtitles
from logging_helper import episode_to_str, log_substitle_reset_success, log_success
from models import AudioStreamInfo, SubtitleStreamInfo


# Update Audio and Subtitles for an Entire Season
# Attempts to match the closest audio/subtitle given an AudioStreamInfo or SubtitleStreamInfo template
def update_season(season, update_audio, update_subtitle, audio_template=None, subtitle_template=None, reset_subtitles=False):
    logging.info(
        f"Attempting to update season: {season.show().title} - {season.title}")
    for episode in season.episodes():
        episode.reload()

        for part in episode.media[0].parts:
            if update_audio:
                new_audio = match_audio(part, audio_template)

                if new_audio:
                    part.setDefaultAudioStream(new_audio)

                    log_success(episode=episode, new_stream=new_audio)
                else:
                    logging.info("No Audio matches found for '%s'" %
                                 episode_to_str(episode))

            if update_subtitle:
                if reset_subtitles:
                    part.resetDefaultSubtitleStream()
                    log_substitle_reset_success(episode=episode)
                    continue

                new_subtitle = matchSubtitles(part, subtitle_template)

                if new_subtitle:
                    part.setDefaultSubtitleStream(new_subtitle)

                    log_success(episode=episode, new_stream=new_subtitle)
                else:
                    logging.info("No subtitle matches found for '%s'" %
                                 episode_to_str(episode))


# Get the currently set AudioStreamInfo and SubtitleStreamInfo from some episode.
# Returned subtitle_stream will be None if no subtitles are chosen.
def get_media_templates(episode):
    episode.reload()
    episode_part = episode.media[0].parts[0]
    audio_streams = episode_part.audioStreams()
    subtitle_streams = episode_part.subtitleStreams()

    selected_audio_stream = next(
        (stream for stream in audio_streams if stream.selected), None)
    selected_subtitle_stream = next(
        (stream for stream in subtitle_streams if stream.selected), None)

    audio_template = AudioStreamInfo(
        selected_audio_stream, selected_audio_stream.index)

    if selected_subtitle_stream is None:
        subtitle_template = None
    else:
        subtitle_template = SubtitleStreamInfo(
            selected_subtitle_stream, selected_subtitle_stream.index,
            selected_subtitle_stream.index - len(audio_streams))

    return audio_template, subtitle_template