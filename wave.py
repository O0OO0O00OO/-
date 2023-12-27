import openpyxl
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import numpy as np
import datetime
# Load the workbook
wbname='data.xlsx'
workbook = openpyxl.load_workbook(wbname)
# Select the active worksheet
sheet = workbook.active
sec=[]
data=[]

# Iterating through rows
for row in sheet.iter_rows(values_only=True):
    try:
        sec.append(float((row[0])))
        data.append(float(row[1]))
    except:
        pass
# Close the workbook when done
workbook.close()

#time domain
sampling_freq = 200.0
low_cutoff_theta = 4
high_cutoff_theta= 8
low_cutoff_alpha = 8
high_cutoff_alpha = 12
low_cutoff_beta = 12
high_cutoff_beta = 25
low_cutoff_delta = 2
high_cutoff_delta = 4
nyquist = 0.5 * sampling_freq
low_alpha = low_cutoff_alpha / nyquist
high_alpha = high_cutoff_alpha / nyquist
low_theta = low_cutoff_theta / nyquist
high_theta = high_cutoff_theta / nyquist
low_beta = low_cutoff_beta / nyquist
high_beta = high_cutoff_beta / nyquist
low_delta = low_cutoff_delta / nyquist
high_delta = high_cutoff_delta / nyquist
b_a, a_a = butter(N=6, Wn=[low_alpha, high_alpha], btype='band')
b_t, a_t = butter(N=6, Wn=[low_theta, high_theta], btype='band')
b_b, a_b = butter(N=6, Wn=[low_beta, high_beta], btype='band')
b_d, a_d = butter(N=6, Wn=[low_delta, high_delta], btype='band')
filtered_data_a = filtfilt(b_a, a_a, data)
filtered_data_t = filtfilt(b_t, a_t, data)
filtered_data_b = filtfilt(b_b, a_b, data)
filtered_data_d = filtfilt(b_d, a_d, data)
#freq domain
fft_result_a = np.fft.fft(filtered_data_a)
fft_result_t = np.fft.fft(filtered_data_t)
fft_result_b = np.fft.fft(filtered_data_b)
fft_result_d = np.fft.fft(filtered_data_d)
frequencies_a = np.fft.fftfreq(len(fft_result_a), 1 / sampling_freq)
frequencies_t = np.fft.fftfreq(len(fft_result_t), 1 / sampling_freq)
frequencies_b = np.fft.fftfreq(len(fft_result_b), 1 / sampling_freq)
frequencies_d = np.fft.fftfreq(len(fft_result_d), 1 / sampling_freq)
'''
plt.figure()
plt.plot(frequencies_a, np.abs(fft_result_a))
plt.plot(frequencies_t, np.abs(fft_result_t))
plt.plot(frequencies_b, np.abs(fft_result_b))
plt.plot(frequencies_d, np.abs(fft_result_d))
plt.xlabel('freq(Hz)')
plt.ylabel('amplitute')
plt.show()
'''
condi_a =(np.abs(frequencies_a)>=8)&(np.abs(frequencies_a)<=12)
condi_t =(np.abs(frequencies_a)>=4)&(np.abs(frequencies_a)<=8)
condi_b =(np.abs(frequencies_a)>=12)&(np.abs(frequencies_a)<=24)
condi_d =(np.abs(frequencies_a)>=2)&(np.abs(frequencies_a)<=4)

sum_a=np.sum(np.abs(fft_result_a[condi_a]))
sum_t=np.sum(np.abs(fft_result_t[condi_t]))
sum_b=np.sum(np.abs(fft_result_b[condi_b]))
sum_d=np.sum(np.abs(fft_result_d[condi_d]))
'''
print(wbname)
print("delta(2-4)=",'\t',sum_d)
print("theta(4-8)=",'\t',sum_t)
print("alpha(8-12)=",'\t',sum_a)
print("beta(12-25)=",'\t',sum_b)
'''
print("a+t=",'\t\t',sum_t+sum_a)
print("a+t /b=",'\t',(sum_t+sum_a)/sum_b)
print(datetime.datetime.now())
if((sum_t+sum_a)/sum_b < 1              and 0):
    print (" Exhausted. Watchout! ")
if((sum_t+sum_a)< 7000                  and 1):
    print (" Exhausted. Watchout! ")
