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
    'push' : 0x0E ,  # push c
    'pop'  : 0x0F ,  # pop  r1

    'b'    : 0x10 ,  # b    dst
    'beq'  : 0x11 ,  # beq  r1 r2 dst
    'bne'  : 0x12 ,  # bne  r1 r2 dst
    'bgt'  : 0x13 ,  # bgt  r1 r2 dst
    'bge'  : 0x14 ,  # bge  r1 r2 dst
    'blt'  : 0x15 ,  # blt  r1 r2 dst
    'ble'  : 0x16 ,  # ble  r1 r2 dst
    'j'    : 0x17 ,  # j    dst
    'jr'   : 0x18 ,  # jr   r1
    'jal'  : 0x19    # jal  r1
}

def strip_comments(assembly):
    stripped_assembly = ''
    for line in assembly.splitlines():
        line = line.strip()
        position = line.find(';')
        if len(line) > 0:
            if position > 0:
                stripped_assembly += (line[:position].strip() + '\n')
            elif position < 0:
                stripped_assembly += (line + '\n')
    return stripped_assembly

def replace_labels(assembly):
    labels = {}
    offset = 0
    final_assembly = ''
    for i, line in enumerate(assembly.splitlines()):
        if line.endswith(':'):
            labels[line[:-1]] = i - offset
            offset += 1
        else:
            final_assembly += line + '\n'
    for label, num in labels.items():
        final_assembly = final_assembly.replace("'" + label + "'", str(num))
    return final_assembly

file_name = 'programs/gcd_iterative.asm'
try:
    with open(file_name, 'r') as f:
        assembly = f.read()
except FileNotFoundError:
    print('File ' + file_name + ' does not exist.')
    exit()
    
print(assembly)
print('---------------')
print(replace_labels(strip_comments(assembly)))