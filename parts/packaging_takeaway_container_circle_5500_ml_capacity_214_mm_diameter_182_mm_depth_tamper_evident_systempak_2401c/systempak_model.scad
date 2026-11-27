// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=179.9, d1=188.785, d2=222.1);
   translate([0,0,176.9]) cylinder(h=3, d=222.1);
   translate([0,0,173.9]) cylinder(h=2, d=225.5);
  }
  translate([0,0,1.2]) cylinder(h=182.0, d1=186.385, d2=219.7);
 }
}
module lid() {
 translate([0,0,179.0]) difference() {
  cylinder(h=3, d=226.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=222.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
module handle() {
 radius=113.0;
 z_top=174.9;
 for (angle=[0:8:172]) hull() {
  for (a=[angle,angle+8]) {
   translate([radius*cos(a), -radius*sin(a)-1.2, z_top-40.04*sin(a)])
    sphere(r=0.96,$fn=12);
  }
 }
}
if (component=="handle" || component=="assembled") handle();

