import os, psutil, datetime, time, csv

path = input("Enter the path: ")
os.system('open ' + path)

def main():

    interval = int(input("Enter the interval: "))

    basename = os.path.basename(path)

    list_of_process_objects = []

    final_data_lst = []

    for proc in psutil.process_iter():

        if basename.lower() in proc.name().lower():
            process_info = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            list_of_process_objects.append(process_info)
            print(basename.lower())

    for elem in list_of_process_objects:

        if psutil.Process(elem['pid']).exe() == path:
            print('TRUE')

            csv_file = f"cpu_usage_{str(datetime.datetime.now().strftime('%Y_%m_%d-%H:%M:%S'))}.csv"

            while psutil.pid_exists(elem['pid']):

                data_dict = {
                'processID' : elem['pid'],
                'basename' : elem['name'],
                'processCreationTime': datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S"),
                'cpu_usage' : psutil.Process(elem['pid']).cpu_percent(interval=1) / psutil.cpu_count(),
                'memory' : psutil.Process(elem['pid']).memory_info().vms / (1024 * 1024 * 1024),
                }
                num_fds = psutil.Process(elem['pid']).as_dict(attrs=['num_fds'])
                for i, k in num_fds.items():
                    data_dict['num_fds'] = k

                final_data_lst.append(data_dict)

                fieldnames = data_dict.keys()

                with open(csv_file, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for i in final_data_lst:
                        writer.writerow(i)

                time.sleep(interval)

if __name__ == "__main__":
    main()

    
    










