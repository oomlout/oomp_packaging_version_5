// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=65.9, d1=96.985, d2=114.1);
   translate([0,0,62.900000000000006]) cylinder(h=3, d=114.1);
   translate([0,0,59.900000000000006]) cylinder(h=2, d=117.5);
  }
  translate([0,0,1.2]) cylinder(h=68.0, d1=94.585, d2=111.69999999999999);
 }
}
module lid() {
 translate([0,0,65.0]) difference() {
  cylinder(h=3, d=118.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=114.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();

