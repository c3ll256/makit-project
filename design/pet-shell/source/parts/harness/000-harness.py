wire_r = param("wire_envelope_radius", 0.4)
wire_pitch = param("wire_bundle_pitch", 0.9)
wires=[]
for i, color in enumerate(["#202020","#b43f46","#f1eee6","#e4bc3e"]):
    dx=(i-1.5)*wire_pitch
    pts=[(10+dx,-9.525,9.92),(7+dx,-7,8.5),(dx,-1,8.5),(dx,23,8.5),(dx,27,9.0),(dx,29.6,11.9)]
    route=Spline(*pts)
    w=sweep(Plane(origin=pts[0],z_dir=Vector(pts[1])-Vector(pts[0]))*Circle(wire_r),path=route)
    w.color=srgb(color)
    wires.append(w)
publish("grove_cable_route",wires,"Grove wire routing envelope (46 mm free route)",role="reference")
