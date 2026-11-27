// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=152.9, d1=132.685, d2=156.1);
   translate([0,0,149.9]) cylinder(h=3, d=156.1);
   translate([0,0,146.9]) cylinder(h=2, d=159.5);
  }
  translate([0,0,1.2]) cylinder(h=155.0, d1=130.285, d2=153.7);
 }
}
module lid() {
 translate([0,0,152.0]) difference() {
  cylinder(h=3, d=160.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=156.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
module handle() {
 radius=80.0;
 z_top=147.9;
 for (angle=[0:8:172]) hull() {
  for (a=[angle,angle+8]) {
   translate([radius*cos(a), -radius*sin(a)-1.2, z_top-34.1*sin(a)])
    sphere(r=0.96,$fn=12);
  }
 }
}
if (component=="handle" || component=="assembled") handle();

