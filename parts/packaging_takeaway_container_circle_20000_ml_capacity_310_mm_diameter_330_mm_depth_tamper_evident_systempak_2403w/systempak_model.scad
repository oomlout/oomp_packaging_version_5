// Millimetres. Z=0 at base. Supplier envelope; wall and draft estimated.
$fn=72;
component="assembled";
module body() {
 difference() {
  union() {
   cylinder(h=327.9, d1=260.185, d2=306.1);
   translate([0,0,324.9]) cylinder(h=3, d=306.1);
   translate([0,0,321.9]) cylinder(h=2, d=309.5);
  }
  translate([0,0,1.2]) cylinder(h=330.0, d1=257.785, d2=303.70000000000005);
 }
}
module lid() {
 translate([0,0,327.0]) difference() {
  cylinder(h=3, d=310.0);
  translate([0,0,-.01]) cylinder(h=1.9500000000000002, d=306.6);
 }
}
if (component=="body" || component=="assembled") body();
if (component=="lid" || component=="assembled") lid();
module handle() {
 radius=155.0;
 z_top=322.9;
 for (angle=[0:8:172]) hull() {
  for (a=[angle,angle+8]) {
   translate([radius*cos(a), -radius*sin(a)-1.2, z_top-72.6*sin(a)])
    sphere(r=0.96,$fn=12);
  }
 }
}
if (component=="handle" || component=="assembled") handle();

