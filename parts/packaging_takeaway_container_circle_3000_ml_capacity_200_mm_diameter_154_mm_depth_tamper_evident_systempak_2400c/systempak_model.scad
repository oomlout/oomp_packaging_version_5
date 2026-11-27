// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=151.9, d1=166.685, d2=196.1);
   translate([0,0,148.9]) cylinder(h=3, d=196.1);
   translate([0,0,145.9]) cylinder(h=2, d=199.5);
  }
  translate([0,0,1.2]) cylinder(h=154.0, d1=164.285, d2=193.7);
 }
}
module lid() {
 translate([0,0,151.0]) difference() {
  cylinder(h=3, d=200.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=196.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
module handle() {
 radius=100.0;
 z_top=146.9;
 for (angle=[0:8:172]) hull() {
  for (a=[angle,angle+8]) {
   translate([radius*cos(a), -radius*sin(a)-1.2, z_top-33.88*sin(a)])
    sphere(r=0.96,$fn=12);
  }
 }
}
if (component=="handle" || component=="assembled") handle();

