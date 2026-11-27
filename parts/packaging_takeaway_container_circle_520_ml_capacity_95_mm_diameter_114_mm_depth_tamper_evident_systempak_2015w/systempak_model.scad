// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=111.9, d1=77.43499999999999, d2=91.1);
   translate([0,0,108.9]) cylinder(h=3, d=91.1);
   translate([0,0,105.9]) cylinder(h=2, d=94.5);
  }
  translate([0,0,1.2]) cylinder(h=114.0, d1=75.03499999999998, d2=88.69999999999999);
 }
}
module lid() {
 translate([0,0,111.0]) difference() {
  cylinder(h=3, d=95.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=91.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();

