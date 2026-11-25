import math
from screwjoint import make_screw_joint_v1
f=part("form")
t=param("keeper_thickness",2.0)
pad_gap=param("keeper_compressed_pad_gap",0.8)
z=f.board_back_z-pad_gap-t
top_x=param("star_keeper_upper_x",20.8)
top_y=param("star_keeper_upper_y",17.9)
side_x=param("keeper_side_screw_x",-28.0)
side_y=param("cluster_keeper_side_y",3.7)
lower_x=param("single_board_keeper_lower_x",22.0)
lower_y=param("single_board_keeper_lower_y",-14.5)
screw_xy=[(-top_x,top_y),(top_x,top_y),(side_x,side_y),(lower_x,lower_y)]
def plate(x,y,w,h):return Pos(x,y,z)*Box(w,h,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
pad_x=f.DISP_W/2-f.DISP_HOLE_INSET
pad_y0=f.board_c[1]-f.DISP_H/2+f.DISP_HOLE_INSET
pad_y1=f.board_c[1]+f.DISP_H/2-f.DISP_HOLE_INSET
rail_x=-17.4
bottom_y=pad_y0-4.6
raw=plate(rail_x,(bottom_y+pad_y1)/2,4,pad_y1-bottom_y+4)
raw=raw+plate(0,pad_y1,2*pad_x+4.4,4)+plate((rail_x+lower_x)/2,bottom_y,lower_x-rail_x+4,3.6)
raw=raw+plate((side_x+rail_x)/2,side_y,rail_x-side_x+3,4)
for x in (-pad_x,pad_x):
    raw=raw+plate(x,(pad_y0+bottom_y)/2,4.4,pad_y0-bottom_y+3.2)
for sign in (-1,1):
    p=(sign*pad_x,pad_y1)
    q=(sign*top_x,top_y)
    link=Edge.make_line(p,q)
    web=Pos((p[0]+q[0])/2,(p[1]+q[1])/2)*SlotOverall(link.length+4.2,4.2,rotation=math.degrees(math.atan2(q[1]-p[1],q[0]-p[0])))
    raw=raw+Pos(0,0,z)*extrude(web,t)
raw=raw+plate(lower_x,(lower_y+bottom_y)/2,4,lower_y-bottom_y+3)
for x,y in screw_xy:
 raw=raw+Pos(x,y,z)*Cylinder(3.5,t,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Header/socket remains accessible in the top-centre notch.
wire_relief=param("wire_corner_relief_radius",0.6)
raw=raw-Pos(13.25,-12.5,z-0.1)*Cylinder(wire_relief,t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
raw=raw-Pos(24,-20,z-0.1)*Cylinder(3.5,t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
raw=raw-Pos(0,pad_y0-1.0,z-0.1)*Box(21.6,3.4,t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
for (x,y), radius in f.buttons:
    raw=raw-Pos(x,y,z-0.1)*Cylinder(f.guide_outer_r+0.2,t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
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
 # Only generated root solids need clipping. Direct engagement uses the existing wall.
 roots=list(j.bosses.solids())
 for root in roots:
  trimmed=root.intersect(f.body)
  if trimmed:
   front_result=front_result.fuse(*trimmed.solids())
   if isinstance(front_result,list):front_result=Compound(children=front_result)
 front_result=front_result-j.engage_cuts
 receiver_bosses.append(j.bosses)
 joints.append(j)
keeper=keeper-f.speaker_relief
keeper=keeper-f.front_shell
# The PCB carrier sits inside the circular bezel and clears the corner anchors.
pcb_slot=Pos(0,f.board_c[1],f.board_back_z-0.06)*Box(f.DISP_W+0.4,f.DISP_H+0.4,f.DISP_BOARD_T+0.12,align=(Align.CENTER,Align.CENTER,Align.MIN))
glass_slot=Pos(0,f.board_c[1],f.board_front_z-0.01)*Box(f.DISP_LCM_W+0.4,f.DISP_LCM_H+0.4,f.DISP_LCM_T+0.12,align=(Align.CENTER,Align.CENTER,Align.MIN))
front_result=front_result-pcb_slot-glass_slot

keeper.color=srgb("#a594f0")
publish("screen_keeper",keeper,"Screwed screen keeper",material="petg")
for i,j in enumerate(joints):publish(f"keeper_screw_{i}",j.hardware,f"Keeper M2x6 screw {i+1}",material="steel",role="fastener")
print("Keeper joint report",[(j.screw_length_mm,j.boss_length_mm,j.notes) for j in joints])