// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 128.0, 191.0, 43.0, 128.0, 192.0, 45.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
 systempak("lid", 128.0, 191.0, 43.0, 128.0, 192.0, 45.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
} else systempak(component, 128.0, 191.0, 43.0, 128.0, 192.0, 45.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
