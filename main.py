import assembler
import processor
import sys


if (sys.version_info[0] < 3):
    print('Python 3 or a more recent version is required')
    print('Try: python3 main.py')
    exit()

if (len(sys.argv) != 2):
    print('Usage: python3 main.py <program.asm>')
    exit()

try:
    file_name = sys.argv[1]
    f = open(file_name, 'r')
    assembly = f.read()
except IOError:
    print('File "{0}" does not exist'.format(file_name))
    exit()

program = assembler.replace_labels(assembler.strip_comments(assembly))
cpu = processor.Processor()

while cpu.is_running():
    cpu.cycle(program)

# while(1):
#     input()
#     print('Cycling cpu...')
#     cpu.cycle(program)

print(f'Registers: {cpu.rf[:32]}')
print(f'Memory: {cpu.mem}')
print(f'{cpu.executed} instructions executed in {cpu.cycles} cycles.')
instructions_per_cycle = float(cpu.executed) / float(cpu.cycles)
print(f'{instructions_per_cycle:.2f} instructions per cycle achieved.')