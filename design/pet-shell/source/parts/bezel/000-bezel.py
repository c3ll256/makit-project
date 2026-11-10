f = part("form")
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
bezel = disc + flange
window = Pos(f.screen_cx, f.screen_cy, top_z) * extrude(RectangleRounded(win_w, win_h, win_r), 20, both=True)
bezel = bezel - window
bezel.color = srgb("#2a2830")
publish("bezel", bezel, "Screen bezel", material="pla")
