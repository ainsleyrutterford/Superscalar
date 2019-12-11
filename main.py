import assembler
import processor
import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('file', type=str, help="file containing the program to run")
parser.add_argument('-rob', action='store', dest='rob', type=int, default=32, help="size of redorder buffer")
parser.add_argument('-branch', action='store', dest='branch', default='two_bit', help="branch prediction scheme")
parser.add_argument('-width', action='store', dest='width', type=int, default=4, help="width of pipeline")

args = parser.parse_args()

try:
    file_name = args.file
    f = open(file_name, 'r')
    assembly = f.read()
except IOError:
    print('File "{0}" does not exist'.format(file_name))
    exit()

program = assembler.replace_labels(assembler.strip_comments(assembly))
cpu = processor.Processor(args.width, args.branch, args.rob)

while cpu.is_running():
    cpu.cycle(program)

print()
print(f'Registers: {cpu.rf[:32]}')
print(f'Memory:    {cpu.mem}')
print(f'Pipeline width:                {cpu.super}')
print(f'Instructions executed:         {cpu.executed}')
print(f'Cycles taken:                  {cpu.cycles}')

instructions_per_cycle = float(cpu.executed) / float(cpu.cycles)

print(f'IPC achieved:                  {instructions_per_cycle:.2f}')
print(f'Branch predixtion method:      {args.branch}')
print(f'Total branches:                {cpu.predictor.correct + cpu.predictor.incorrect}')
print(f'Correctly predicted:           {cpu.predictor.correct}')

distances = [cpu.predictor.branches[i + 1] - cpu.predictor.branches[i] for i in range(len(cpu.predictor.branches) - 1)]

if len(distances) == 0:
    average = float('inf')
    accuracy = 100
else:
    average = sum(distances) / len(distances)
    accuracy = 100 * cpu.predictor.correct / (cpu.predictor.correct + cpu.predictor.incorrect)

print(f'Branch prediction accuracy:    {accuracy:.1f}%')

print(f'Average branch distance:       {average:.1f}')
print()