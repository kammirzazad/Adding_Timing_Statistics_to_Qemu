import os
import sys
import glob

exe		= "build/ARM/gem5.opt"
config		= "configs/example/se.py"
stderr		= "gem5_stderr.txt"

outdir		= "m5out/"
path2gem5	= "/home/osboxes/Documents/gem5-qemu-v0/"

cpu_flag        = "--cpu-type=minor"
mem_flag        = "--mem-type=SimpleMemory"        # currently not used
cache_flag      = "--caches"
debug_flag      = "--debug-flags=MinorSteer,MinorCommit"
restore_flag    = "--restore-with-cpu=minor"
checkpoint_flag = "--checkpoint-at-end"


def	get_commit(blockPair):
	
	fn  =	outdir 
	fn +=	"MinorCommit"	  + "_"	
	fn +=	str(blockPair[0]) + "_"			
	fn +=	str(blockPair[1]) + "_"
	fn +=	str(blockPair[2]) + "_"
	fn +=	str(blockPair[3]) + ".txt"
	
	return	fn

def	print_all():

	checkpoints = glob.glob( outdir + "cpt*" )
	checkpoints.sort()
	print checkpoints

def	get_checkpoint(addr):

	if addr == -1:
		return 0

	checkpoints = glob.glob( outdir + "cpt*" )
	checkpoints.sort()

	for i in range(len(checkpoints)):
	
		fh = open(checkpoints[i]+"/m5.cpt",'r')
	
		for line in fh:			
			if ("_pc=" + str(addr)) in line:	

				print "Using checkpoint", (i+1), "[", checkpoints[i], "]"
				fh.close()
				return (i+1)	
		fh.close()	

	return 0

def	get_inst_count(blockPair):	

	# special case : current block has no predecessor
	if blockPair[0] == -1 and blockPair[1] == -1:

		return ( (blockPair[3] - blockPair[2]) / 4 ) + 1					

	assert blockPair[0] != -1 and blockPair[1] != -1 

	# not-taken 
        if blockPair[1]==(blockPair[2]-4):

		return ( abs(blockPair[3] - blockPair[0]) / 4 ) + 1

        # taken        
	return ( (blockPair[1] - blockPair[0]) / 4 ) + ( (blockPair[3] - blockPair[2]) / 4 ) + 2

def	gen_steering(blockPair,suffix):

	# special case : there is no need to steer branches/branchPredictor if current block has no predecessor
	if blockPair[0] == -1 and blockPair[1] == -1:
		return	
	
	assert blockPair[0] != -1 and blockPair[1] != -1	

	cond_fh	   = open("cond_"    + str(blockPair[1]) + "_" + suffix + ".txt", 'w')
	target_fh  = open("target_"  + str(blockPair[1]) + "_" + suffix + ".txt", 'w')
	predict_fh = open("predict_" + str(blockPair[1]) + "_" + suffix + ".txt", 'w')	
	
	# not-taken
	if blockPair[1]==(blockPair[2]-4):

		cond_fh.write("0\n")
		predict_fh.write("0\n")
	# taken
	else:
		cond_fh.write("1\n")		
		target_fh.write(str(blockPair[2])+"\n");
		predict_fh.write("1\n")
		predict_fh.write(str(blockPair[2])+"\n")
			
	cond_fh.close()			
	target_fh.close()	
	predict_fh.close()
	return	

def	setup():
	command = "mkdir -p " + outdir
	os.system(command)
	return

def	intermediate_cleanUp():
	command = "rm " + stderr + " cond_* target_* predict_* 2> /dev/null"
	os.system(command)
	return
	
def     run(binary,blockPair,cpt):
	
	# add common commandline options
	command   =	path2gem5 + exe			+ " "	
	command  +=	debug_flag			+ " "		 	
	command  +=	path2gem5 + config		+ " "
	command  +=	"-c"				+ " "
	command  +=	binary				+ " "	
	command  +=	"-I"				+ " "
	command  +=	str(get_inst_count(blockPair))	+ " "	
	command	 += 	cpu_flag			+ " "
	command  +=	mem_flag			+ " "	
	command  +=	cache_flag			+ " "	
	command  +=	checkpoint_flag			+ " "			

	# add restore specific flags
	if cpt != 0:			
		command += restore_flag			+ " "	 		
		command += "-r"				+ " "
		command += str(cpt)			+ " "		
			
	# direct stdout and stderr	
	command  +=	">"				+ " "
	command  +=	get_commit(blockPair)		+ " "
	command  +=	"2>"				+ " "
	command  +=	stderr				+ " "						

	os.system(command)	
        return

def     parse_commit_info(blockPair):

	fh = open(get_commit(blockPair), 'r')

	start_time = -1
	final_time = -1

        start_addr_hex = hex(blockPair[2]).split('x')[1]
        final_addr_hex = hex(blockPair[3]).split('x')[1]

        for line in fh:

                if "MinorCommit" in line and start_addr_hex in line:
                        start_time = int(line.split(':')[0])

                if "MinorCommit" in line and start_addr_hex in line:
                        final_time = int(line.split(':')[0])

	fh.close()

        return (final_time - start_time)

def	cleanUp():	
	command = "rm -r " + outdir + " 2> /dev/null"
	os.system(command)	
	return

def	get_block_run_time(binary,currBlockPair,nextBlockPair):

	print "Measuring runtime of block pair [ (", currBlockPair[0], ",", currBlockPair[1], ") , (", currBlockPair[2], ",", currBlockPair[3], ") ] followed by (", nextBlockPair[2], ",", nextBlockPair[3], ")"

	assert currBlockPair[2] == nextBlockPair[0] and currBlockPair[3] == nextBlockPair[1]		

	# create output directory
	setup()

	# generate files required to steer simulator
	gen_steering(currBlockPair,'a')
	gen_steering(nextBlockPair,'b')

	print "Generating checkpoint with pc=", nextBlockPair[2], " with ", get_inst_count(currBlockPair), " instructions"

	# run gem5
	run(binary,currBlockPair,get_checkpoint(currBlockPair[0]))	# FIXME: Not sure about checkpoint

	print_all()

	if sys.stdin.read(1) == 'c':
		"Exiting...."	
		exit()

	# remove files we do not need anymore
	intermediate_cleanUp()		
	# get execution time from output file
	return parse_commit_info(currBlockPair)
