; int a = 2790;
; int b = 3990;

; while (a != b) {
;   if (a > b) {
;     a = a – b;
;   } else {
;     b = b – a;
;   }
; }
; return a;

    addi $0 $0 2790         ; int a = 2790
    addi $1 $1 3990         ; int b = 3990

while:
    beq $0 $1 'while_done'  ; while (a != b)
    ble $0 $1 'less_than'   ; if (a > b)
    sub $0 $0 $1            ; a = a - b
    j 'while'
less_than:                  ; else
    sub $1 $1 $0            ; b = b - a
    j 'while'

while_done:
    addi $10 $0 0           ; $10 contains a = gcd
    addi $31 $31 1          ; set register 31 to 1 (halt)