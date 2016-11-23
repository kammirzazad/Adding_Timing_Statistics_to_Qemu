int	main(int argc, char** argv)
{
	//m5_checkpoint(0,0);			// 1	0x109c4	68036

	asm
	(
//		"here: MRC  p1, 2, R0, c6, c0, 0\n\t"	
				
		"	MOV  r0, #19	\n\t"	// 2	0x109c8	68040
		"	MOV  r1, #18	\n\t"	// 3	0x109cc	68044
		"	MOV  r2, #17	\n\t"	// 4	0x109d0	68048
		"	MOV  r3, #16	\n\t"	// 5	0x109d4	68052
		"	MOV  r4, #15	\n\t"	// 6	0x109d8	68056
		"	MOV  r5, #14	\n\t"	// 7	0x109dc	68060	                
		"	MOVS r6, #13	\n\t"	// 8	0x109e0	68064
		"	BNE  L1		\n\t"	// 9	0x109e4	68068

		"	MOV  r7, #10	\n\t"	// 10	0x109e8	68072

                "       ADD  r0, r0, r0 \n\t"   // 11   0x109ec	68076
                "       ADD  r1, r1, r1 \n\t"   // 12   0x109f0	68080
                "       ADD  r2, r2, r2 \n\t"   // 13   0x109f4 68084	
                "       ADD  r3, r3, r3 \n\t"   // 14   0x109f8	68088
                "       ADD  r4, r4, r4 \n\t"   // 15   0x109fc	68092         
                "       ADD  r5, r5, r5 \n\t"   // 16   0x10a00	68096      	   
                "       ADD  r6, r6, r6 \n\t"   // 17   0x10a04	68100


		"L1:	MOV  r7, #11	\n\t"	// 10	0x10a08	68104
		
		"	ADD  r0, r0, r0	\n\t"	// 11	0x10a0c	68108
		"	ADD  r1, r1, r1	\n\t"	// 12	0x10a10	68112
		"	ADD  r2, r2, r2	\n\t"	// 13	0x10a14	68116
		"	ADD  r3, r3, r3	\n\t"	// 14	0x10a18	68120
		"	ADD  r4, r4, r4	\n\t"	// 15	0x10a1c	68124	
		"	ADD  r5, r5, r5	\n\t"	// 16	0x10a20	68128			
		"	ADD  r6, r6, r6	\n\t"	// 17	0x10a24	68132
		
//		"MRC  p1, 2, R0, c7, c0, 0\n\t"
	);	

	printf("Hi there\n");

	return 0;
}
