import sys
import os
import pwd
import grp
import time
import stat
from pathlib import Path

def change_group_executable(f):
	# takes in filepath, f and returns f with the execute permission
	# for group flipped
	current = os.stat(f).st_mode & 0o777
	oct_current = int(oct(current)[-2])

	if oct_current % 2 == 1:
		current -= 8
	else:
		current += 8

	os.chmod(f, current)

def get_perms(f):
	# returns a string with permissions related to file, f
	# e.g. /home/files/mode_604.txt Group Readable: False, Group Executable: False Size: 0, Owner: user, Group: user, last modified date: Aug 03  2022, last access date: Aug 03  2022
	status = os.stat(f)
	file_size = status.st_size
	group_perms = oct(status.st_mode)[-2]

	stat_info = os.stat(f)
	uid = stat_info.st_uid
	gid = stat_info.st_gid

	owner = pwd.getpwuid(uid)[0]
	group = grp.getgrgid(gid)[0]

	ti_m = os.path.getmtime(f)
	m_ti = time.ctime(ti_m)
	modified_date = m_ti[4:11] + m_ti[-5:]

	date = time.ctime(status[stat.ST_ATIME])
	access_date = date[4:11] + date[-5:]

	if modified_date[4] == ' ':
		modified_date = modified_date[:4] + '0' + modified_date[5:]
	if access_date[4] == ' ':
		access_date = access_date[:4] + '0' + access_date[5:]

	executable = False
	readable = False
	if group_perms == '1' or group_perms == '3' or group_perms == '5' or group_perms == '7':
		executable = True
	if group_perms == '4' or group_perms == '5' or group_perms == '6' or group_perms == '7':
		readable = True

	s = f'{f} Group Readable: {readable}, Group Executable: {executable} Size: {file_size}, Owner: {owner}, Group: {group}, last modified date: {modified_date}, last access date: {access_date}\n'
	return s

def main():
	#TODO
	filename = 'filelist.txt'
	if not(os.path.exists(filename)):
		g = open('output.txt', 'w')
		s = f"{filename} can not be found\n"
		g.write(s)
		g.close()
		sys.exit(0)

	with open(filename) as f:
		lines = f.readlines()

	g = open('output.txt', 'w')
	for i in range(len(lines)):
		lines[i] = lines[i][:-1]
		if os.path.exists(lines[i]):
			g.write(get_perms(lines[i]))
			change_group_executable(lines[i])
		else:
			g.write(f"{lines[i]} can not be found\n")

	g.close()


if __name__ == '__main__':
	main()
