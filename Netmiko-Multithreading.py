from netmiko import ConnectHandler
import threading
import time

start_for=time.time()

def execute(device,commands):

    print(f'Connecting to device...')
    connection = ConnectHandler(**device)
    print(f'Connecting to enable')
    connection.enable()
    print(f'connecting to global config')
    connection.config_mode()
    print(f'Sending command {commands}')
    output=connection.send_config_set(commands)
    print(output)
    print(f'Disconnecting from {device["host"]}')
    connection.disconnect()

#defining a dictionary for each device
router1={'device_type':'cisco_ios',
                  'host':'10.1.2.10',
                  'username':'u1',
                  'password':'cisco',
                  'port':22,'secret':'cisco',
                  'verbose':True}
router2={'device_type':'cisco_ios',
                  'host':'10.1.2.20',
                  'username':'u1',
                  'password':'cisco',
                  'port':22,'secret':'cisco',
                  'verbose':True}
router3={'device_type':'cisco_ios',
                  'host':'10.1.2.30',
                  'username':'u1',
                  'password':'cisco',
                  'port':22,'secret':'cisco',
                  'verbose':True}

#commands for each router
cmd1=['router ospf 1','network 0.0.0.0 0.0.0.0 area 0']
cmd2=['int loop 0','ip add 1.1.1.1 255.255.255.255','end','sh ip int l0']
cmd3=['username k9 secret abck9','ip domain-name k9']
devices=[(router1,cmd1),(router2,cmd2),(router3,cmd3)]

for router in devices:
    execute(router[0],router[1])

end_for=time.time()

#multi threading uses threads
threads=list()
start_thread=time.time()
for router in devices:
        th = threading.Thread(target=execute, args=(router[0],router[1]))
        threads.append(th)

for th in threads:
    th.start()

for th in threads:
    th.join()
end_thread=time.time()
print(f'Total time Sequentially is {end_for-start_for}')
print(f'Total time Concurrently is {end_thread-start_thread}')
