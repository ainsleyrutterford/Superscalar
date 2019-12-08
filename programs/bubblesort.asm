; int A[10] = {8, 7, 0, 2, 1, 3, 6, 5, 4, 9}
; int n = 10
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

.A: 8 7 0 2 1 3 6 5 4 9     ; int A[10] = {...}

    addi $0 $0 10           ; int n = 10
    addi $1 $1 1            ; $1 = 1

while:
    blt $0 $1 'while_done'  ; while (n >= 1)
    addi $2 $2 0            ; int new_n = 0
    addi $3 $3 1            ; int i = 1
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
    blt $3 $0 'for'         ; if (i < n) for loop again
for_done:
    addi $0 $2 0            ; n = new_n
    j 'while'

while_done:
    addi $31 $31 1          ; set register 31 to 1 (halt)
