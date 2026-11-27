// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=25.799999999999997, d1=36.635, d2=43.1);
   translate([0,0,22.799999999999997]) cylinder(h=3, d=43.1);
   translate([0,0,19.799999999999997]) cylinder(h=2, d=46.5);
  }
  translate([0,0,1.2]) cylinder(h=27.9, d1=34.235, d2=40.7);
 }
}
module lid() {
 translate([0,0,24.9]) difference() {
  cylinder(h=3, d=47);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=43.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();

