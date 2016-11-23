import	os
import	sys

exe	= "qemu-arm"
stdout	= "qemu_stdout.txt"
stderr	= "qemu_stderr.txt"

# 	helper functions

def	run(binary):
	command  = exe + " -d in_asm,cpu " + binary + " > " + stdout + " 2> " + stderr
	os.system(command)
	return

def	parse_block_info():

	addrList = []

	fh = open(stderr, 'r') 

	srch4r15  = False
	srch4line = False

	lastLine  = ""	
	startAddr = 0
	finalAddr = 0	

	for line in fh:			

		if srch4line:

			count = count-1
		
			if count == 0:		
				srch4line = False				

				if line == "\n":
					startAddr = -1
				else:
					startAddr = int(line.split(':')[0],16)			
					#print "S: ", line
		
		if line == "\n":
			
			srch4r15 = True

			if startAddr == -1:						
				finalAddr = -1
			else:
				finalAddr = int(lastLine.split(':')[0],16)	
				#print "F: ", lastLine


		if "R15=" in line and srch4r15:
			
			startAddr2 = int(line.split("R15=")[1],16)

			if startAddr == -1:
				assert finalAddr == -1
				finalAddr = startAddr2 + 4
				print "Using arch state for block's start and final addresses ( ", startAddr2, " , ", finalAddr, " )"
			else:
				#make sure arch state matches block info
				assert startAddr == startAddr2			
	
			addrList.append( (startAddr2,finalAddr) )		
			srch4r15 = False

	
		if '----------------' in line:		
			srch4line  = True		
			count = 2

		lastLine = line	

	return	addrList

#	public functions

def	get_basic_blocks(binary):
	run(binary)
	return parse_block_info()

def	cleanUp():
	command = "rm " + stdout + " " + stderr + " 2> /dev/null"
	os.system(command)
	return
