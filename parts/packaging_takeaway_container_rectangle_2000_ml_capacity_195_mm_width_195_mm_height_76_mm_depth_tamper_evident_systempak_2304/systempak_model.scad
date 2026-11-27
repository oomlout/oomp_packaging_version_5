// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 195.0, 194.0, 74.0, 195.0, 195.0, 76.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
 systempak("lid", 195.0, 194.0, 74.0, 195.0, 195.0, 76.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
} else systempak(component, 195.0, 194.0, 74.0, 195.0, 195.0, 76.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
