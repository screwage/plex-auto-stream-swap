class ClientMediaInfo:
    def __init__(self, rating_key, season, audio_template, subtitle_template):
        self.rating_key = rating_key
        self.season = season
        self.audio_template = audio_template
        self.subtitle_template = subtitle_template


class AudioStreamInfo:
    """ Container class to hold info about an AudioStream
        Attributes:
            allStreamsIndex (int): Index of this
                :class:`~plexapi.media.AudioStream` in combined AudioStream +
                SubtitleStream list.
            audioChannelLayout (str): Audio channel layout (ex: 5.1(side)).
            audioStreamsIndex (int): Index of this
                :class:`~plexapi.media.AudioStream` in MediaPart.audioStreams()
            codec (str): Codec of the stream (ex: srt, ac3, mpeg4).
            languageCode (str): Ascii code for language (ex: eng, tha).
            title (str): Title of the audio stream.
    """

    def __init__(self, audioStream, audioStreamsIndex):
        # Initialize variables
        self.allStreamsIndex = audioStreamsIndex
        self.audioChannelLayout = audioStream.audioChannelLayout
        self.audioStreamsIndex = audioStreamsIndex
        self.codec = audioStream.codec
        self.languageCode = audioStream.languageCode
        self.title = audioStream.title

    def __eq__(self, other):
        return self.allStreamsIndex == other.allStreamsIndex \
            and self.audioChannelLayout == other.audioChannelLayout \
            and self.audioStreamsIndex == other.audioStreamsIndex \
            and self.codec == other.codec \
            and self.languageCode == other.languageCode \
            and self.title == other.title


class SubtitleStreamInfo:
    """ Container class to hold info about a SubtitleStream
        Attributes:
            allStreamsIndex (int): Index of this
                :class:`~plexapi.media.SubtitleStream` in combined AudioStream
                + SubtitleStream list.
            codec (str): Codec of the stream (ex: srt, ac3, mpeg4).
            forced (bool): True if stream is a forced subtitle.
            languageCode (str): Ascii code for language (ex: eng, tha).
            location (str): "Internal" if subtitle is embedded in the video,
                "External" if it is not.
            subtitleStreamsIndex (int): Index of this
                :class:`~plexapi.media.SubtitleStream` in
                MediaPart.subtitleStreams().
            title (str): Title of the subtitle stream.
    """

    def __init__(self, subtitleStream, allStreamsIndex, subtitleStreamsIndex):
        # Initialize variables
        self.allStreamsIndex = allStreamsIndex
        self.codec = subtitleStream.codec
        self.forced = subtitleStream.forced
        self.languageCode = subtitleStream.languageCode
        self.location = "Internal" if subtitleStream.index >= 0 else "External"
        self.subtitleStreamsIndex = subtitleStreamsIndex
        self.title = subtitleStream.title

    def __eq__(self, other):
        return not ((self is None) ^ (other is None)) \
            and self.allStreamsIndex == other.allStreamsIndex \
            and self.codec == other.codec \
            and self.forced == other.forced \
            and self.languageCode == other.languageCode \
            and self.location == other.location \
            and self.subtitleStreamsIndex == other.subtitleStreamsIndex \
            and self.title == other.title


class OrganizedStreams:
    """ Container class that stores AudioStreams and SubtitleStreams while
        allowing for additional organizational functionality.
        Attributes:
            audioStreams (list<:class:`~plexapi.media.AudioStream`>): List of
                all AudioStreams in MediaPart
            externalSubs (list<:class:`~plexapi.media.SubtitleStream`>): List
            of all SubtitleStreams that are located in the MediaPart externally
            internalSubs (list<:class:`~plexapi.media.SubtitleStream`>): List
                of all SubtitleStreams that are located in the MediaPart
                internally
            part (:class:`~plexapi.media.MediaPart`): MediaPart that these
                streams belong to
            subtitleStreams (list<:class:`~plexapi.media.SubtitleStream`>):
                List of all SubtitleStreams in MediaPart
    """

    def __init__(self, mediaPart):

        # Store all streams
        self.part = mediaPart
        self.audioStreams = mediaPart.audioStreams()
        self.subtitleStreams = mediaPart.subtitleStreams()

        # Separate internal & external subtitles
        self.internalSubs = []
        self.externalSubs = []
        for stream in self.subtitleStreams:
            if stream.index >= 0:
                self.internalSubs.append(stream)
            else:
                self.externalSubs.append(stream)

    def allStreams(self):
        """ Return a list of all :class:`~plexapi.media.AudioStream` and
            :class:`~plexapi.media.SubtitleStream`> in MediaPart."""
        return self.audioStreams + self.subtitleStreams

    def getIndexFromStream(self, givenStream):
        """ Return 1-index of given :class:`~plexapi.media.AudioStream` or
            :class:`~plexapi.media.SubtitleStream`. """
        streams = self.allStreams()
        for i, stream in enumerate(streams, 1):
            if givenStream.id == stream.id:
                return i
        raise Exception("AudioStream or SubtitleStream not found.")

    def getStreamFromIndex(self, givenIndex):
        """ Return :class:`~plexapi.media.AudioStream` or
            :class:`~plexapi.media.SubtitleStream` from a given index (1-index)
        """
        streams = self.allStreams()
        if givenIndex > len(streams) or givenIndex < 1:
            raise IndexError("Given index is out of range.")
        return streams[givenIndex - 1]

    def indexIsAudioStream(self, givenIndex):
        """ Return True if givenIndex is the index of an
            :class:`~plexapi.media.AudioStream`, False otherwise.
        """
        return 0 < givenIndex <= len(self.audioStreams)

    def indexIsSubStream(self, givenIndex):
        """ Return True if givenIndex is the index of a
            :class:`~plexapi.media.SubtitleStream`, False otherwise.
        """
        if givenIndex <= len(self.allStreams()):
            return not self.indexIsAudioStream(givenIndex)
        return False
