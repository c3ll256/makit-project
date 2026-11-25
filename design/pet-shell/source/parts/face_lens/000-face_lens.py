f=part("form")
b=part("bezel")
sheet_t=param("face_lens_thickness",0.5)
bond_t=param("face_lens_tape_thickness",0.10)
edge_inset=param("lens_to_bezel_edge",0.50)
radius=f.bezel_r-edge_inset
base=b.top_z+bond_t
lens=Pos(0,f.face_y,base)*Cylinder(radius,sheet_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
lens.color=srgb("#181c23",0.30)
publish("face_lens",lens,"Circular optical lens",material="pc")