t=param("clamp_thickness",1.0)
r=param("clamp_outer_radius",2.75)
hole_r=param("clamp_hole_radius",1.2)
z=param("carrier_top_height",4.65)
clamp_parts=[]
for i,(x,y) in enumerate([(0,-32.5),(-9,-30.5)]):
    a=Pos(x,y,z)*(Cylinder(r,t,align=(Align.CENTER,Align.CENTER,Align.MIN))-Cylinder(hole_r,t,align=(Align.CENTER,Align.CENTER,Align.MIN)))
    clamp_parts.append(a)
    publish(f"carrier_clamp_{i}",a,f"Carrier clamp {i+1}",material="petg")
