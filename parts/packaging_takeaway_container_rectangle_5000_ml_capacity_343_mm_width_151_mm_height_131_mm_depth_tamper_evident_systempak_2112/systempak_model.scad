// Millimetres. Profile and features are estimates based on the SKU 209 reference.
use <systempak_rectangle.scad>
component="assembled";
if (component=="assembled") {
 systempak("body", 151.0, 342.0, 129.0, 151.0, 343.0, 131.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
 systempak("lid", 151.0, 342.0, 129.0, 151.0, 343.0, 131.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
} else systempak(component, 151.0, 342.0, 129.0, 151.0, 343.0, 131.0, 13, 0.85, 5.7, 2.1, 8.7, 12);
