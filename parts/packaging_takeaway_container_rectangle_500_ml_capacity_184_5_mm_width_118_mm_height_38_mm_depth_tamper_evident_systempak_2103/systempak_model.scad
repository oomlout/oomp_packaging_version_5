// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 118.0, 183.5, 36.0, 118.0, 184.5, 38.0, 13, 0.85, 5.7, 2.1, 8.36, 12);
 systempak("lid", 118.0, 183.5, 36.0, 118.0, 184.5, 38.0, 13, 0.85, 5.7, 2.1, 8.36, 12);
} else systempak(component, 118.0, 183.5, 36.0, 118.0, 184.5, 38.0, 13, 0.85, 5.7, 2.1, 8.36, 12);
