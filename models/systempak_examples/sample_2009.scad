
$fn=96;
module body() {
 difference() {
  union() {
   cylinder(h=39, d1=83, d2=93);
   translate([0,0,38]) cylinder(h=5, d=94);
  }
  translate([0,0,1]) cylinder(h=43, d1=81, d2=91);
 }
}
module lid() {
 translate([0,0,42]) difference() {
  cylinder(h=3, d=95);
  translate([0,0,-0.01]) cylinder(h=2.1, d=91.5);
 }
}
component="assembled";
if(component=="body" || component=="assembled") body();
if(component=="lid" || component=="assembled") lid();
