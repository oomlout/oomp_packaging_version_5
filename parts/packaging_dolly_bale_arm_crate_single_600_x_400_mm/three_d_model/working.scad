style = "bale_arm_crate_single";
seat_depth = 23;
seat_length = 603;
seat_width = 405;
deck = 30;
height = 170;
length = 610;
wheel = 100;
width = 410;
deck_color = "#edaf16";
trim_color = "#e39d12";
wheel_color = "#c8c6b5";
mount_color = "#9bA2A6";

// Dimensional reference in mm. X is length, Y is width and the floor is Z=0.
// The generated working.scad supplies the values above this template.
$fn = 32;
component = "all";
wood = style == "simple";
single_crate = style == "bale_arm_crate_single";
trim_height = wood ? 1.5 : single_crate ? seat_depth : 5;
deck_top = height - trim_height;
deck_base = deck_top - deck;
wheel_width = wheel * 0.30;
wheel_x = length / 2 - wheel * 0.66;
wheel_y = width / 2 - wheel * 0.58;

module rounded(l, w, radius) {
    offset(r=radius) square([l-2*radius, w-2*radius], center=true);
}

module octagon(l, w, c) {
    polygon([[-l/2+c,-w/2],[l/2-c,-w/2],[l/2,-w/2+c],[l/2,w/2-c],
             [l/2-c,w/2],[-l/2+c,w/2],[-l/2,w/2-c],[-l/2,-w/2+c]]);
}

module deck_outline() {
    difference() {
        rounded(length, width, wood ? 18 : 12);
        if (wood)
            translate([-length/2+42,0]) rounded(22,94,10);
        else if (single_crate)
            octagon(length*0.58, width*0.34, width*0.08);
        else
            for (s=[-1,1]) translate([s*length*0.24,0])
                rounded(length*0.14,width*0.23,9);
    }
}

module top_details() {
    if (wood)
        for (x=[-1,1], y=[-1,1])
            translate([x*(length/2-54),y*(width/2-50)]) circle(d=59);
    else if (single_crate)
        difference() {
            rounded(length,width,12);
            rounded(seat_length,seat_width,9);
        }
    else
        for (x=[-0.37,0,0.37], y=[-1,1])
            translate([x*length,y*(width/2-13)]) rounded(55,18,5);
}

module wheel_positions() {
    for (x=[-1,1], y=[-1,1])
        translate([x*wheel_x,y*wheel_y,0]) children();
}

module axle_cylinder(diameter, span) {
    rotate([90,0,0]) cylinder(d=diameter,h=span,center=true);
}

module bracket() {
    plate = wheel * 0.09;
    translate([0,0,deck_base-plate/2])
        cube([wheel*0.61,wheel_width+plate*3,plate], center=true);
    for (s=[-1,1])
        translate([0,s*(wheel_width/2+plate/2),0]) hull() {
            translate([0,0,wheel/2]) axle_cylinder(wheel*0.25,plate);
            translate([0,0,deck_base-plate]) cube([wheel*0.46,plate,plate],center=true);
        }
}

if (component=="all" || component=="deck")
    color(deck_color) translate([0,0,deck_base]) linear_extrude(deck) deck_outline();
if (component=="all" || component=="trim")
    color(trim_color) translate([0,0,deck_top]) linear_extrude(trim_height) top_details();
if (component=="all" || component=="wheels")
    color(wheel_color) wheel_positions() translate([0,0,wheel/2]) axle_cylinder(wheel,wheel_width);
if (component=="all" || component=="mounts")
    color(mount_color) wheel_positions() bracket();
