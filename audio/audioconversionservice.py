from audio.wavfile import WavFile

class AudioConversionService:
    def convert_audio_file(self, source_file, target_file):
        try:
            wav_stdout = source_file.convert_to_wav(None, True)
            target_file.convert_from_wav(None, wav_stdout)
            source_tag = source_file.get_tag()
            target_file.set_tag(source_tag)
        except Exception as e:
            print("Conversion failed! " + str(e))
