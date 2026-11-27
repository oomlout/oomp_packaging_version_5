// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 90.0, 119.0, 68.0, 90.0, 120.0, 70.0, 13, 0.85, 5.3999999999999995, 2.1, 8.7, 12);
 systempak("lid", 90.0, 119.0, 68.0, 90.0, 120.0, 70.0, 13, 0.85, 5.3999999999999995, 2.1, 8.7, 12);
} else systempak(component, 90.0, 119.0, 68.0, 90.0, 120.0, 70.0, 13, 0.85, 5.3999999999999995, 2.1, 8.7, 12);
