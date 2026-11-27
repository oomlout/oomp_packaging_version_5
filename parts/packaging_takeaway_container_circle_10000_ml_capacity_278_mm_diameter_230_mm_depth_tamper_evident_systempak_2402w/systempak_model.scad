// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=227.9, d1=232.985, d2=274.1);
   translate([0,0,224.9]) cylinder(h=3, d=274.1);
   translate([0,0,221.9]) cylinder(h=2, d=277.5);
  }
  translate([0,0,1.2]) cylinder(h=230.0, d1=230.585, d2=271.70000000000005);
 }
}
module lid() {
 translate([0,0,227.0]) difference() {
  cylinder(h=3, d=278.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=274.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
module handle() {
 radius=139.0;
 z_top=222.9;
 for (angle=[0:8:172]) hull() {
  for (a=[angle,angle+8]) {
   translate([radius*cos(a), -radius*sin(a)-1.2, z_top-50.6*sin(a)])
    sphere(r=0.96,$fn=12);
  }
 }
}
if (component=="handle" || component=="assembled") handle();

