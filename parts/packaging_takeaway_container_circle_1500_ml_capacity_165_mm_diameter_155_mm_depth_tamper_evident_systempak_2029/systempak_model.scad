// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=152.9, d1=136.935, d2=161.1);
   translate([0,0,149.9]) cylinder(h=3, d=161.1);
   translate([0,0,146.9]) cylinder(h=2, d=164.5);
  }
  translate([0,0,1.2]) cylinder(h=155.0, d1=134.535, d2=158.7);
 }
}
module lid() {
 translate([0,0,152.0]) difference() {
  cylinder(h=3, d=165.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=161.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
module handle() {
 radius=82.5;
 z_top=147.9;
 for (angle=[0:8:172]) hull() {
  for (a=[angle,angle+8]) {
   translate([radius*cos(a), -radius*sin(a)-1.2, z_top-34.1*sin(a)])
    sphere(r=0.96,$fn=12);
  }
 }
}
if (component=="handle" || component=="assembled") handle();

