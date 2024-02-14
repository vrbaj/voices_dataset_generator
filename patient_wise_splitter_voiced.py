from pathlib import Path
import random
from utilities.converters import wav2spectrogram, txt2wav
from random import shuffle, sample



svd_path = Path("datasets", "voiced_renamed")
destination_path_wavs = Path("datasets", "wavs_voiced")
destination_path_spectrogram = Path("datasets", "spectrogram_voiced")
fft_len = 256
fft_overlap = 128
spectrogram_resolution = (480, 480)
octaves = []
chunks = 10



# for txt_file in svd_path.glob("*.*"):
#     txt2wav(txt_file, destination_path_wavs, 8000, chunks)
# print("txt2wav done")
#
# for wav_file in destination_path_wavs.glob("*.*"):
#     print(f"processing {wav_file}")
#     wav2spectrogram(wav_file, destination_path_spectrogram, fft_len, fft_overlap,
#                                     spectrogram_resolution, octaves=[], standard_chunk=False,
#                                     resampling_freq=None)
dataset_path = Path("datasets", "patients_wise_datasets_voiced")
dataset_path.mkdir(exist_ok=True)
dataset_path.joinpath("train", "healthy").mkdir(exist_ok=True, parents=True)
dataset_path.joinpath("train", "nonhealthy").mkdir(exist_ok=True, parents=True)
dataset_path.joinpath("test", "healthy").mkdir(exist_ok=True, parents=True)
dataset_path.joinpath("test", "nonhealthy").mkdir(exist_ok=True, parents=True)

patients_ids = []
for spectrogram_path in destination_path_spectrogram.glob("*.*"):
    patients_ids.append(str(spectrogram_path.name).lstrip("voice")[:3])
patients_ids = list(set(patients_ids))
shuffle(patients_ids)
test = sample(patients_ids, 24)
remove_from_test_set = sample(test, 4)
remove_segments = [random.randint(0, 9, ) for _ in range(4)]
for spectrogram_path in destination_path_spectrogram.glob("*.*"):
    spectrogram_path_str = str(spectrogram_path)

    if "nonhealthy" in str(spectrogram_path_str):
        if not str(spectrogram_path.name).lstrip("voice")[:3] in test:
            dest = dataset_path.joinpath("train", "nonhealthy")
        else:
            dest = dataset_path.joinpath("test", "nonhealthy")
    else:
        if not str(spectrogram_path.name).lstrip("voice")[:3] in test:
            dest = dataset_path.joinpath("train", "healthy")
        else:
            dest = dataset_path.joinpath("test", "healthy")
    src =spectrogram_path.read_bytes()
    dest.joinpath(spectrogram_path.name).write_bytes(src)

# randomly delete 8 files to get 208 samples in test set
test_set_paths = list(dataset_path.joinpath("test").glob("**/*"))
samples_to_delete = sample(test_set_paths, 8)

for to_delete in samples_to_delete:
    to_delete.unlink()
