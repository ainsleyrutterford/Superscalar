; int a = 27;
; int b = 39;
; while (a != b) {
;   if (a > b) {
;     a = a – b;
;   } else {
;     b = b – a;
;   }
; }
; return a;

    addi $0 $0 27           ; int a = 27
    addi $1 $1 39           ; int b = 39

while:
    beq $0 $1 'while_done'  ; while (a != b)
    ble $0 $1 'less_than'   ; if (a > b)
    sub $0 $0 $1            ; a = a - b
    j 'while'
less_than:                  ; else
    sub $1 $1 $0            ; b = b - a
    j 'while'

while_done:
    add $100 $100 $0        ; %100 contains a = gcd