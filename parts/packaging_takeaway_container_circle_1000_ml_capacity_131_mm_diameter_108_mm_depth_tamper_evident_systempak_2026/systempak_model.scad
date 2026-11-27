// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=105.9, d1=109.73499999999999, d2=129.1);
   translate([0,0,102.9]) cylinder(h=3, d=129.1);
   translate([0,0,99.9]) cylinder(h=2, d=132.5);
  }
  translate([0,0,1.2]) cylinder(h=108.0, d1=107.33499999999998, d2=126.69999999999999);
 }
}
module lid() {
 translate([0,0,105.0]) difference() {
  cylinder(h=3, d=133.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=129.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
module handle() {
 radius=66.5;
 z_top=100.9;
 for (angle=[0:8:172]) hull() {
  for (a=[angle,angle+8]) {
   translate([radius*cos(a), -radius*sin(a)-1.2, z_top-23.76*sin(a)])
    sphere(r=0.96,$fn=12);
  }
 }
}
if (component=="handle" || component=="assembled") handle();

