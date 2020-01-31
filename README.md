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

The instruction set is based on the MIPS instruction set. It allows indexed loads and stores and allows text labels. A simple vector addition program:

```assembly
.A: 0 1 2 3 4               ; int A[5] = {...}
.B: 0 1 2 3 4               ; int B[5] = {...}
.C: 0 0 0 0 0               ; int C[5] = {...}

    addi $0 $0 30           ; int n = 30
    addi $1 $1 1            ; int i = 1

for:
    lw $3 A($1)             ; $3 = A[i]
    lw $4 B($1)             ; $4 = B[i]
    add $5 $3 $4            ; $5 = A[i] + B[i]
    sw C($1) $5             ; c[i] = $5
    addi $1 $1 1            ; i++
    blt $1 $0 'for'         ; if (i < n) for loop again
```

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
