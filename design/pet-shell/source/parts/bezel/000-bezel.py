f = part("form")
k = part("screen_keeper")
bezel_t = param("bezel_thickness", 2.4)
bezel_inset = param("bezel_inset", 0.6)
flange_w = param("bezel_flange", 2.0)
win_w = param("screen_window_width", 24.0)
win_h = param("screen_window_height", 24.0)
win_r = param("screen_window_corner", 2.0)

top_z = f.body_h - bezel_inset
disc = Pos(f.screen_cx, f.screen_cy, top_z - bezel_t) * Cylinder(f.bezel_r, bezel_t, align=(Align.CENTER, Align.CENTER, Align.MIN))
disc = fillet(disc.edges().group_by(Axis.Z)[-1], 1.0)
# Flange under the shell wall holds the bezel from inside
flange = Pos(f.screen_cx, f.screen_cy, f.body_h - f.wall - 1.0) * Cylinder(f.bezel_r + flange_w, 1.0, align=(Align.CENTER, Align.CENTER, Align.MIN))
key=Pos(f.bezel_r+2.1,f.screen_cy,f.body_h-f.wall-1.0)*Box(3,4,1.0,align=(Align.CENTER,Align.CENTER,Align.MIN))
bezel = disc + flange + key
for x,y in k.screw_xy+f.screw_xy:
 bezel=bezel-Pos(x,y,f.body_h-f.wall-1.2)*Cylinder(5.3 if x==k.side_x else 3.4,1.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
shield_post_z=param("shield_hold_down_bottom",14.785)
bezel=bezel+Pos(18.5,0,shield_post_z)*Box(5,6,top_z-bezel_t-shield_post_z+0.3,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Four PCB-edge locators and the lower ledges grow from the insert itself.
# They meet the opaque disc/flange directly rather than hanging inside its opening.
rail_t=param("bezel_screen_locator_thickness",1.2)
rail_gap=param("bezel_screen_locator_gap",0.2)
rail_z0=f.board_back_z-0.6
rail_top=f.body_h-f.wall-0.7
pcb_y0=f.board_c[1]-f.DISP_H/2
pcb_y1=f.board_c[1]+f.DISP_H/2
for side in (-1,1):
    for yy in (pcb_y0+1.8,pcb_y1-1.8):
        bezel=bezel+Pos(side*(f.DISP_W/2+rail_gap+rail_t/2),yy,rail_z0)*Box(rail_t,3,rail_top-rail_z0,align=(Align.CENTER,Align.CENTER,Align.MIN))
    bezel=bezel+Pos(side*(f.DISP_W/2-1.8),pcb_y0-rail_gap-rail_t/2,rail_z0)*Box(4,rail_t,rail_top-rail_z0,align=(Align.CENTER,Align.CENTER,Align.MIN))
window = Pos(f.screen_cx, f.screen_cy, top_z) * extrude(RectangleRounded(win_w, win_h, win_r), 20, both=True)
bezel = bezel - window
bezel.color = srgb("#2a2830")
publish("bezel", bezel, "Screen bezel", material="petg")