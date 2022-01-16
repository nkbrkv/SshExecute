import paramiko
import sys
import getpass
import os.path
import datetime

host = '---'
name = 'uateam'
secret = '/home/%s/.ssh/-----' % getpass.getuser()


def runCommand(command, list):


	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(host, username = name, key_filename = secret)
	date = datetime.datetime.now()
	date = date.strftime("%c")
	filename = 'Report_%s.txt' % date.replace(' ','_')
	f = open(filename, 'w')

	for i in range(0, len(list)):
		try:
			current_command = "ssh root@priv.%s '%s'" % (list[i], command)
			stdin, stdout, stderr = ssh.exec_command(current_command)
			log = stdout.readlines()
			log = [x.encode('utf-8') for x in log]
			log = [x.strip() for x in log]
			f.write('START REPORT FROM - %s\n\n%s\n\nEND REPORT\n\n\n' % (list[i], '\n'.join(log)))

		except Exception:
			print('Error!')

		else: 
			print('%s ... Done' % list[i])

	f.close()
	sftp = ssh.open_sftp()
	remotepath = '/home/uateam/scripts/Reports/%s' % filename
	localpath = './%s' % filename
	sftp.put(localpath, remotepath)
	sftp.close()
	ssh.close()


def getListServers():
	if os.path.exists('list.txt') != True:

			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(host, username = name, key_filename = secret)
			stdin, stdout, stderr = ssh.exec_command('cat /home/uateam/scripts/list.txt')
			data = stdout.readlines()
			data = [x.encode('utf-8') for x in data]
			data = [x.strip() for x in data]

			with open('list.txt', 'w') as fw:
    				for item in data:
        				fw.write('%s\n' % item)
			ssh.close()

	with open('list.txt') as f:
    		content = f.readlines()

    	content = [x.strip() for x in content]

	return content
  	


print('''
	#####################################
	Powered by Nikolay
	Quick execute command on all servers:
	#####################################\n\n
	1. Run command on all servers
	
	''')

operation_type = input('Please select operation: ')

if operation_type == 1:

	print('You selected 1 operation')
	command = raw_input('Please enter command to execute: ')
	check = raw_input('Was the command "%s" entered correctly?(yes/no): ' % command)

	if command != 0 and check == 'yes':
		runCommand(command, getListServers())
	else:
		print('Error, try again!')

else:
	sys.exit(0)


