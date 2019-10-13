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

    ; int a = 27
    addi r1 r1 27
    ; int b = 39
    addi r2 r2 39

while:
    beq r1 r2 while_done
    ble r1 r2 less_than
    sub r1 r1 r2
    j while
less_than:
    sub r2 r2 r1
    j while

while_done:
    ; r1 contains a = gcd