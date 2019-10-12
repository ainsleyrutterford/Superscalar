opcodes = { 
    'nop'  : 0x00 ,  # nop

    'add'  : 0x01 ,  # add  r1 r2 r3 
    'addi' : 0x02 ,  # addi r1 r2 c
    'sub'  : 0x03 ,  # sub  r1 r2 r3
    'subi' : 0x04 ,  # subi r1 r2 c
    'mul'  : 0x05 ,  # mul  r1 r2 r3
    'div'  : 0x06 ,  # div  r1 r2 r3
    'and'  : 0x07 ,  # and  r1 r2 r3
    'or'   : 0x08 ,  # or   r1 r2 r3

    'ldw'  : 0x09 ,  # ldw  r1
    'lda'  : 0x0A ,  # lda
    'ldi'  : 0x0B ,  # ldi
    'stw'  : 0x0C ,  # stw
    'sta'  : 0x0D ,  # sta

    'b'    : 0x0E ,  # b    dst
    'beq'  : 0x0F ,  # beq  r1 r2 dst
    'bne'  : 0x10 ,  # bne  r1 r2 dst
    'bgt'  : 0x11 ,  # bgt  r1 r2 dst
    'bge'  : 0x12 ,  # bge  r1 r2 dst
    'blt'  : 0x13 ,  # blt  r1 r2 dst
    'ble'  : 0x14 ,  # ble  r1 r2 dst
    'j'    : 0x15 ,  # j    dst
    'jr'   : 0x16 ,  # jr   r1
    'jal'  : 0x17    # jal  r1
}

