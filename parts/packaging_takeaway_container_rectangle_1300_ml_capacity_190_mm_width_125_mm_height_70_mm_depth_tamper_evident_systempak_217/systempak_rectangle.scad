// Millimetres. XY centre at the footprint centre, base at Z=0. X is the short side.
// Each ring is [width, length, radius, z]. Joined profiles keep the shell hollow.
function ring(s,n=16) = [for(q=[0:3],k=[0:n-1])
    let(a=90*q+90*k/(n-1), r=s[2], sx=q==0||q==3?1:-1, sy=q<2?1:-1)
    [sx*(s[0]/2-r)+r*cos(a),sy*(s[1]/2-r)+r*sin(a),s[3]]];
module skin(profile) {
    n=64; last=(len(profile)-1)*n;
    polyhedron(points=[for(s=profile) each ring(s)],
        faces=concat([[for(i=[0:n-1]) i]],
            [for(j=[0:len(profile)-2],i=[0:n-1]) each
              let(a=j*n+i,b=j*n+(i+1)%n) [[a,a+n,b+n],[a,b+n,b]]],
            [[for(i=[n-1:-1:0]) last+i]]),convexity=12);
}
// Profile dimensions independent of nominal capacity; do not scale wall thickness with height.
module systempak(mode,w,l,h,lid_w,lid_l,lid_h,r,wall,shoulder,draft,collar,tab_w) {
    function s(inset,z)=[w-2*inset,l-2*inset,max(1,r-inset*.48),z];
    function t(inset,z)=[lid_w-2*inset,lid_l-2*inset,max(1,r-inset*.48),z];
    lower=shoulder+draft;
    assert(h>collar+3 && lid_h>h && wall>0 && min(w,l)>2*r);
    module tub() {
        union() {
            skin([s(lower+1.5,0),s(lower+.55,.35),s(lower,1.2),
                  s(shoulder,h-collar-.75),s(shoulder-.35,h-collar),
                  s(.65,h-collar),s(.18,h-collar+.55),s(.18,h-collar+2.15),
                  s(.55,h-collar+2.5),s(.60,h-2.25),s(.20,h-1.85),
                  s(0,h-1.45),s(.12,h-.65),s(.55,h),s(1.35,h),
                  s(1.65,h-.85),s(1.65,h-collar+1.2),
                  s(shoulder+wall,h-collar+1.05),s(lower+wall,2),s(lower+wall+1,wall)]);
            // Slim mould ribs on the straight sections of the protective collar.
            for(side=[-1,1]) {
                for(i=[-2:2]) translate([i*(w-2*r)/5,side*(l/2-.54),h-collar*.50])
                    cube([.55,.60,collar*.45],center=true);
                for(i=[-3:3]) translate([side*(w/2-.54),i*(l-2*r)/7,h-collar*.50])
                    cube([.60,.55,collar*.45],center=true);
            }
            // Break-away tongue below the short-end collar and two moulded bridges.
            for(x=[-tab_w*.38,tab_w*.38])
                translate([x,-l/2+1,h-collar-.7]) cube([1.25,1.3,2.8],center=true);
            hull() for(x=[-1,1],z=[0,1])
                translate([x*(tab_w/2-1),-l/2+1.1,h-collar-2.4+z*1.6])
                    rotate([90,0,0]) cylinder(h=.85,r=.7,center=true,$fn=24);
        }
    }
    module lid() {
        // A shallow inset top panel, raised stacking bead and undercut outer skirt.
        skin([t(3.5,lid_h-1.75),t(2.85,lid_h-1.75),t(2.7,h-.8),
              t(2.25,h-.8),t(2.05,h+.12),t(.65,h+.12),t(.2,h+.08),t(0,h+.35),t(.18,lid_h-.55),t(.75,lid_h),
              t(1.45,lid_h),t(2.0,lid_h-.25),t(2.55,lid_h-1.05),
              t(3.4,lid_h-1.2)]);
    }
    if(mode=="body") difference() {
        tub();
        // Shallow underside relief leaves a continuous rounded stacking foot.
        skin([s(lower+3.2,-1),s(lower+3.2,.28),s(lower+3.5,.38)]);
    }
    else if(mode=="lid") lid();
}
