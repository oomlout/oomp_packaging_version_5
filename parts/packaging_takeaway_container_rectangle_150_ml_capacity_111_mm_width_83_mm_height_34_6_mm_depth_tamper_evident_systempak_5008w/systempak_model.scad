// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 83.0, 110.0, 32.6, 83.0, 111.0, 34.6, 12.45, 0.85, 4.9799999999999995, 1.992, 7.612, 12);
 systempak("lid", 83.0, 110.0, 32.6, 83.0, 111.0, 34.6, 12.45, 0.85, 4.9799999999999995, 1.992, 7.612, 12);
} else systempak(component, 83.0, 110.0, 32.6, 83.0, 111.0, 34.6, 12.45, 0.85, 4.9799999999999995, 1.992, 7.612, 12);
