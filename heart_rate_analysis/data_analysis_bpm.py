import heartpy as hp
import numpy
import csv
#hrdata = hp.get_data('J:\\Lithic\\data\\heart\\heat.csv')

txt_file_address = 'E:\\Lithic\\data\\heart\\heart-bill.txt'
csv_file_address = txt_file_address.replace('txt','csv')

in_txt = csv.reader(open(txt_file_address, "r"), delimiter = ',')
out_csv = csv.writer(open(csv_file_address, 'w'))

out_csv.writerows(in_txt)
print(csv_file_address)

hrdata = hp.get_data(csv_file_address, column_name='Analog1_chA')
timerdata = hp.get_data(csv_file_address, column_name='Timestamp')
# column_name='Timestamp','Analog1_chA','Analog1_chB'
working_data, measures = hp.process(hrdata, hp.get_samplerate_mstimer(timerdata))
hp.plotter(working_data, measures, title='Heart Beat Detection on Noisy Signal')