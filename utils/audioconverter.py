from pydub import AudioSegment

wav_audio = AudioSegment.from_file("uploads/1599048813891.aac", format='aac')
print("Audio Channels "+str(wav_audio.channels)+" Rate "+str(wav_audio.frame_rate)+" BytesPerSample "+str(wav_audio.sample_width))
wav_audio.set_channels(1)
wav_audio.set_frame_rate(16000)
newWaveAudio = wav_audio.split_to_mono()
print("splitted "+str(newWaveAudio))
print(newWaveAudio[0].channels)

newWaveAudio[0].export('1599048813891.wav', format='wav')