from models import OrganizedStreams


# Find closest Audio Stream match in a specific episode, given some AudioStreamInfo template
def match_audio(episodePart, template):

    # Get episode streams
    episodeStreams = OrganizedStreams(episodePart)
    audioStreams = episodeStreams.audioStreams

    # Initialize variables
    winningIndex = -1  # Index of AudioStream in the lead (1-indexed)
    winningScore = -1  # Score of AudioStream in the lead

    for i, stream in enumerate(audioStreams, 1):

        # If title and language code match, AudioStream automatically matches
        if (stream.title and stream.title == template.title and
                stream.languageCode == template.languageCode):
            return stream

        # Languages must be the same to even be considered for a match
        if stream.languageCode == template.languageCode:

            # Start scoring match
            curScore = 0

            # Audio codec and channel layout
            if (stream.codec == template.codec and
                    stream.audioChannelLayout == template.audioChannelLayout):
                curScore += 1

            # Index in AudioStreams list
            if i == template.audioStreamsIndex:
                curScore += 1

            # Check if AudioStream is winning
            if curScore > winningScore:
                winningScore = curScore
                winningIndex = i

    if winningScore >= 0:
        return audioStreams[
            winningIndex - 1]  # Must subtract one because array is 0-indexed


# Find closest Subtitle Stream match in a specific episode, given some SubtitleStreamInfo template
def matchSubtitles(episodePart, template):

    # Get episode streams
    episodeStreams = OrganizedStreams(episodePart)
    subtitleStreams = episodeStreams.subtitleStreams

    # Initialize variables
    winningIndex = -1  # Index of AudioStream in the lead (1-indexed)
    winningScore = -1  # Score of AudioStream in the lead

    for i, stream in enumerate(subtitleStreams, 1):

        # If title and language code match, SubtitleStream automatically
        # matches
        if (stream.title and stream.title == template.title and
                stream.languageCode == template.languageCode):
            return stream

        # Languages must be the same to even be considered for a match
        if stream.languageCode == template.languageCode:

            # Start scoring match
            curScore = 0

            # Codec
            if stream.codec == template.codec:
                curScore += 1

            # Internal vs. external
            location = "Internal" if stream.index >= 0 else "External"
            if location == template.location:
                curScore += 1

            # Forced
            if stream.forced == template.forced:
                curScore += 1

            # Index in SubtitleStreams list
            if i == template.subtitleStreamsIndex:
                curScore += 1

            # Check if SubtitleStream is winning
            if curScore > winningScore:
                winningScore = curScore
                winningIndex = i

    if winningScore >= 0:
        return subtitleStreams[
            winningIndex - 1]  # Must subtract one because array is 0-indexed
