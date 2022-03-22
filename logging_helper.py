import logging
from plexapi.media import AudioStream
from plexapi.media import SubtitleStream


def episode_to_str(episode):
    """ Returns a string representation of an episode in the following format:
        "SXXEXX - Title"
        Parameters:
            episode(:class:`plexapi.video.Episode`): The episode that will be
                represented with a string.
    """
    return "%s - %s" % (episode.seasonEpisode.upper(), episode.title)


def log_substitle_reset_success(episode):
    logging.info("Reset subtitle for '%s'" % episode_to_str(episode))


def log_success(episode, new_stream):
    """ Prints stream set successfully.
        Parameters:
            episode(:class:`~plexapi.video.Episode`): Episode in which audio
                was set.
            newStream(:class:`~plexapi.media.AudioStream`): The AudioStream
                that was applied.
    """
    if new_stream.title:
        descriptor = "'%s' " % new_stream.title
    elif new_stream.language:
        descriptor = "'%s' " % new_stream.languageCode
    else:
        descriptor = ""
    if isinstance(new_stream, AudioStream):
        stream_type = "audio"
    elif isinstance(new_stream, SubtitleStream):
        stream_type = "subtitle"
    logging.info("Set %s %sfor '%s'" % (
        stream_type, descriptor, episode_to_str(episode)))
