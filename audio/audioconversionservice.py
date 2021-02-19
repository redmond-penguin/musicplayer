from audio.wavfile import WavFile

class AudioConversionService:
    def convert_audio_file(self, source_file, target_file):
        wav_file = None
        try:
            if type(source_file) == WavFile:
                wav_file = source_file
            else:
                if type(target_file) == WavFile:
                    wav_file = target_file
                else:
                    wav_file = WavFile("temp.wav") # todo: make sure it's a unique name
                source_file.convert_to_wav(wav_file.get_path())
            if not type(target_file) == WavFile:
                target_file.convert_from_wav(wav_file.get_path())
        except Exception as e:
            print("Conversion failed! " + str(e))
        finally:
            if wav_file != None and wav_file != source_file and wav_file != target_file:
                wav_file.delete()
