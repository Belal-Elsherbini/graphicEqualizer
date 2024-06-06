import numpy as np
import scipy
import customtkinter as ctk
from playsound import playsound
#create basic app layout
root = ctk.CTk()
root.geometry('1500x1000')
root.title("6-Band Graphic Equalizer")



#Split the audible frequency spectrum into individual bands 
bands = [(0,200), (200,500), (500,1000), (1000,5000), (5000,10000), (10000,20000)]


#create functions that update slider values for each bandwidth 
def bassSlider(value):
    bassLabel.configure(text = f"Bass: {int(value)}")
def lmrSlider(value):
    lowMidrangeLabel.configure(text = f"LMR: {int(value)}")
def midrangeSlider(value):
    midrangeLabel.configure(text = f"MR: {int(value)}")
def umrSlider(value):
    upperMidrangeLabel.configure(text = f"UMR: {int(value)}")
def presenceLabelSlider(value):
    presenceLabel.configure(text = f"Pres.: {int(value)}")
def brillianceSlider(value):
    brillianceLabel.configure(text = f"Brill.: {int(value)}")


#create vertical sliders and labels for all the bandwidths
bass = ctk.CTkSlider(root, from_= -100, to=100, orientation="vertical", command=bassSlider)
lowMidrange = ctk.CTkSlider(root, from_= -100, to=100, orientation="vertical", command=lmrSlider)
midrange = ctk.CTkSlider(root, from_= -100, to=100, orientation="vertical", command=midrangeSlider)
upperMidrange = ctk.CTkSlider(root, from_= -100, to=100, orientation="vertical", command=umrSlider)
presence = ctk.CTkSlider(root, from_= -100, to=100, orientation="vertical", command=presenceLabelSlider)
brilliance = ctk.CTkSlider(root, from_= -100, to=100, orientation="vertical", command=brillianceSlider)

bassLabel = ctk.CTkLabel(root, text="", font=("Helvetica", 18))
lowMidrangeLabel = ctk.CTkLabel(root, text="", font=("Helvetica", 18))
midrangeLabel = ctk.CTkLabel(root, text="", font=("Helvetica", 18))
upperMidrangeLabel = ctk.CTkLabel(root, text="", font=("Helvetica", 18))
presenceLabel = ctk.CTkLabel(root, text="", font=("Helvetica", 18))
brillianceLabel = ctk.CTkLabel(root, text="", font=("Helvetica", 18))

#place the labels and sliders in the gui
bass.pack(side=ctk.LEFT, padx=100)
bassLabel.place(relx=0.05, rely=0.61, anchor=ctk.W)
bass.set(1)
bassLabel.configure(text = f"Bass: {1}")

lowMidrange.pack(side=ctk.LEFT, padx=100)
lowMidrangeLabel.place(relx=0.2, rely=0.61, anchor=ctk.W)
lowMidrange.set(1)
lowMidrangeLabel.configure(text = f"LMR: {1}")

midrange.pack(side=ctk.LEFT, padx=100)
midrangeLabel.place(relx=0.34, rely=0.61, anchor=ctk.W)
midrange.set(1)
midrangeLabel.configure(text = f"MR: {1}")

upperMidrange.pack(side=ctk.LEFT, padx=100)
upperMidrangeLabel.place(relx=0.49, rely=0.61, anchor=ctk.W)
upperMidrange.set(1)
upperMidrangeLabel.configure(text = f"UMR: {1}")

presence.pack(side=ctk.LEFT, padx=100)
presenceLabel.place(relx=0.63, rely=0.61, anchor=ctk.W)
presence.set(1)
presenceLabel.configure(text = f"Presence: {1}")

brilliance.pack(side=ctk.LEFT, padx=100)
brillianceLabel.place(relx=0.77, rely=0.61, anchor=ctk.W)
brilliance.set(1)
brillianceLabel.configure(text = f"Brilliance: {1}")



#create a function that reads the wav file
def loadAudio(path):
    sampleRate, data = scipy.io.wavfile.read(path)
    dataL = data[: , 0]
    dataR = data[: , 1]
    return sampleRate, dataL, dataR

#applies the user defined gains to the audio
def applyGains(audioDataL, audioDataR, sampleRate, gains):
    #calculate fft
    dataFTLeft = np.fft.fft(audioDataL)
    dataFTRight = np.fft.fft(audioDataR)
    modifiedDataFTLeft = dataFTLeft.copy()
    modifiedDataFTRight = dataFTRight.copy()

    leftFrequencies = np.fft.fftfreq(len(dataFTLeft), 1/sampleRate)
    rightFrequencies = np.fft.fftfreq(len(dataFTRight), 1/sampleRate)


    i = 0
    for frequency in leftFrequencies:
        for band in bands:
            if(frequency >= band[0] and frequency < band[1]):
                modifiedDataFTLeft[i] = dataFTLeft[i] * gains[bands.index(band)]
        i += 1

    j = 0
    for frequency in rightFrequencies:
        for band in bands:
            if(frequency >= band[0] and frequency < band[1]):
                modifiedDataFTRight[j] = dataFTRight[j] * gains[bands.index(band)]
        j += 1

    inverseLeftFT = np.fft.ifft(modifiedDataFTLeft)
    inverseRightFT = np.fft.ifft(modifiedDataFTRight)

    inverseLeftFT = np.clip(inverseLeftFT, -32768, 32767)
    inverseRightFT = np.clip(inverseRightFT, -32768, 32767)

    modifiedAudio = np.vstack((inverseLeftFT, inverseRightFT)).T
    modifiedAudio = np.real(modifiedAudio).astype(np.int16)

    scipy.io.wavfile.write("modifiedAudio.wav", sampleRate, modifiedAudio)

    print(gains)
    print(modifiedAudio)

def playMixedAudio():
    playsound('modifiedAudio.wav')

def lockGain():
    bassGain = bass.get()
    lmrGain = lowMidrange.get()
    mrGain = midrange.get()
    umrGain = upperMidrange.get()
    presenceGain = presence.get()
    brillianceGain = brilliance.get()
    samplingRate,dataLeft, dataRight = loadAudio('original.wav')
    gains = [bassGain, lmrGain, mrGain, umrGain, presenceGain, brillianceGain]
    applyGains(dataLeft, dataRight, samplingRate, gains)
    playAudio.configure(state=ctk.NORMAL)



gainLockIn = ctk.CTkButton(master = root, corner_radius=10, command=lockGain, text="Mix")
gainLockIn.place(relx=0.5,rely=0.2,anchor=ctk.CENTER)

playAudio = ctk.CTkButton(master=root, corner_radius=10, command=playMixedAudio, text="Play Mixed Audio")
playAudio.configure(state=ctk.DISABLED)
playAudio.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)
root.mainloop()
