all:
	arm-linux-gnueabi-gcc -mcpu=cortex-a15 -DUNIX -static test.c -o test.o ../gem5-qemu-v0/util/m5/m5op_arm.S
