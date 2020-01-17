# Superscalar

Superscalar is a simple simulator of a processor that makes use Tomasulo's algorithm allowing over 1 instruction to be executed per 'cycle'.

## Usage

Superscalar requires Python 3.4 or above.

```shell
$ python main.py programs/pi.asm
```

## Instruction set

- `add  r1 r2 r3`
- `addi r1 r2 c`
- `sub  r1 r2 r3`
- `subi r1 r2 c`
- `mul  r1 r2 r3`
- `imul r1 r2 r3`
- `div  r1 r2 r3`
- `idiv r1 r2 r3`
- `lw   r1 A(i)`
- `sw   A(i) r1`
- `beq  r1 r2 dst`
- `bne  r1 r2 dst`
- `blt  r1 r2 dst`
- `ble  r1 r2 dst`
- `j    dst`
