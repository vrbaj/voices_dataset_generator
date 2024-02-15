from pathlib import Path
from utilities.converters import wav2spectrogram, txt2wav

dataset = "svdadult"  # or voiced
svd_path = Path("datasets", "raw", f"{dataset}_renamed")
destination_path_wavs = Path("datasets", "raw", "wavs", f"{dataset}_renamed")
destination_path_spectrogram = Path("datasets", "spectrograms", f"{dataset}_renamed")
destination_path_wavs.mkdir(parents=True, exist_ok=True)
destination_path_spectrogram.mkdir(parents=True, exist_ok=True)

fft_len = 256  # length of fft window (Hamming is used by default)
fft_overlap = 128  # overlap of ffts windows
spectrogram_resolution = (480, 480)  # desired spectrogram resolution as tuple
octaves = []  # specify octave filters if needed, see utilities.octave_filter_bank.py for details
chunks = 10  # each wav file is split into multiple chunks, set the number of chunks
if dataset == "voiced":
    sample_rate = 8000
else:
    sample_rate = 50000
for txt_file in svd_path.glob("*.*"):
    # beware!! voiced is sampled at 8 kHz, SVD is 50 kHz, set appropriate value
    txt2wav(txt_file, destination_path_wavs, sample_rate, chunks)

print("txt2wav done")

for wav_file in destination_path_wavs.glob("*.*"):
    print(f"processing {wav_file}")
    wav2spectrogram(wav_file, destination_path_spectrogram, fft_len, fft_overlap,
                                    spectrogram_resolution, octaves=[], standard_chunk=False,
                                    resampling_freq=None)
