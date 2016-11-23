#!/usr/bin/python

#	get_run_time.py
#
#	-
#
#	UT Austin, ECE Department
#
#	Author      : Kamyar Mirzazad-Barijough (kammirzazad@gmail.com)
#	Created  On : Jan 4th, 2016
#	Modified On : Jan 9th, 2016	[ checkpoint names are now sorted before search ]
#

import sys
import qemu	# see qemu.py
import gem5	# see gem5.py

from random import randint

if len(sys.argv) is not 2: 
	print "usage :", sys.argv[0], " [arm binary file]"
	exit() 

addrList = []
blockPairs = {}

def	cleanUp():
	qemu.cleanUp()
	gem5.cleanUp()
	return

def	get_total_run_time():

	total = 0

	for i in range(len(addrList)):	

		prevAddrStart = -1
		prevAddrFinal = -1
		nextAddrStart = -1
		nextAddrFinal = -1
		currAddrStart = addrList[i][0]
		currAddrFinal = addrList[i][1]

		# see if there is  preceding block
		if i != 0:
			prevAddrStart = addrList[i-1][0]
			prevAddrFinal = addrList[i-1][1]
	
		# see if there is succeeding block
		if i != len(addrList)-1:
			nextAddrStart = addrList[i+1][0]
			nextAddrFinal = addrList[i+1][1]
		
		currBlockPair = ( prevAddrStart, prevAddrFinal, currAddrStart, currAddrFinal )
		nextBlockPair = ( currAddrStart, currAddrFinal, nextAddrStart, nextAddrFinal )
		
		if not	blockPairs.has_key(currBlockPair):		
			#blockPairs[currBlockPair] = randint(0,9)
			blockPairs[currBlockPair] = gem5.get_block_run_time(sys.argv[1],currBlockPair,nextBlockPair)
				
		total += blockPairs[currBlockPair]		

	return	total

def	print_block_pairs():

	for i in range(len(addrList)-1):			

		if addrList[i][1] == (addrList[i+1][0]-4):

			print "- ( ", addrList[i][0], " , ", addrList[i][1], " ) => ( ", addrList[i+1][0], " , ", addrList[i+1][1], " )"		

		else:
			print "+ ( ", addrList[i][0], " , ", addrList[i][1], " ) => ( ", addrList[i+1][0], " , ", addrList[i+1][1], " )"	
	return	

########################## lets do real processing ###########################

# make sure everything is fine
cleanUp()

# generate address list
addrList = qemu.get_basic_blocks(sys.argv[1])

# some safety check 
#print_block_pairs()

total = get_total_run_time()
print "Total execution time :", total

# delete everything 
cleanUp()
