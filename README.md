# Superscalar

Superscalar is a simple simulator of a processor that makes use Tomasulo's algorithm allowing over 1 instruction to be executed per 'cycle'.

## Architectural features

- **Pipelined execution** with six stages
  - Fetch, Decode, Issue, Dispatch, Execute, Writeback
- **n-way superscalar** execution
- **Out-of-order execution** using Tomasulo's algorithm and a reorder buffer
- **Non-blocking issue** to a unified reservation station (unless no reorder buffer or reservation station entries are free)
- **Register renaming** using the reorder buffer to relieve WAR and WAW dependencies
- **Load store queue** for in-order memory execution
- **Branch prediction**
  - Static not taken
  - Static taken
  - Dynamic 2-bit history and 2-bit saturating counter

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
