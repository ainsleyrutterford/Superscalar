; int a = 27;
; int b = 39;
;
; int gcd(int a, int b) {
;   if (a == b) {
;     return a;
;   }
;   if (a > b) {
;     return gcd(a-b, b);
;   }
;   return gcd(a, b-a);
; }

    li $0 27               ; int a = 27
    li $1 39               ; int b = 39
    jal 'gcd'              ; call gcd(a, b)

gcd_done:                  ; return value is in $0
    li $31 1               ; set register 31 to 1 (halt)

gcd:
    bne $0 $1 'not_equal'  ; if (a == b)
    jr $29                 ; jump to return address
not_equal:
    ble $0 $1 'less_than'  ; if (a > b)
    sub $0 $0 $1           ; a = a - b
    jal 'gcd'              ; call gcd(a - b, b)
    j 'gcd_done'           ; return
less_than:
    sub $1 $1 $0           ; b = b - a
    jal 'gcd'              ; call gcd(a, b - a)
    j 'gcd_done'           ; return