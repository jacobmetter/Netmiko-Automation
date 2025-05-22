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
