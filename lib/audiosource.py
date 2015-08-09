import os

from __init__ import Armando
from config import Config
from logger import Logger

class AudioSource(object):
    """
    AudioSource class for Armando platform
    @depend: arecord (ALSA record), in order to record the audio. Yes, I used Pyaudio before,
        but the other apps using Pyaudio were then systematically breaking their audio stack
        after I used this code. You can anyway customize your audio recording app through
        audio.record_cmd config setting, as long as the app returns a WAV file (for FLAC conversion)
    @depend: flac executable in your PATH, to convert the recorded audio to FLAC [apt-get install flac, pacman -S flac]
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    __config = Config.get_config()
    __logger = Logger.get_logger(__name__)
    __default_wav_file = '%s/audio.wav' % (Armando.get_tmp_dir())
    __default_flac_file = '%s/audio.flac' % (Armando.get_tmp_dir())
    __default_record_seconds = 3
    __default_record_cmd = 'arecord -f cd -t wav -d %d -r 44100 > %s' \
        % (__default_record_seconds, __default_wav_file)
    __default_flac_cmd = 'flac -f %s -o %s' % (__default_wav_file, __default_flac_file)

    def __init__(self):
        """
        self.wav_file -- From config [audio.wav_file] or __TMPDIR__/audio.wav
        self.flac_file -- From config[audio.flac_file] or __TMPDIR__/audio.flac
        self.record_seconds -- From config[audio.record_seconds] or 3
        self.record_cmd -- From config[audio.record_cmd] or `arecord -f cd -t wav -d self.record_seconds -r 44100 > self.wav_file`
        self.flac_cmd -- From config[audio.flac_cmd] or `flac -f self.wav_file -o self.flac_file`
        """
        self.wav_file = AudioSource.__config.get('audio.wav_file') or AudioSource.__default_wav_file
        self.flac_file = AudioSource.__config.get('audio.flac_file') or AudioSource.__default_flac_file
        self.record_seconds = AudioSource.__config.get('audio.record_seconds') or AudioSource.__default_record_seconds
        self.record_cmd = AudioSource.__config.get('audio.record_cmd') or AudioSource.__default_record_cmd
        self.flac_cmd = AudioSource.__config.get('audio.flac_cmd') or AudioSource.__default_flac_cmd

        AudioSource.__logger.info({
            'msg_type': 'Initializing audio source',
            'wav_file': self.wav_file,
            'flac_file': self.flac_file,
            'record_seconds': self.record_seconds,
            'record_cmd': self.record_cmd,
            'flac_cmd': self.flac_cmd,
        })

    def record_to_wav(self):
        """ Record from the audio source and output the recorded WAV audio to self.wav_file """
        AudioSource.__logger.info({
            'msg_type': 'Recording started',
            'wav_file': self.wav_file,
        })

        os.system(self.record_cmd)

        AudioSource.__logger.info({
            'msg_type': 'Recording stopped',
            'wav_file': self.wav_file,
        })

    def record_to_flac(self):
        """ Record from the audio source and output the recorded audio to self.flac_file """
        self.record_to_wav()

        AudioSource.__logger.debug({
            'msg_type': 'Converting WAV to FLAC file',
            'wav_file': self.wav_file,
            'flac_file': self.flac_file,
        })

        os.system(self.flac_cmd)
        os.remove(self.wav_file)

        AudioSource.__logger.debug({
            'msg_type': 'Converted WAV to FLAC file',
            'wav_file': self.wav_file,
            'flac_file': self.flac_file,
        })

# vim:sw=4:ts=4:et:

