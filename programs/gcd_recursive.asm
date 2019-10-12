; int gcd(int a, int b) {
;   if (a == b) return a;
;   if (a > b) return gcd(a-b, b);
;   return gcd(a, b-a);
; }

gcd: