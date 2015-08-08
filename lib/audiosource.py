from array import array
from struct import pack
from sys import byteorder
from logger import Logger

import copy
import os
import re
import pyaudio
import wave

class AudioSource(object):
    """
    AudioSource class for Armando platform
    @depend: pyaudio [pip install pyaudio]
    @depend: flac executable to convert the recorded audio to FLAC [apt-get install flac, pacman -S flac]
    @author: Fabio "BlackLight" Manganiello <blacklight86@gmail.com>
    """

    threshold = 5000  # audio levels not normalised.
    chunk_size = 32768
    rate = 44100
    max_chunks = int(3 * rate / chunk_size) # 3 sec
    format = pyaudio.paInt16
    frame_max_value = 2 ** 15 - 1
    normalize_minus_one_db = 10 ** (-1.0 / 20)
    channels = 1
    trim_append = rate / 4

    def __init__(self,
             audio_file=None,
             threshold=None,
             chunk_size=None,
             rate=None):
        if audio_file is not None:
            self.audio_file = audio_file
        else:
            raise Exception('No audio.audio_file item specified in your configuration')

        self.threshold = int(threshold) if threshold is not None else self.__class__.threshold
        self.chunk_size = int(chunk_size) if chunk_size is not None else self.__class__.chunk_size
        self.rate = int(rate) if rate is not None else self.__class__.rate
        self.max_chunks = int(3 * self.rate / self.chunk_size)
        self.format = self.__class__.format
        self.frame_max_value = self.__class__.frame_max_value
        self.normalize_minus_one_db = self.__class__.normalize_minus_one_db
        self.channels = self.__class__.channels
        self.trim_append = self.__class__.trim_append

        Logger.get_logger().info({
            'msg_type': 'Initializing audio source',
            'module': self.__class__.__name__,
            'threshold': self.threshold,
            'chunk_size': self.chunk_size,
            'rate': self.rate,
            'channels': self.channels,
            'frame_max_value': self.frame_max_value,
        })

    def __normalize(self, data_all):
        """Amplify the volume out to max -1dB"""
        # MAXIMUM = 16384
        normalize_factor = (float(self.normalize_minus_one_db * self.frame_max_value)
                            / max(abs(i) for i in data_all))

        r = array('h')
        for i in data_all:
            r.append(int(i * normalize_factor))
        return r

    def __trim(self, data_all):
        _from = 0
        _to = len(data_all) - 1
        for i, b in enumerate(data_all):
            if abs(b) > self.threshold:
                _from = int(max(0, i - self.trim_append))
                break

        for i, b in enumerate(reversed(data_all)):
            if abs(b) > self.threshold:
                _to = int(min(len(data_all) - 1, len(data_all) - 1 - i + self.trim_append))
                break

        return copy.deepcopy(data_all[_from:(_to + 1)])

    def record(self):
        """Record a word or words from the microphone and 
        return the data as an array of signed shorts."""

        p = pyaudio.PyAudio()
        stream = p.open(format=self.format, channels=self.channels, rate=self.rate, input=True, output=True, frames_per_buffer=self.chunk_size)

        try:
            audio_started = False
            data_all = array('h')

            Logger.get_logger().info({
                'msg_type': 'Audio recording started',
                'module': self.__class__.__name__
            })

            while int(len(data_all) / self.chunk_size) < self.max_chunks:
                # little endian, signed short
                data_chunk = array('h', stream.read(self.chunk_size))
                if byteorder == 'big':
                    data_chunk.byteswap()
                data_all.extend(data_chunk)

            sample_width = p.get_sample_size(self.format)
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

        Logger.get_logger().info({
            'msg_type': 'Audio recording stopped',
            'module': self.__class__.__name__
        })

        data_all = self.__trim(data_all)
        data_all = self.__normalize(data_all)
        return sample_width, data_all

    @staticmethod
    def __split_filename(filename):
        basename = filename
        extension = 'wav'
        m = re.match('(.*)\.(.*)', filename)
        if m:
            basename = m.group(1)
            extension = m.group(2).lower()

        return basename, extension

    def record_to_file(self):
        "Records from the microphone and outputs the resulting data to the file"
        sample_width, data = self.record()
        data = pack('<' + ('h' * len(data)), *data)

        basename, extension = self.__split_filename(self.audio_file)
        wave_file_name = '%s.wav' % basename
        wave_file = wave.open(wave_file_name, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(sample_width)
        wave_file.setframerate(self.rate)
        wave_file.writeframes(data)
        wave_file.close()

        Logger.get_logger().debug({
            'msg_type': 'Saved recorded audio to wave file',
            'module': self.__class__.__name__,
            'filename': wave_file_name,
        })

        if extension.lower() == 'flac':
            flac_file_name = '%s.flac' % basename
            print('*** WAV [%s] FLAC [%s]' % (wave_file_name, flac_file_name))
            os.system('flac -f %s -o %s' % (wave_file_name, flac_file_name))
            os.remove(wave_file_name)

            Logger.get_logger().debug({
                'msg_type': 'Saved recorded audio to flac file',
                'module': self.__class__.__name__,
                'filename': wave_file_name,
            })

# vim:sw=4:ts=4:et:

