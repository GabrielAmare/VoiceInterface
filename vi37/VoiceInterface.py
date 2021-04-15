import os
import gtts
import playsound
import speech_recognition as sr
from typing import Union, List


class AudioToTextError(Exception):
    pass


class TextToAudioError(Exception):
    pass


class VoiceInterface:
    def __init__(self, lang_IETF: str, time_limit=5, temp_file="temp.mp3"):

        super().__init__()
        self.listener: sr = sr.Recognizer()

        self.time_limit: float = time_limit
        self.temp_file: str = temp_file

        self.lang_IETF = lang_IETF

    @property
    def lang_IETF(self):
        return self._lang_IETF

    @lang_IETF.setter
    def lang_IETF(self, value):
        self._lang_IETF = value
        self._lang_ISO_639_1 = value.split('-', 1)[0]

    @property
    def lang_ISO_639_1(self):
        return self._lang_ISO_639_1

    def _listen_parse(self, audio, show_all: bool = False) -> Union[str, List[str]]:
        try:
            result = self.listener.recognize_google(
                audio,
                language=self.lang_IETF,
                show_all=show_all
            )
            if show_all:
                return [data["transcript"] for data in result['alternative']]
            else:
                return result

        except sr.UnknownValueError:
            raise AudioToTextError

        except sr.RequestError:
            raise AudioToTextError

    def _listen_audio(self, delay):
        try:
            with sr.Microphone() as microphone:
                return self.listener.listen(microphone, phrase_time_limit=delay)

        except sr.WaitTimeoutError:
            raise AudioToTextError

    def _speak_create_gtts(self, text: str):
        try:
            return gtts.gTTS(text=text, lang=self.lang_ISO_639_1, slow=False, lang_check=False)

        except AssertionError:
            raise TextToAudioError

        except ValueError:
            raise TextToAudioError

        except RuntimeError:
            raise TextToAudioError

    def _speak_save_speech(self, speech):
        try:
            speech.save(self.temp_file)

        except gtts.tts.gTTSError:
            raise TextToAudioError

    def _speak_play_sound(self, block: bool):
        try:
            playsound.playsound(self.temp_file, block=block)

        except UnicodeDecodeError:
            raise TextToAudioError

        except playsound.PlaysoundException:
            raise TextToAudioError

        finally:
            if os.path.exists(self.temp_file) and os.path.isfile(self.temp_file):
                os.remove(self.temp_file)

    def speak(self, text: str, block: bool = True) -> None:
        """
            This method reads the given text out loud
            :param text: The text to read
            :param block: if True, blocks the process until the end of the audio
            :return None

            :raise
                TextToAudioError:
                - When ``text`` is ``None`` or empty;
                - When there's nothing left to speak after pre-precessing, tokenizing and cleaning.
                - When ``lang_check`` is ``True`` and ``lang`` is not supported.
                - When ``lang_check`` is ``True`` but there's an error loading the languages dictionary.
                - When there's an error with the API request
                - When playsound raise an UnicodeDecodeError or a PlaysoundException
        """

        speech = self._speak_create_gtts(text)

        self._speak_save_speech(speech)

        self._speak_play_sound(block)

    def listen(self, delay=None, show_all=False) -> Union[str, List[str]]:
        """
            This method listen to the user microphone and map the audio input to a corresponding text output
            :return: Text extracted from the user's record
            :raise:
                AudioToTextError:
                - When the speech is unintelligible.
                - When the speech recognition operation failed, if the key isn't valid
                - When there is no internet connection.
                - When the listener raise WaitTimeoutError while listening
        """

        audio = self._listen_audio(delay or self.time_limit)

        text = self._listen_parse(audio, show_all)

        return text

    def adjust(self, seconds=1):
        with sr.Microphone() as microphone:
            self.listener.adjust_for_ambient_noise(microphone, duration=seconds)
