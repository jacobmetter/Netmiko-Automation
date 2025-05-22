# Netmiko-Automation
This is a folder of Python programs where I use Netmiko to remote connect to Cisco devices in GNS3 and run automation commands.

## Netmiko Enable Interface on a Single Router

Netmiko and Paramiko are very similar in terms of what they do. Both are programs used in Python to automate tasks by sending commands to routers and switches using Putty. However, Netmiko is is an open-source, Python MIT-licensed library designed to interact with a wide range of network devices (Cisco, Juniper, Arista, Huawei, and many others. It hides low-level differences between different vendors and provides a high-level API that exposes common behaviors of many web CLI shells (e.g. the existence of operational/configuration modes) in a consistent way. I also find Netmiko to be much simplier to understand in terms of set up. Our first code that I did was a simple connect to a router and enable an interface. 

![image](https://github.com/user-attachments/assets/4ab93334-a127-4946-8b17-2dac5e6bc351)

Shown above is the set up I will be using for this project. The python script to enable interface is as follows:

    from netmiko import ConnectHandler

    cisco_device= {
            'device_type':'cisco_ios',
            'host':'10.1.2.20',
            'username':'admin',
            'password': 'cisco',
            'port':22,
            'secret':'cisco',
        'verbose':True
        }
    connection=ConnectHandler(**cisco_device)
    prompt=connection.find_prompt()
    print('Entering the enable mode..')

    if '>' in prompt:
        connection.enable()

    interface=input('Please enter the interface you want to enable: ')
    output=connection.send_command('sh ip interface ' + interface)

    if 'Invalid input detected' in output:
        print('You entered an invalid interface.')
    else:
        first_line=output.splitlines()[0]
        print(first_line)
    if not 'up' in first_line:
        print('The interface is down, enabling interface...')
        commands=['int '+ interface, 'no shut','exit']
        output=connection.send_config_set(commands)
        print(output)
        print('#'*30)
        print('The interface has been enabled')
    else:
        print('Interface '+ interface + ' is already enabled')
    print('Disconnecting Connection...')
    connection.disconnect()

Netmiko uses a command called ConnectHandler to connect to your device via SSH. Which is much simpler compared to Paramiko where you have to enter three lines of code to execute the same function. From there we connect to the device using given info about the router (this has to be already set up on the router, you cannot execute commands on a "brand new" router"). From there using a variable called prompt you can see what privilage level you are in, so with the first if statement we immediatly go to enable. We ask the user for what interface they want to enable, and they either give a valid interface and it gets  turned on, or the user gives and invalid input and nothing is returned. Running the script we get this.

![image](https://github.com/user-attachments/assets/f884fd8c-d68c-4cd9-a8c9-83e79152c224)

As shown, the script runs and enables the interface i inputted (e0/3) with no errors.

## Netmiko Running Multiple Commands on a Device 

Running multiple commands on a single device is very straightforward. Unlike in Paramiko, you cannot use shell.send() or a similar command, instead you have to make a list of commands and use the function connection.send_config_set(commands). The code for a basic list of commands should look like this:

     from netmiko import ConnectHandler
    cisco_device={'device_type':'cisco_ios','host':'10.1.2.10','username':'u1',
                  'password':'cisco','port':22,'secret':'cisco','verbose':True}
    
    connection=ConnectHandler(**cisco_device)
    
    print('Entering the enable mode..')
    connection.enable() #enters enable mode
    
    commands=['ip ssh ver 2; access-list 1 permit any; ip domain-name network-automation.io']
    
    output=connection.send_config_set(commands) #converts the string of cmd into a list, another way to send commands
    print(output)
    
    connection.send_command('write memory') #how you save the configuration
    print('Closing Connection')
    connection.disconnect()

![image](https://github.com/user-attachments/assets/4bd5db68-eeda-4886-9fe6-302f51026d79)


In this example, I enables ssh version 2 and created an access-list as well as a domain name. But with this we can send as many commands as we need to configure our devices. 

## Netmiko Configuring a Device From a File

The next step is sending basic .txt files to the script and running the commands to a single device. It will look something like this:

    from netmiko import ConnectHandler
    
    cisco_device={'device_type':'cisco_ios','host':'10.1.2.10','username':'u1',
                  'password':'cisco','port':22,'secret':'cisco','verbose':True}
    
    connection=ConnectHandler(**cisco_device)
    print('Entering the enable mode..')
    connection.enable() #enters enable mode
    
    print('Sending commands from file...')
    output=connection.send_config_from_file('ospf.txt') #sends the .txt file to the router
    print(output) #allows you to see every command sent to the router in the terminal
    print('Closing Connection')
    connection.disconnect()

The major difference from this and the code from the previous project is the command connection.send_config_from_file(file_name) this reads a simple text file and executes the commands sequentially. This is good for configuring a new device added to an already existing network. What about if we need to configure multiple devices?

## Netmiko Configuring Multiple Routers with Multiple files

To do this we will need to use for loops to iterate over each router that we want to configure in each subnet. On top of that, while we are iterating we need to make sure each router gets the correct config file. We can do that by entering the names or paths of the config files into the Python interface. Since we are now dealing with multiple routers, I adjust the lab enviornment to look like the following:

![image](https://github.com/user-attachments/assets/1dd6ecfa-7db2-41c6-a07c-17bac5100e77)

Now we have three routers in the 10.1.2.0 subnet. Let's configure them using different .txt files with different commands. The python script will look something like this:

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

![image](https://github.com/user-attachments/assets/527ee614-70e0-417a-9d4a-a46768819964)

![image](https://github.com/user-attachments/assets/e63afb21-1a9d-4851-bfd2-0eda17b84fba)

![image](https://github.com/user-attachments/assets/b90d5e89-c0fc-47e2-ade8-1da191a455f6)

As you can see, each router got a different configuration from the three different files I inputted. However, what if we needed to send configs to 100 or more routers? doing each one sequentially is too slow and will take too long. Which is why we need to impliment threading to run all commands concurrently, greatly speeding up config times.

## Netmiko and Multithreading

Multithreading is when you send commands to all devices at the same time, rather than sequentially. This is very beneficial because it greatly speeds up the time it takes to configure devices. So if you are in a new enviornment and you have to configure 100 devices. You can use multithreading to speed up the process. The following python code shows the difference in time between multithreading and non multipthreading scripts:

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

![image](https://github.com/user-attachments/assets/cd80ff56-61cb-4860-bf5e-8a3b88dcd745)

As you can see, running multithreading is almost 3x faster than running the program sequentially. The downside is it takes up more processing power and requires high quality computers to run it at high volumes.

