// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=85.9, d1=109.73499999999999, d2=129.1);
   translate([0,0,82.9]) cylinder(h=3, d=129.1);
   translate([0,0,79.9]) cylinder(h=2, d=132.5);
  }
  translate([0,0,1.2]) cylinder(h=88.0, d1=107.33499999999998, d2=126.69999999999999);
 }
}
module lid() {
 translate([0,0,85.0]) difference() {
  cylinder(h=3, d=133.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=129.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();

