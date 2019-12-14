    addi $0 $0 90           ; int n = 90
    addi $1 $1 1            ; int i = 1

for:
    addi $1 $1 1            ; i++
    add $4 $3 $2
    add $7 $6 $5
    add $10 $9 $8
    add $13 $12 $11
    add $16 $15 $14
    add $19 $18 $17
    add $22 $21 $20
    add $25 $24 $23
    blt $1 $0 'for'         ; if (i < n) for loop again

    addi $31 $31 1          ; set register 31 to 1 (halt)