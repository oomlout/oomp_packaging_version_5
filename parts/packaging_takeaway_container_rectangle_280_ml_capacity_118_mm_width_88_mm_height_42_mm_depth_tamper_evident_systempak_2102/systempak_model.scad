// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 88.0, 117.0, 40.0, 88.0, 118.0, 42.0, 13, 0.85, 5.279999999999999, 2.1, 8.7, 12);
 systempak("lid", 88.0, 117.0, 40.0, 88.0, 118.0, 42.0, 13, 0.85, 5.279999999999999, 2.1, 8.7, 12);
} else systempak(component, 88.0, 117.0, 40.0, 88.0, 118.0, 42.0, 13, 0.85, 5.279999999999999, 2.1, 8.7, 12);
