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

def process_file_last_format(input_folder, filename, output_folder):
    sav_data = scipy.io.readsav(input_folder + filename)

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
    
def process_file_prev_format(input_folder, filename, output_folder):
    sav_data = scipy.io.readsav(input_folder + filename)

    # Available records
    # - ON
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
        'doy',
        'points',
        'd_lat',
        'd_lon',
        'ut',
        'day',
        'month',
        'year',
        'orbit'
    ])

    for idx_slice, _ in enumerate(sav_data['saved_data']['lat']):
        for idx_lat, val_lat in enumerate(sav_data['saved_data']['lat'][idx_slice]): 
            if  sav_data['saved_data']['lat'][idx_slice][idx_lat] == 0.0 \
                and sav_data['saved_data']['lon'][idx_slice][idx_lat] == 0.0 \
                and sav_data['saved_data']['sza'][idx_slice][idx_lat] == 0.0 \
                and sav_data['saved_data']['on2'][idx_slice][idx_lat] == 0.0 :
                    continue       
            output_list.append([
                sav_data['saved_data']['lat'][idx_slice][idx_lat],
                sav_data['saved_data']['lon'][idx_slice][idx_lat],
                sav_data['saved_data']['sza'][idx_slice][idx_lat],
                sav_data['saved_data']['on2'][idx_slice][idx_lat],
                sav_data['saved_data']['doy'][idx_slice].decode('ascii'),
                sav_data['saved_data']['points'][idx_slice],
                sav_data['saved_data']['d_lat'][idx_slice],
                sav_data['saved_data']['d_lon'][idx_slice],
                sav_data['saved_data']['ut'][idx_slice][idx_lat],
                sav_data['saved_data']['day'][idx_slice],
                sav_data['saved_data']['month'][idx_slice],
                sav_data['saved_data']['year'][idx_slice].decode('ascii'),
                sav_data['saved_data']['orbit'][idx_slice].decode('ascii')
            ])

    save_to_ascii_file(output_list, output_folder + filename.replace(".", "_") + ".dat")

def main():
    print("Script is started")
    
    # Change here
    INPUT_PATH = "./input/"
    INPUT_FILENAME = "ON2_2005_001m.sav"
    OUTPUT_PATH = "./output/"
    # ----------------------------------

    is_file_parsed = False

    try:
        print("Try to parse as past format...")
        process_file_last_format(INPUT_PATH, INPUT_FILENAME, OUTPUT_PATH)
        is_file_parsed = True
    except Exception as e:
        print(f"Cannot parse the file as last version of the format. Reason <{str(e)}>")
        
    if not is_file_parsed:
        try:
            print("Try to parse as prevous format...")
            process_file_prev_format(INPUT_PATH, INPUT_FILENAME, OUTPUT_PATH)
            is_file_parsed = True
        except Exception as e:
            print(f"Cannot parse the file as prev version of the format. Reason <{str(e)}>")
    
    if not is_file_parsed:
        print(f"Cannot parse file <{INPUT_PATH}{INPUT_FILENAME}> due to unknown format")

    print("Script is finished")

if __name__ == '__main__':
    main()