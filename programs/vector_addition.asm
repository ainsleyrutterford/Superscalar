; int A[10] = {...};
; int B[10] = {...};
; int C[10] = {...};
; 
; for (int i = 0; i < 10; i++) {
;   C[i] = A[i] + B[i];
; }

.A: 0 1 2 3 4 5 6 7 8 9     ; int A[10] = {...}
.B: 0 1 2 3 4 5 6 7 8 9     ; int B[10] = {...}
.C: 0 0 0 0 0 0 0 0 0 0     ; int C[10] = {...}


    li $0 10                ; int n = 10
    li $1 1                 ; int i = 1

for:
    lw $3 A($1)             ; $3 = A[i]
    lw $4 B($1)             ; $4 = B[i]
    add $5 $3 $4            ; $5 = A[i] + B[i]
    sw C($1) $5             ; c[i] = $5
    addi $1 $1 1            ; i++
    blt $1 $0 'for'         ; if (i < n) for loop again

for_done:
    li $31 1                ; set register 31 to 1 (halt)
