// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=136.5, d1=124.18499999999999, d2=146.1);
   translate([0,0,133.5]) cylinder(h=3, d=146.1);
   translate([0,0,130.5]) cylinder(h=2, d=149.5);
  }
  translate([0,0,1.2]) cylinder(h=138.6, d1=121.78499999999998, d2=143.7);
 }
}
module lid() {
 translate([0,0,135.6]) difference() {
  cylinder(h=3, d=150.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=146.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
module handle() {
 radius=75.0;
 z_top=131.5;
 for (angle=[0:8:172]) hull() {
  for (a=[angle,angle+8]) {
   translate([radius*cos(a), -radius*sin(a)-1.2, z_top-30.491999999999997*sin(a)])
    sphere(r=0.96,$fn=12);
  }
 }
}
if (component=="handle" || component=="assembled") handle();

