f = part("form")
k = part("screen_keeper")
bezel_t = param("bezel_thickness", 2.4)
bezel_inset = param("bezel_inset", 0.6)
flange_w = param("bezel_flange", 2.0)
win_w = param("tft154_window_width", 28.3)
win_h = param("tft154_window_height", 28.3)
win_r = param("screen_window_corner", 2.0)

top_z = f.body_h - bezel_inset
disc = Pos(f.screen_cx, f.face_y, top_z - bezel_t) * Cylinder(f.bezel_r, bezel_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
disc = fillet(disc.edges().group_by(Axis.Z)[-1], 1.0)
# Flange under the shell wall holds the bezel from inside
flange = Pos(f.screen_cx, f.face_y, f.body_h - f.wall - 1.0) * Cylinder(f.bezel_r + flange_w, 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
key=Pos(f.bezel_r+2.1,f.face_y,f.body_h-f.wall-1.0)*Box(3,4,1.0,align=(Align.CENTER,Align.CENTER,Align.MIN))
bezel = disc + flange + key
for x,y in k.screw_xy+f.screw_xy:
 bezel=bezel-Pos(x,y,f.body_h-f.wall-1.2)*Cylinder(5.3 if x==k.side_x else 3.4,1.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
glass_gap=param("tft_glass_face_clearance",0.25)
pocket=Pos(f.board_c[0],f.board_c[1],f.lcm_front_z-3.0)*Box(f.DISP_LCM_W+0.4,f.DISP_LCM_H+0.4,3.0+glass_gap,align=(Align.CENTER,Align.CENTER,Align.MIN))
bezel=bezel-pocket
# Four bare PCB lands oppose the rear foam. The glass sits clear of the pocket roof.
land_r=param("tft_pcb_land_radius",2.05)
for px in (-k.pad_x,k.pad_x):
    for py in (k.pad_y0,k.pad_y1):
        foot=Circle(land_r)-Circle(f.DISP_HOLE_R+0.12)
        bezel=bezel+Pos(px,py,f.board_front_z)*extrude(foot,f.body_h-f.wall-f.board_front_z-0.14)
# Four PCB-edge locators and the lower ledges grow from the insert itself.
# They meet the opaque disc/flange directly rather than hanging inside its opening.
rail_t=param("bezel_screen_locator_thickness",1.2)
rail_gap=param("bezel_screen_locator_gap",0.2)
rail_z0=f.board_back_z-0.6
rail_top=f.body_h-f.wall-0.7
pcb_y0=f.board_c[1]-f.DISP_H/2
pcb_y1=f.board_c[1]+f.DISP_H/2
for side in (-1,1):
    for yy in (f.screen_cy-9.0,f.screen_cy+9.0):
        bezel=bezel+Pos(side*(f.DISP_W/2+rail_gap+rail_t/2),yy,rail_z0)*Box(rail_t,3,rail_top-rail_z0,align=(Align.CENTER,Align.CENTER,Align.MIN))
    bezel=bezel+Pos(side*5.0,pcb_y0-rail_gap-rail_t/2,rail_z0)*Box(4,rail_t,rail_top-rail_z0,align=(Align.CENTER,Align.CENTER,Align.MIN))
window = Pos(f.screen_cx, f.screen_cy, top_z) * extrude(RectangleRounded(win_w, win_h, win_r), 20, both=True)
if isinstance(bezel,list): bezel=Compound(children=list(bezel))
bezel = bezel - window
if isinstance(bezel,list): bezel=Compound(children=list(bezel))
bezel=bezel-k.front_result
# Allow the shell-mounted stop to enter the bezel flange during assembly.
stop_relief=Pos(0,pcb_y1+0.8,15)*Box(4.5,1.7,5.45,align=(Align.CENTER,Align.CENTER,Align.MIN))
bezel=bezel-stop_relief
bezel.color = srgb("#14171e")
publish("bezel", bezel, "Screen bezel", material="petg")