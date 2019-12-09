; int A[9] = {1,2,3,4,5,6,7,8,9};
; int B[9] = {1,2,3,4,5,6,7,8,9};
; int C[9] = {0,0,0,0,0,0,0,0,0};
; int n = 3;

; for (int i = 0; i < n; i++) {
;   for (int j = 0; j < n; j++) {
;     for (int k = 0; k < n; k++) {
;       C[j + i * n] += A[k + i * n] * B[j + k * n];
;     }
;   }
; }

; $0 = 0
; i = $2
; j = $3
; k = $4

.A: 1 2 3 4 5 6 7 8 9
.B: 1 2 3 4 5 6 7 8 9
.C: 0 0 0 0 0 0 0 0 0

    addi $1 $1 3      ; int n = 3

for_i:
    add $3 $0 $0      ; j = 0
for_j:
    add $4 $0 $0      ; k = 0
for_k:
    mul $5 $2 $1      ; $5 = i * n
    mul $6 $4 $1      ; $6 = k * n
    add $7 $3 $5      ; $7 = j + i * n
    add $8 $4 $5      ; $8 = k + i * n
    add $9 $3 $6      ; $9 = j + k * n
    lw $10 C($7)      ; $10 = C(j + i * n)
    lw $11 A($8)      ; $11 = A(k + i * n)
    lw $12 B($9)      ; $12 = B(j + k * n)
    mul $13 $11 $12   ; $13 = A(k + i * n) * B(j + k * n)
    add $13 $13 $10   ; $13 = C(j + i * n) + A(k + i * n) * B(j + k * n)
    sw C($7) $13      ; C(j + i * n) = C(j + i * n) + A(k + i * n) * B(j + k * n)
    addi $4 $4 1      ; k++
    blt $4 $1 'for_k' ; if (k < n), inner for loop again
    addi $3 $3 1      ; j++
    blt $3 $1 'for_j' ; if (j < n), inner for loop again
    addi $2 $2 1      ; i++
    blt $2 $1 'for_i' ; if (i < n), outer for loop again

done:
    addi $31 $31 1    ; set register 31 to 1 (halt)