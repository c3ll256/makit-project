f=part("form")
travel_gap=param("cap_boot_clearance",1.10)
peg_r=param("button_coupling_peg_radius",1.6)
cap_top=param("primary_key_top_z",22.45)
aux_top=param("auxiliary_key_top_z",22.13)
caps=[]
for index,((cx,cy),radius) in enumerate(f.cap_layout):
    top=cap_top if index==0 else aux_top
    bottom=f.body_h-f.btn_pocket_depth+travel_gap
    dome=Pos(cx,cy,bottom)*Cylinder(radius,top-bottom,align=(Align.CENTER,Align.CENTER,Align.MIN))
    dome=fillet(dome.edges().group_by(Axis.Z)[-1],min((top-bottom)*0.7,0.72))
    stem_start=f.collar_z+f.collar_t
    shank=Pos(cx,cy,stem_start)*Cylinder(f.button_stem_r,bottom-stem_start+0.08,align=(Align.CENTER,Align.CENTER,Align.MIN))
    peg=Pos(cx,cy,f.actuator_contact_z)*Cylinder(peg_r,stem_start-f.actuator_contact_z+0.08,align=(Align.CENTER,Align.CENTER,Align.MIN))
    key=dome.fuse(shank,peg)
    caps.append(key)
for index,(name,key) in enumerate(zip(["button_left","button_mid","button_right"],caps)):
    key.color=srgb("#151721") if index==0 else srgb("#a594f0",f.shell_opacity)
    publish(name,key,["Cluster main key","Cluster lower key","Cluster inner key"][index],material="petg")