f=part("form")
# Nominal 30 x 26 mm stainless split ring. Axial thickness through the
# double-wound section is 3 mm; the winding and opening angle are approximate.
turns=param("split_ring_turns",1.9)
radial_wire=param("flat_ring_radial_width",2.0)
layer=param("flat_ring_single_thickness",1.48)
pitch=layer+param("flat_ring_turn_gap",0.04)
height=turns*pitch
path=Helix(pitch,height,(f.ring_od-radial_wire)/2)
plane=Plane(origin=path.position_at(0),x_dir=(1,0,0),z_dir=path.tangent_at(0))
wound=sweep(plane*Ellipse(radial_wire/2,layer/2),path=path,is_frenet=True)
ring=Pos(0,f.ring_cy,f.ring_cz-height/2)*Rot(0,0,90)*wound
ring.color=srgb("#bac4ce")
publish("keyring_ref",ring,"Split key ring",material="stainless_steel",role="reference")