import numpy as np
import scipy
import matplotlib.pyplot as plt

sampleRate, data = scipy.io.wavfile.read("piano.wav")

print(f'Sample Rate: {sampleRate}');
print(f'{data.shape}')  #data.shape returns the # of rows by # of columns in the form of a tuple. since this is a stereo audio file, it will return (# of total samples, 2)

#plotting the input audio signal
length = data.shape[0]/sampleRate #length (in seconds) of the DT audio signal
time = np.linspace(0, length, data.shape[0]); #x axis in units of samples with amplitudes
plt.plot(time,data[:,0], label = "Left Channel") #plot the left channel by tapping into the first index of the data numpy array
plt.plot(time,data[:,1], label = "Right Channel") #plot the right channel by tapping into the second index of the data numpy array
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()

#separate the left and right audio channels from the DT audio signal
left = data[:, 0]
right = data[:, 1]
