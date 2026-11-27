// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 125.0, 189.0, 68.0, 125.0, 190.0, 70.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
 systempak("lid", 125.0, 189.0, 68.0, 125.0, 190.0, 70.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
} else systempak(component, 125.0, 189.0, 68.0, 125.0, 190.0, 70.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
