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

    li $0 10                ; int n = 10
    li $1 1                 ; $1 = 1

while:
    blt $0 $1 'while_done'  ; while (n >= 1)
    li $2 0                 ; int new_n = 0
    li $3 1                 ; int i = 1
for:
    li $4 0                 ; $4 = 0 THINK I CAN REMOVE THIS? TEST AND SEE
    sub $4 $3 $1            ; $4 = i-1
    lw $5 A($4)             ; $5 = A[i-1]
    lw $6 A($3)             ; $6 = A[i]
    ble $5 $6 'less_than'   ; if (A[i-1] > A[i])
    move $7 $5              ; int temp = A[i-1]
    sw A($4) $6             ; A[i-1] = A[i]
    sw A($3) $7             ; A[i] = temp
    move $2 $3              ; new_n = i
less_than:                  ; A[i-1] <= A[i]
    addi $3 $3 1            ; i++
    blt $3 $0 'for'         ; if (i < n) for loop again
for_done:
    move $0 $2              ; n = new_n
    j 'while'

while_done:
    li $31 1                ; set register 31 to 1 (halt)
