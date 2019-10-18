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

    addi r1 r1 27           ; int a = 27
    addi r2 r2 39           ; int b = 39

while:
    beq r1 r2 'while_done'  ; while (a != b)
    ble r1 r2 'less_than'   ; if (a > b)
    sub r1 r1 r2            ; a = a - b
    j 'while'
less_than:                  ; else
    sub r2 r2 r1            ; b = b - a
    j 'while'

while_done:
    ; r1 contains a = gcd