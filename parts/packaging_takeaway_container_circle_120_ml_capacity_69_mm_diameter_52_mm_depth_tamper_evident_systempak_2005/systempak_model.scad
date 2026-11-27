// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=49.9, d1=55.334999999999994, d2=65.1);
   translate([0,0,46.9]) cylinder(h=3, d=65.1);
   translate([0,0,43.9]) cylinder(h=2, d=68.5);
  }
  translate([0,0,1.2]) cylinder(h=52.0, d1=52.934999999999995, d2=62.699999999999996);
 }
}
module lid() {
 translate([0,0,49.0]) difference() {
  cylinder(h=3, d=69.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=65.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();

