import heartpy as hp
import numpy
import csv

# convert txt file to csv
#txt_file_address = 'E:\\Lithic\\data\\heart\\heart-bill.txt'
txt_file_address = 'HR_2019-09-22T14-19-17.txt'
csv_file_address = txt_file_address.replace('txt','csv')
in_txt = csv.reader(open(txt_file_address, "r"), delimiter = ',')
out_csv = csv.writer(open(csv_file_address, 'w'))

out_csv.writerows(in_txt)
print(csv_file_address)

hrdata = hp.get_data(csv_file_address, column_name='Analog1_chB')
timerdata = hp.get_data(csv_file_address, column_name='Timestamp')

working_data, measures = hp.process(hrdata, hp.get_samplerate_mstimer(timerdata))
hp.plotter(working_data, measures, title='good plot')
