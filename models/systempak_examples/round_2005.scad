
$fn=96;
module body() {
 difference() {
  union() {
   cylinder(h=46, d1=60, d2=67);
   translate([0,0,45]) cylinder(h=5, d=68);
  }
  translate([0,0,1]) cylinder(h=50, d1=58, d2=65);
 }
}
module lid() {
 translate([0,0,49]) difference() {
  union() {
   cylinder(h=3, d=69);
   cylinder(h=0.8, d=69);
  }
  translate([0,0,-0.01]) cylinder(h=2.1, d=65.5);
 }
}
component="assembled";
if(component=="body" || component=="assembled") body();
if(component=="lid" || component=="assembled") lid();
