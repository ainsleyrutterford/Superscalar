; int a = 27;
; int b = 39;
;
; int gcd(int a, int b) {
;   if (a == b) return a;
;   if (a > b) return gcd(a-b, b);
;   return gcd(a, b-a);
; }

    addi r1 r1 27         ; int a = 27
    addi r2 r2 39         ; int b = 39

gcd:
    bne r1 r2 not_equal
    