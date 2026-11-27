// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 140.0, 184.0, 108.0, 140.0, 185.0, 110.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
 systempak("lid", 140.0, 184.0, 108.0, 140.0, 185.0, 110.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
} else systempak(component, 140.0, 184.0, 108.0, 140.0, 185.0, 110.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
