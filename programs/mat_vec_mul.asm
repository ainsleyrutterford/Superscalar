; int A[9] = {1,2,3,4,5,6,7,8,9};
; int B[3] = {1,2,3};
; int C[3] = {0,0,0};
; int n = 3;

; for (int i = 0; i < n; i++) {
;   for (int j = 0; j < n; j++) {
;     C[i] = C[i] + A[j + i * n] * B[j];
;   }
; }

; $0 = 0
; i = $2
; j = $3

.A: 1 2 3 4 5 6 7 8 9
.B: 1 2 3
.C: 0 0 0

    addi $1 $1 3      ; int n = 3

for_y:
    add $3 $0 $0      ; j = 0
for_x:
    mul $4 $2 $1      ; $4 = i * n
    add $4 $4 $3      ; $4 = i * n + j
    lw $5 B($3)       ; $5 = B(j)
    lw $6 A($4)       ; $6 = A(i * n + j)
    lw $7 C($2)       ; $7 = C(i)
    mul $8 $6 $5      ; $8 = A(i * n + j) * B(j)
    add $8 $8 $7      ; $8 = C(i) + A(i * n + j) * B(j)
    sw C($2) $8       ; C(i) = C(i) + A(i * n + j) * B(j)
    addi $3 $3 1      ; j++
    blt $3 $1 'for_x' ; if (j < n), inner for loop again
    addi $2 $2 1      ; i++
    blt $2 $1 'for_y' ; if (i < n), outer for loop again

done:
    addi $31 $31 1    ; set register 31 to 1 (halt)