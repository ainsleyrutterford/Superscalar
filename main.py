import assembler
import processor

f = open('programs/gcd_iterative.asm', 'r')
assembly = f.read()

program = assembler.replace_labels(assembler.strip_comments(assembly))
cpu = processor.Processor()

while cpu.data[100] == 0:
    instruction = cpu.fetch(program)
    cpu.execute(instruction)

print("gcd: " + str(cpu.data[100]))