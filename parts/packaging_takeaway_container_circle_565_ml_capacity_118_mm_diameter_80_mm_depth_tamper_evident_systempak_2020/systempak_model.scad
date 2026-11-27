// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=77.9, d1=96.985, d2=114.1);
   translate([0,0,74.9]) cylinder(h=3, d=114.1);
   translate([0,0,71.9]) cylinder(h=2, d=117.5);
  }
  translate([0,0,1.2]) cylinder(h=80.0, d1=94.585, d2=111.69999999999999);
 }
}
module lid() {
 translate([0,0,77.0]) difference() {
  cylinder(h=3, d=118.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=114.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();

