import assembler
import copy
import processor
import sys

def main():

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

    cpu_history = []

    while cpu.registers[10] == 0:
        instruction = cpu.fetch(program)            # fetch
        opcode, operands = cpu.decode(instruction)  # decode
        cpu.execute(opcode, operands)               # execute
        cpu.instructions_executed += 1
        cpu_history.append(copy.deepcopy(cpu))
    print(cpu.registers)
    print(cpu.data_memory)
    print('{0} instructions executed in {1} cycles.'.format(cpu.instructions_executed, cpu.cycles))
    instructions_per_cycle = float(cpu.instructions_executed) / float(cpu.cycles)
    print('{0:.2f} instructions per cycle achieved.'.format(instructions_per_cycle))

main()