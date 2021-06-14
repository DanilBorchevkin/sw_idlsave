import scipy.io

sav_data = scipy.io.readsav('./input/ON2_2015_079m.sav')

print(sav_data)
print(sav_data.keys())

