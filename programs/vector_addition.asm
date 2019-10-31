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
    
    ; Do vector add here
    
    addi $1 $1 1            ; i++
    blt $1 $0 'for'         ; if (i < n) for loop again
    
for_done:
    li $10 1                ; set register 10 to 1
