import json

class Track(object):
    """
    Plugin to manage 
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    def __init__(self, track_info):
        """
        Track constructor
        track_info -- Dictionary containing the track information:
            ['file'] -- The file ID (mandatory, stream URL, file path, Spotify ID...)
            ['artist'] -- Track artist
            ['title'] -- Track title
            ['album'] -- Track album
            ['time'] -- Track time (in seconds)
            ['elapsed'] -- Track elapsed time (in seconds)
            ['state'] -- Track state (playing, stopped, paused)
        """

        if 'file' not in track_info:
            raise AttributeError("File ID not specified")

        self.track = {
            'file':  track_info['file'] if 'file' in track_info else None,
            'artist': track_info['artist'] if 'artist' in track_info else None,
            'title': track_info['title'] if 'title' in track_info else None,
            'album': track_info['album'] if 'album' in track_info else None,
            'time': track_info['time'] if 'time' in track_info else None,
            'state': track_info['state'] if 'state' in track_info else None,
            'elapsed': track_info['elapsed'] if 'elapsed' in track_info else None,
        }

    def get(self, field):
        """ Retrieve the field `field` from the internal track information """
        return self.track[field]

    def equals(self, other_track):
        """ Return true if two tracks equal (i.e. if they have the same file ID) """
        return False \
            if not 'file' in self.track \
                or other_track.get('file') is None \
            else (self.track['file'] == other_track.get('file') \
                    and self.track['title'] == other_track.get('title'))

    def dump(self):
        """ Dump the track info in JSON format """
        return json.dumps(self.track)

    def update_now_playing(self, session_key=None):
        """ Update the configured Last.FM profile "now playing" track with this track """
        from lastfm import LastFM
        from config import Config

        if session_key is None:
            session_key = Config.get_config().get('lastfm.sessionkey')

        LastFM(session_key=session_key).apiCall('track.updateNowPlaying', {
            'artist': self.track['artist'],
            'track': self.track['title'],
            'duration': self.track['time'],
        })

    def scrobble(self, session_key=None):
        """ Scrobble this track to the configured Last.FM profile """
        from lastfm import LastFM
        from config import Config

        if session_key is None:
            session_key = Config.get_config().get('lastfm.sessionkey')

        LastFM(session_key=session_key).apiCall('track.scrobble', {
            'artist[0]': self.track['artist'],
            'track[0]': self.track['title'],
            'duration[0]': self.track['time'],
            'timestamp[0]': int(time.time()),
        })

    def notify(self):
        """
        Notify the system that this track is currently being played.
        @TODO: Make it customizable - i.e. custom shell command executed to notify
            the track, retrieving its information through a format string
        """
        os.system('notify-send -t 3000 "%s - %s"' % (self.track['artist'], self.track['title']))

class EmptyTrack(Track):
    """
    Empty track, used to initialize un-initialized track statuses, or for track comparisons
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """
    def __init__(self):
        Track.__init__(self, { 'file': None })

