#!/usr/bin/python
#Addition of header_list[8]

from os import walk
import sys, csv

NoHeaderFile = open('NoHeader.txt', 'w')
ConfigFile = open('Config.txt', 'w')
Template_Config = 'Dummy'
no_object = []
def collect_header(filename):
	""" collects Acls header data from the files """
	f = open(filename, 'r')
	header_present = 0
	no_sys = 1
	header_list = ['NA','NA','NA','NA','NA','NA', 'NA', 'NA', 'NA']
	header_list[0] = filename
	for line in f.readlines():
	    if "ON:" in line:
	    	header_present = 1
	        device_line = line.strip()
	        header_list[1] = device_line
	        print "\t[+] found Device info "
	    if "PUSH:" in line:
		header_present = 1
	        push_line = line.strip()
	        header_list[2] = push_line
	        print "\t[+] found PUSH file info "
	    if "OS:" in line:
	        header_present = 1
	        type_line = line.strip()
	        header_list[3] = type_line
	        print "\t[+] found TYPE info "
	    if "SCP:" in line:
	    	header_present = 1
	    	command_line = line.strip()
	    	header_list[4] = command_line
	    	print "\t[+] found Command info "
	    if "NETWORKS:" in line:
	    	header_present = 1
	    	command_line = line.strip()
	    	header_list[5] = command_line
	    	print "\t[+] found Network info "	    	
	    if "CONTACT:" in line:
	    	header_present = 1
	    	bz_line = line.strip()
	    	header_list[6] = bz_line
	    	print "\t[+] found BZ info "
	    if (("ingress" in line) and ("no" not in line)):
	    	header_list[7] = line.strip()
	    if (("remark Apple" in line) and ("DataCenter Nets" in line)):
	    	header_list[8] = line.strip()
	    if (("remark" in line) and ("DC-Subnets" in line)):
	    	header_list[8] = line.strip()
	f.close()
	if ((header_present == 1) and (no_sys == 1)):
		if (str(header_list[3]) == "!! OS: IOS"):
			for i in range(1,7):
				ConfigFile.write(header_list[i] + '\n')
			ConfigFile.write("\n" + str(header_list[7]) + "\n\n")
			ConfigFile.write("UNDER:" + str(header_list[8]) + "\n\n")
			ConfigFile.write("ADD: \n")
			ConfigFile.write("permit ip 10.53.0.0 0.0.255.255 any\n" )
			ConfigFile.write("permit ip 17.36.0.0 0.1.255.255 any\n" )
			ConfigFile.write("permit ip 17.56.0.0 0.0.255.255 any\n" )
			ConfigFile.write("---------------------------------------------------------------------------------------------------\n" )
			ConfigFile.write("\n")
		else:
			for i in range(1,7):
				ConfigFile.write(header_list[i] + '\n')
			ConfigFile.write("\n" + str(header_list[7]) + "\n\n")
			ConfigFile.write("UNDER:" + str(header_list[8]) + "\n\n")
			ConfigFile.write("ADD: \n")
			ConfigFile.write("permit ip 10.53.0.0/16 any\n" )
			ConfigFile.write("permit ip 17.36.0.0/15 any\n" )
			ConfigFile.write("permit ip 17.56.0.0/16 any\n" )
			ConfigFile.write("---------------------------------------------------------------------------------------------------\n" )
			ConfigFile.write("\n")			    
	if (header_present == 0):
		print "\t [-] No headers found"
		NoHeaderFile.write(header_list[0] + "\n")
	if no_sys == 0:
		global no_object
		no_object.append(filename)

def FileCheck(fn):
	""" Check if the file can be opened"""
    	try:
      		open(fn, "r")
      		return 1
    	except IOError:
      		print "Error: File does not appear to exist."
      		return 0

def Grab_Template(fn):
	""" Grab the template config to be updated in all the router acls files """
	t = open(fn, "r")
	global Template_Config
	Template_Config = t.read()
	t.close()

mypath = "/Users/pranaybomma/Desktop/Scripts/Whitelist/"
file_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    file_list.extend(filenames)
    break

#Grab_Template('Placeholder.txt')
print Template_Config

for x in file_list:
	if (("acls." in x) and (".py" not in x)):
		print "Looking in to file " + x
	        result = FileCheck(x)
		if result == 1:
			collect_header(x)

print " \n\n\n#########Files with no syslog object group are as below######### "
for i in no_object:
	print i

NoHeaderFile.close()
ConfigFile.close()
