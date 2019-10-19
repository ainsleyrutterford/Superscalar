import copy

import assembler
import processor

def main():
    f = open('programs/bubblesort.asm', 'r')
    assembly = f.read()

    program = assembler.replace_labels(assembler.strip_comments(assembly))
    cpu = processor.Processor()

    cpu_history = []

    while cpu.registers[10] == 0:
        instruction = cpu.fetch(program)
        cpu.execute(instruction)
        cpu.instructions_executed += 1
        cpu.cycles += 1
        cpu_history.append(copy.deepcopy(cpu))
    for i in range(10):
        print(str(cpu.registers[i]))
    print('')
    for i in range(10):
        print(str(cpu.data_memory[i]))

main()