// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 89.0, 117.0, 74.0, 89.0, 118.0, 76.0, 13, 0.85, 5.34, 2.1, 8.7, 12);
 systempak("lid", 89.0, 117.0, 74.0, 89.0, 118.0, 76.0, 13, 0.85, 5.34, 2.1, 8.7, 12);
} else systempak(component, 89.0, 117.0, 74.0, 89.0, 118.0, 76.0, 13, 0.85, 5.34, 2.1, 8.7, 12);
