// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 86.0, 108.0, 50.0, 86.0, 109.0, 52.0, 12.9, 0.85, 5.16, 2.064, 8.7, 12);
 systempak("lid", 86.0, 108.0, 50.0, 86.0, 109.0, 52.0, 12.9, 0.85, 5.16, 2.064, 8.7, 12);
} else systempak(component, 86.0, 108.0, 50.0, 86.0, 109.0, 52.0, 12.9, 0.85, 5.16, 2.064, 8.7, 12);
