f=part("form")
rim=param("speaker_corner_radius",0.65)
unit=Box(f.spk_t,f.spk_l,f.spk_w)
unit=fillet(unit.edges().filter_by(Axis.X),rim)
unit=f.spk_pose*unit
unit.color=srgb("#373b42")
publish("speaker_ref",unit,"HDK-151108ZA-5W13, seated body envelope",role="reference")