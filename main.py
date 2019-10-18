import assembler

f = open('programs/gcd_iterative.asm', 'r')
assembly = f.read()

print(assembler.strip_comments(assembly))