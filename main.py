import assembler
import processor

f = open('programs/gcd_iterative.asm', 'r')
assembly = f.read()

program = assembler.replace_labels(assembler.strip_comments(assembly))

print(program)