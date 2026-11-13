from screwjoint import make_screw_joint_v1
f=part("form")
t=param("keeper_thickness",2.0)
pad_gap=param("keeper_compressed_pad_gap",0.8)
z=f.board_back_z-pad_gap-t
top_x=param("keeper_top_screw_x",21.5)
top_y=param("keeper_top_screw_y",22.0)
side_x=param("keeper_side_screw_x",-28.0)
side_y=param("keeper_side_screw_y",0.0)
lower_x=param("keeper_lower_screw_x",27.0)
lower_y=param("keeper_lower_screw_y",-13.0)
screw_xy=[(-top_x,top_y),(top_x,top_y),(side_x,side_y),(lower_x,lower_y)]
def plate(x,y,w,h):return Pos(x,y,z)*Box(w,h,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
raw=plate(-15.5,4,4,40)+plate(0,24,2*top_x+2,3)+plate(5.5,-15.5,45,4)+plate((side_x-13.5)/2,side_y,-13.5-side_x+3,4)
for x in (-11.39,11.39):
 raw=raw+plate(x,21,4,8)+plate(x,-14.39,4,4)
for x,y in screw_xy:
 raw=raw+Pos(x,y,z)*Cylinder(3.5,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Header/socket remains accessible in the top-centre notch.
wire_relief=param("wire_corner_relief_radius",0.6)
raw=raw-Pos(13.25,-12.5,z-0.1)*Cylinder(wire_relief,t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
raw=raw-Pos(24,-20,z-0.1)*Cylinder(3.5,t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
raw=raw-Pos(0,20.6,z-0.1)*Box(19.4,4.2,t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
if isinstance(raw,list):raw=Compound(children=raw)
front_result=f.front_shell
keeper=raw
joints=[]
receiver_bosses=[]
for i,(x,y) in enumerate(screw_xy):
 if isinstance(front_result,list):front_result=Compound(children=front_result)
 j=make_screw_joint_v1(size="M2",at=Location((x,y,z),(180,0,0)),through=[(keeper,t)],seat="surface",head="pan",engage_depth=3.6,into=front_result,material="PETG",lengths=(6,),label=f"screen-keeper:{i}")
 keeper=keeper-j.through_cuts[0]
 if isinstance(keeper,list):keeper=Compound(children=keeper)
 # The kit solves the complete joint. Trim only its root outside the
 # intended outer roll, so a shallow skirt cannot print through the skin.
 receiver=j.bosses.intersect(f.body)
 front_result=front_result+receiver-j.engage_cuts
 receiver_bosses.append(j.bosses)
 joints.append(j)
keeper.color=srgb("#a594f0")
publish("screen_keeper",keeper,"Screwed screen keeper",material="petg")
for i,j in enumerate(joints):publish(f"keeper_screw_{i}",j.hardware,f"Keeper M2x6 screw {i+1}",material="steel",role="fastener")
print("Keeper joint report",[(j.screw_length_mm,j.boss_length_mm,j.notes) for j in joints])