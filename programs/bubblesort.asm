; int A[30] = {...}
; int n = 30
; 
; while (n >= 1) {
;   int new_n = 0
;   for (int i = 1; i < n; i++) {
;     if (A[i-1] > A[i]) {
;       int temp = A[i-1];
;       A[i-1] = A[i];
;       A[i] = temp;
;       new_n = i
;     }
;   }
;   n = new_n
; }

.A: 8 14 7 22 15 1 25 13 23 24 2 25 30 9 19 28 3 23 21 19 28 24 9 6 29 12 4 29 19 24    ; int A[30] = {...}

    addi $10 $10 30         ; int n = 30
    addi $1 $1 1            ; $1 = 1

while:
    blt $10 $1 'while_done' ; while (n >= 1)
    add $2 $0 $0            ; int new_n = 0
    add $3 $1 $0            ; int i = 1
for:
    sub $4 $3 $1            ; $4 = i-1
    lw $5 A($4)             ; $5 = A[i-1]
    lw $6 A($3)             ; $6 = A[i]
    ble $5 $6 'less_than'   ; if (A[i-1] > A[i])
    addi $7 $5 0            ; int temp = A[i-1]
    sw A($4) $6             ; A[i-1] = A[i]
    sw A($3) $7             ; A[i] = temp
    addi $2 $3 0            ; new_n = i
less_than:                  ; A[i-1] <= A[i]
    addi $3 $3 1            ; i++
    blt $3 $10 'for'        ; if (i < n) for loop again
for_done:
    addi $10 $2 0           ; n = new_n
    j 'while'

while_done:
    addi $31 $31 1          ; set register 31 to 1 (halt)
