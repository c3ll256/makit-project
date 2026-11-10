import math
f = part("form")
dome_h = param("button_dome_height", 2.2)
travel_gap = 0.4
peg_r = param("button_coupling_peg_radius", 2.4)
caps=[]
for ((cx,cy),br),((sx,sy),_) in zip(f.cap_layout,f.buttons):
    dome_z=f.body_h-f.btn_pocket_depth+travel_gap
    dome=Pos(cx,cy,dome_z)*Cylinder(br,dome_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
    dome=fillet(dome.edges().group_by(Axis.Z)[-1],min(dome_h*0.9,br*0.6))
    peg=Pos(cx,cy,f.sw_plunger_top_z+0.1)*Cylinder(peg_r,f.button_pusher_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
    main_stem=Pos(cx,cy,f.sw_plunger_top_z+f.button_pusher_t)*Cylinder(f.button_stem_r,dome_z-f.sw_plunger_top_z-f.button_pusher_t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    caps.append(dome.fuse(main_stem,peg))
for cap,n,l in zip(caps,["button_left","button_mid","button_right"],["Left button","Middle button","Right button"]):
    cap.color=srgb("#c9bfff")
    publish(n,cap,l,material="petg")
