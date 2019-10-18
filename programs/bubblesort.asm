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

.array A: 8, 7, 0, 2, 1, 3, 6, 5, 4, 9  ; int A[10] = {...}

    li $0 10                            ; int n = 10
    li $1 1                             ; $1 = 1

while:
    blt $0 $1 'while_done'              ; while (n >= 1)
    li $2 0                             ; int new_n = 0
    li $3 1                             ; int i = 1
for:
    ble A[i-1] A[i] 'less_than'         ; if (A[i-1] > A[i])
    move $4 A[i-1]                      ; int temp = A[i-1]
    move A[i-1] A[i]                    ; A[i-1] = A[i]
    move A[i] $4                        ; A[i] = temp
    move $2 $3                          ; new_n = i
less_than:                              ; A[i-1] <= A[i]
    addi $3 1                           ; i++
    bge $3 $0 'for_done'                : end for loop if (i >= n)
for_done:
    move $0 $2                          ; n = new_n

while_done:
