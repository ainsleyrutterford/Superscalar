; $0 = 12
; $1 = 7
; $2 = 4
; $3 = 2
; $4 = 9

;.A: 8 7 0 2 1 3 6 5 4 9     ; int A[10] = {...}

;    lw $10 A(7)
;    lw $11 A(8)
;    lw $12 A(9)
;    lw $2 A(1)
;    lw $1 A(8)
;    add $3 $2 $1    ; $3 = 11
;    sw A(9) $3
;    lw $15 A(5)
;    add $5 $2 $1    ; $5 = 11
;    sub $4 $5 $3    ; $4 = 0
;    mul $1 $4 $5    ; $1 = 0
;    lw $2 A(1)
;    mul $1 $2 $5    ; $1 = 77

    blt $1 $4 'for'
    add $3 $2 $1
    sub $4 $5 $3    ; $4 = 0
    mul $1 $4 $5    ; $1 = 0

for:
    add $4 $5 $6
    add $5 $2 $1    ; $5 = 11
    sub $4 $5 $3    ; $4 = 0
    mul $1 $4 $5    ; $1 = 0