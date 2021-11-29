import scipy.io

def save_to_ascii_file(data_list, out_filepath):
    write_list = []

    for data in data_list:
        output_str = ""
        for val in data:
            output_str += str(val) + "\t"
        output_str = output_str[:-1]
        output_str += "\n"
        write_list.append(output_str)

    with open(out_filepath,"w") as f:
        f.writelines(write_list)

def process_file(input_folder, filename, output_folder):
    sav_data = scipy.io.readsav('./input/ON2_2015_079m.sav')

    # For output available keys use it
    #print(sav_data.keys())

    # All data saved in 'saved_data' dict key
    # Available records
    # - lat
    # - lon
    # - sza
    # - on2
    # - fdoy
    # - points
    # - data
    # - year
    # - orbit

    output_list = list()

    output_list.append([
        'lat',
        'lon',
        'sza',
        'on2',
        'fdoy',
        'points',
        'data_1',
        'data_2',
        'data_3',
        'data_4',
        'data_5',
        'year',
        'orbit'
    ])

    for idx_entity,lat_entity in enumerate(sav_data['saved_data']['lat']):
        for idx_lat, lat in enumerate(lat_entity):
            if (sav_data['saved_data']['fdoy'][idx_entity][[idx_lat]] == 0.0) and (sav_data['saved_data']['on2'][idx_entity][idx_lat] == 0.0) and (sav_data['saved_data']['sza'][idx_entity][idx_lat] == 0.0):
                # Reject null values
                continue
            
            output_list.append([
                sav_data['saved_data']['lat'][idx_entity][idx_lat],
                sav_data['saved_data']['lon'][idx_entity][idx_lat],
                sav_data['saved_data']['sza'][idx_entity][idx_lat],
                sav_data['saved_data']['on2'][idx_entity][idx_lat],
                sav_data['saved_data']['fdoy'][idx_entity][idx_lat],
                sav_data['saved_data']['points'][idx_entity],
                sav_data['saved_data']['data'][idx_entity][idx_lat][0],
                sav_data['saved_data']['data'][idx_entity][idx_lat][1],
                sav_data['saved_data']['data'][idx_entity][idx_lat][2],
                sav_data['saved_data']['data'][idx_entity][idx_lat][3],
                sav_data['saved_data']['data'][idx_entity][idx_lat][4],
                sav_data['saved_data']['year'][idx_entity].decode('ascii'),
                sav_data['saved_data']['orbit'][idx_entity].decode('ascii')
            ])

    save_to_ascii_file(output_list, output_folder + filename.replace(".", "_") + ".dat")

def main():
    print("Script is started")

    output_list = process_file("./input/", "ON2_2005_001m.sav", "./output/")

    print("Script is finished")

if __name__ == '__main__':
    main()