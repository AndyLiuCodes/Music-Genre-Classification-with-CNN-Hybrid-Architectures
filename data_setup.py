#! /usr/env/python3
import os
import shutil
from Data_Processing import conversion
from Data_Processing import spect_create
from Data_Processing import data_csv_gen
from Data_Processing import utils

#number of files you want to convert to .wav, this
#also affects the number of spectrograms you create
FILES_TO_GENERATE = 50
SONG_DURATION = 30
SPECTROGRAM_WIDTH = 3 #in inches
SPECTROGRAM_HEIGHT = 3 #in inches
SPECTROGRAM_DPI = 500
SONG_SAMPLING_RATE = 16000

print("Beginning Setup")

shutil.rmtree("./Data/")
conversion.mp3_Convert(FILES_TO_GENERATE)

spect_create.Spectrogram_Create(SPECTROGRAM_WIDTH, SPECTROGRAM_HEIGHT,
                                SPECTROGRAM_DPI, SONG_DURATION, SONG_SAMPLING_RATE)

data_csv_gen.Generate_CSV()

print("Removing Samples Folder")
shutil.rmtree("./Samples/")

print("Setup Complete")