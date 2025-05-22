from netmiko import ConnectHandler

cisco_device= {
            'device_type':'cisco_ios',
            'host':'10.1.2.10',
            'username':'u1',
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
