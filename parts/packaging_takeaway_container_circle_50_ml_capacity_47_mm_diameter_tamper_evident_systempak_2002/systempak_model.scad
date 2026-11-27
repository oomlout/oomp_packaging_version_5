// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=28.9, d1=37.485, d2=44.1);
   translate([0,0,25.9]) cylinder(h=3, d=44.1);
   translate([0,0,22.9]) cylinder(h=2, d=47.5);
  }
  translate([0,0,1.2]) cylinder(h=31, d1=35.085, d2=41.7);
 }
}
module lid() {
 translate([0,0,28]) difference() {
  cylinder(h=3, d=48);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=44.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();

