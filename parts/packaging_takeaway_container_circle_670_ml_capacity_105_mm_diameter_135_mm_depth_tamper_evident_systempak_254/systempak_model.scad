// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=132.9, d1=85.93499999999999, d2=101.1);
   translate([0,0,129.9]) cylinder(h=3, d=101.1);
   translate([0,0,126.9]) cylinder(h=2, d=104.5);
  }
  translate([0,0,1.2]) cylinder(h=135.0, d1=83.53499999999998, d2=98.69999999999999);
 }
}
module lid() {
 translate([0,0,132.0]) difference() {
  cylinder(h=3, d=105.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=101.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();

