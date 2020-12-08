import csv
import GTC

e_tape_cal_1 = GTC.ureal(0, 0.0005, 70)
e_tape_cal_2 = GTC.ureal(0, 0.0005, 70)
e_position_setting_1 = GTC.ureal(0, 0.0005, 70)
e_position_setting_2 = GTC.ureal(0, 0.0005, 70)

d = []
pos1 = []
pos2 = []
ref1 = []
ref2 = []
DUT1 = []
DUT2 = []

with open("G:\\Shared drives\MSL - Photometry & Radiometry\\COMMERCIAL\\Photometry\\2020\\96150233 - Stephenson & Turner NZ Ltd\\Ref plane Uncertainty in.csv", mode='r') as csv_file:
    data = csv.reader(csv_file, delimiter=",")
    for row in data:
        print(row)
        d1 = GTC.ureal(float(row[2]), 0) + e_tape_cal_1 + e_position_setting_1
        d2 = GTC.ureal(float(row[3]), 0) + e_tape_cal_2 + e_position_setting_2
        d.append(d2 - d1)
        ref1.append(GTC.ureal(float(row[6]), float(row[7])))
        ref2.append(GTC.ureal(float(row[8]), float(row[9])))
        DUT1.append(GTC.ureal(float(row[10]), float(row[11])))
        DUT2.append(GTC.ureal(float(row[13]), float(row[14])))

with open("G:\\Shared drives\MSL - Photometry & Radiometry\\COMMERCIAL\\Photometry\\2020\\96150233 - Stephenson & Turner NZ Ltd\\Ref plane Uncertainty out.csv", mode='w') as file_out:


    print(d)
    x1 = []
    pos = 0
    for value in d:
        x1.append(d[pos] * ((1 / (GTC.sqrt(DUT1[pos] / DUT2[pos]) - 1)) - (1 / (GTC.sqrt(ref1[pos] / ref2[pos]) - 1))))
        file_out.write(str(GTC.value(d[pos])) + "," + str(GTC.value(ref1[pos])) + "," + str(GTC.uncertainty(ref1[pos]))
                       + "," + str(GTC.value(ref2[pos])) + "," + str(GTC.uncertainty(ref2[pos])) + "," +
                       str(GTC.value(DUT1[pos])) + "," + str(GTC.uncertainty(DUT1[pos])) + "," +
                       str(GTC.value(DUT2[pos])) + "," + str(GTC.uncertainty(DUT2[pos])) + "," + str(GTC.value(x1[pos])) +
                       "," + str(GTC.uncertainty(x1[pos])) + "\n")
        pos += 1

    print(x1)

