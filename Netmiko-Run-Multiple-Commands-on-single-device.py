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
