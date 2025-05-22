from netmiko import ConnectHandler
with open('devices.txt')as f:
    devices=f.read().split()

device_list=list()

#this for loop takes the info from devices.txt and adds it to an empty list called device_list
for ip in devices:
    cisco_device= {
        'device_type':'cisco_ios',
        'host':ip,
        'username':'u1',
        'password': 'cisco',
        'port':22,
        'secret':'cisco',
    'verbose':True
    }
    device_list.append(cisco_device)

#print(device_list)

for device in device_list:
    connection=ConnectHandler(**device)
    print('Entering enable mode...')
    connection.enable()

    #enter a file name to send configuration commands
    file=input(f'Enter a configuration file (use a valid path) for {device["host"]}: ')
    output=connection.send_config_from_file(file)
    print(output)

    print(f'Closing connection to {cisco_device["host"]}')
    connection.disconnect()
    print('#'*30)
