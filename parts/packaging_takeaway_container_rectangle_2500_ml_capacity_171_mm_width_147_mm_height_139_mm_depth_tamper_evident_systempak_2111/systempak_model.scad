// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 147.0, 170.0, 137.0, 147.0, 171.0, 139.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
 systempak("lid", 147.0, 170.0, 137.0, 147.0, 171.0, 139.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
} else systempak(component, 147.0, 170.0, 137.0, 147.0, 171.0, 139.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
