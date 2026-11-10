import math
from screwjoint import make_screw_joint_v1
from portcut import port_cut, PortSpec

# ---------- Form (approved look) ----------
lobe_count = int(param("lobe_count", 6))
lobe_r = param("lobe_radius", 18.0)
lobe_ring_r = param("lobe_ring_radius", 22.0)
notch_r = param("notch_radius", 6.0)
body_h = param("body_thickness", 22.0)
front_edge_r = param("front_edge_radius", 7.0)
back_edge_r = param("back_edge_radius", 5.0)
wall = param("wall_thickness", 2.0)
seam_z = param("seam_height", 8.0)
reveal = param("seam_reveal", 0.5)

screen_cx, screen_cy = 0.0, param("screen_center_y", 3.0)
bezel_r = param("bezel_radius", 21.0)
bezel_gap = 0.35
btn_side_r = param("side_button_radius", 4.5)
btn_mid_r = param("mid_button_radius", 5.5)
btn_ring_r = param("button_ring_radius", 27.5)
btn_gap = 0.3
btn_pocket_depth = 0.8
btn_stem_hole_r = 2.9
button_inset = param("button_inward_shift", 3.0)
button_side_drop = param("button_side_drop", 2.0)
button_mid_raise = param("button_middle_raise", 1.0)
button_stem_r = 2.6
button_pusher_r = param("button_pusher_radius", 2.9)
button_pusher_t = param("button_pusher_thickness", 1.2)
button_pusher_clearance = param("button_pusher_clearance", 0.3)
button_working_travel = param("button_working_travel", 0.25)
nub_r = param("nub_radius", 5.5)
nub_hole_r = param("nub_cord_hole_radius", 1.3)

# ---------- Purchased-part facts ----------
# Grove 1.2in IPS: 40x40 board with edge notches (vendor Eagle .brd); active area sits
# ~2 mm above board centre (vendor front photo). Board/LCM thickness assumed (no vendor drawing).
DISP_BOARD = 40.0
DISP_BOARD_T = 1.6
DISP_LCM_W, DISP_LCM_H, DISP_LCM_T = 25.76, 28.96, 2.0
DISP_AA_OFFSET_Y = 2.0
DISP_J1_H = 6.0                 # Grove right-angle socket on the back, assumed height
# XIAO ESP32-S3: 21 x 17.8 (Seeed wiki); PCB thickness, USB-C overhang and height assumed
XIAO_L, XIAO_W, XIAO_PCB_T = 21.0, 17.8, 1.2
XIAO_USB_OVERHANG, XIAO_USB_H = 1.0, 3.2
XIAO_PIN_PITCH = 2.54           # 7 pins per side, centred on the board
# Right-angle 2.54 header on the XIAO underside (GND, 3V3, D10, D9) + Grove-to-Dupont female housings
HDR_BODY_H, HDR_BODY_W = 2.5, 2.5
DUPONT_LEN, DUPONT_SQ = 14.0, 2.6
# 6x6x5 THT tact switch: 3.5 body + 1.5 plunger (standard part)
SW_BODY, SW_BODY_H, SW_PLUNGER_H, SW_PLUNGER_D = 6.0, 3.5, 1.5, 3.5
# 503035 LiPo, laid with its 30 mm side across
BAT_X, BAT_Y, BAT_T = 30.0, 35.0, 5.0

# ---------- Layout ----------
def lobe_angle(i):
    return math.radians(90 + 360 * i / lobe_count)

def lobe_center(i, r=None):
    a = lobe_angle(i)
    r = lobe_ring_r if r is None else r
    return (r * math.cos(a), r * math.sin(a))

def cloud_outline():
    f = Circle(lobe_ring_r)
    for i in range(lobe_count):
        f += Pos(*lobe_center(i)) * Circle(lobe_r)
    f = offset(f, notch_r)
    f = offset(f, -notch_r)
    return f

bottom = lobe_count // 2
buttons = [
    (lobe_center(bottom - 1, btn_ring_r), btn_side_r),
    (lobe_center(bottom, btn_ring_r), btn_mid_r),
    (lobe_center(bottom + 1, btn_ring_r), btn_side_r),
]
# Visible caps converge while the released PCB switch locations stay fixed.
cap_layout = []
for (sx, sy), br in buttons:
    if abs(sx) < 0.001:
        cap_layout.append(((sx, sy + button_mid_raise), br))
    else:
        cap_layout.append(((sx - math.copysign(button_inset, sx), sy - button_side_drop), br))
# Lanyard ball sits wholly in the front half so the seam never cuts it
nub_c = (0.0, lobe_ring_r + lobe_r + nub_r * 0.25, seam_z + reveal + nub_r + 0.3)

# Z stack, front to back
bezel_inset = 0.6
bezel_t = 2.4
bezel_bottom_z = body_h - bezel_inset - bezel_t
lcm_front_z = bezel_bottom_z - 0.1
board_front_z = lcm_front_z - DISP_LCM_T
board_back_z = board_front_z - DISP_BOARD_T
support_top_z = board_back_z - 0.1
board_c = (screen_cx, screen_cy - DISP_AA_OFFSET_Y)
j1_box = (6.1, board_c[1] + 10.4, board_c[1] + 19.6)   # half-width, y0, y1 (vendor .brd)

bat_c = (0.0, -0.5)
bat_floor_z = wall + 0.1
box_t = 1.2
box_clear = 0.3
box_in_x = BAT_X / 2 + box_clear
box_in_y0, box_in_y1 = bat_c[1] - BAT_Y / 2 - box_clear, bat_c[1] + BAT_Y / 2 + box_clear

sw_plunger_top_z = param("switch_top_z", 19.1)
key_pcb_bottom_z = param("key_pcb_bottom_z", 12.505)
key_pcb_top_z = key_pcb_bottom_z + 1.545
key_locator_r = param("key_locator_radius", 0.9)
key_support_r = param("key_support_radius", 1.5)
key_upper_gap = param("key_upper_retention_gap", 0.2)
key_locators = [(0.0, -32.5), (-9.0, -30.5)]
sw_base_z = sw_plunger_top_z - SW_PLUNGER_H - SW_BODY_H

# USB-C sits just behind the wall; the plug reaches it through a recessed opening that stays
# clear of the seam (at least 0.8 mm of front-half rim under it)
USB_PLUG_POCKET_H = 7.6          # port kit plug pocket height incl. clearance
usb_z = seam_z + reveal + 0.8 + USB_PLUG_POCKET_H / 2
xiao_bottom_z = usb_z - XIAO_USB_H / 2 - XIAO_PCB_T
usb_recess = wall + 0.1

# Screws on the upper-side lobes and between the bottom buttons, on the flat of the back face,
# clear of the bezel, display and tray
screw_xy = [(27.0, 13.0), (-27.0, 13.0), (22.5, -21.7), (-22.5, -21.7)]

# ---------- Outer form ----------
outline = cloud_outline()
body = extrude(outline, body_h)
body = fillet(body.faces().sort_by(Axis.Z)[-1].edges(), front_edge_r)
body = fillet(body.faces().sort_by(Axis.Z)[0].edges(), back_edge_r)
inner = offset(body, -wall)

# Right valley: where the USB-C opening goes
x_outer = (outline & (Pos(60, 0) * Rectangle(120, 0.05))).bounding_box().max.X
xiao_x1 = x_outer - usb_recess - XIAO_USB_OVERHANG    # PCB end under the receptacle
xiao_x0 = xiao_x1 - XIAO_L
xiao_xc = (xiao_x0 + xiao_x1) / 2
# Pin k = 0..6 along the 5V row (k = 6 is 5V, next to USB); that row faces -Y with USB toward +X
def xiao_pin_x(k):
    return xiao_xc + (k - 3) * XIAO_PIN_PITCH
dupont_pins = [2, 3, 4, 5]                          # D9, D10, 3V3, GND
dupont_x0 = xiao_pin_x(dupont_pins[0]) - DUPONT_SQ / 2
dupont_x1 = xiao_pin_x(dupont_pins[-1]) + DUPONT_SQ / 2
dupont_z0 = xiao_bottom_z - HDR_BODY_H
dupont_y1 = -XIAO_W / 2 - 0.5
dupont_y0 = dupont_y1 - DUPONT_LEN

shell = body - inner
shell = shell - Pos(screen_cx, screen_cy, body_h) * Cylinder(bezel_r + bezel_gap, 8)
for (bx, by), br in cap_layout:
    shell = shell - Pos(bx, by, body_h - btn_pocket_depth) * Cylinder(br + btn_gap, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
    shell = shell - Pos(bx, by, body_h - wall - 1) * Cylinder(btn_stem_hole_r, wall + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))

# Hidden clearance pockets for the eccentric pusher/flanges; leave the outside skin intact.
pusher_pockets = []
for ((cx, cy), br), ((sx, sy), _) in zip(cap_layout, buttons):
    d = math.hypot(sx-cx, sy-cy)
    a = math.degrees(math.atan2(sy-cy, sx-cx))
    pr = button_pusher_r + button_pusher_clearance
    profile = Pos((cx+sx)/2, (cy+sy)/2) * SlotOverall(d+2*pr, 2*pr, rotation=a)
    pusher_pockets.append(Pos(0,0,sw_plunger_top_z-button_pusher_clearance-button_working_travel) * extrude(profile, button_pusher_t+2*button_pusher_clearance+button_working_travel))
    # The rear-open install channel clears the pusher without weakening the screw engagement.
    entry_r = button_pusher_r + 0.1
    entry_profile = Pos((cx+sx)/2,(cy+sy)/2)*SlotOverall(d+2*entry_r,2*entry_r,rotation=a)
    pusher_pockets.append(extrude(entry_profile,sw_plunger_top_z+button_pusher_t))

# Sphere turned so its surface seam faces into the body, away from the cord hole
nub = Pos(*nub_c) * Rot(0, 0, -90) * Sphere(nub_r)
nub = nub - inner
nub = nub - Pos(nub_c[0], nub_c[1] + nub_r * 0.2, nub_c[2]) * Rot(0, 90, 0) * Cylinder(nub_hole_r, 20)
shell = shell + nub

# A round-ended moulded-plug pocket replaces the kit's rectangular recess.
# Start outside the whole curved valley so the capsule stays continuous across its width.
usb_clearance = param("usb_opening_clearance", 0.3)
usb_pocket_w = param("usb_pocket_width", 13.0)
usb_pocket_h = param("usb_pocket_height", 7.0)
usb_cut_face_x = x_outer + 3.0
usb_throat = port_cut("usb_c", at=(usb_cut_face_x, 0, usb_z), facing="+X", depth=wall + 6, clearance=usb_clearance)
usb_pocket_radius = param("usb_pocket_corner_radius", 1.5)
usb_land_ring = param("usb_surround_width", 1.2)
usb_face_gap = param("usb_face_to_socket", 0.35)
# Conceal the PCB behind a same-colour recessed face, just ahead of the metal socket.
usb_socket_front_x = xiao_x1 + XIAO_USB_OVERHANG
usb_land_back_x = xiao_x1 + 0.15
usb_land_face_x = usb_socket_front_x + usb_face_gap
usb_land = port_cut(PortSpec("rounded", usb_pocket_w + 2 * usb_land_ring, usb_pocket_h + 2 * usb_land_ring, usb_pocket_radius + usb_land_ring), at=(usb_cut_face_x, 0, usb_z), facing="+X", depth=usb_cut_face_x-usb_land_back_x, clearance=usb_clearance)
usb_pocket = port_cut(PortSpec("rounded", usb_pocket_w, usb_pocket_h, usb_pocket_radius), at=(usb_cut_face_x, 0, usb_z), facing="+X", depth=usb_cut_face_x-usb_land_face_x, clearance=usb_clearance)
usb_cut = usb_throat + usb_pocket
shell = (shell + (usb_land & body)) - usb_cut

front_shell = shell - Pos(0, 0, seam_z - 100) * Box(400, 400, 200)
back_shell = shell - Pos(0, 0, seam_z + 100) * Box(400, 400, 200)

# ---------- Front-half internals ----------
ZTOP = body_h + 1
front_feat = []
# Display locating ribs at the board corners (top corners: L, bottom corners: bar under the edge)
bx0, bx1 = -DISP_BOARD / 2, DISP_BOARD / 2
by0, by1 = board_c[1] - DISP_BOARD / 2, board_c[1] + DISP_BOARD / 2
rib_z0 = board_back_z - 1.0
rib_g, rib_t = 0.2, 1.2
for sx in (-1, 1):
    # side bar at top corner
    x_in = sx * (DISP_BOARD / 2 + rib_g)
    x_out = sx * (DISP_BOARD / 2 + rib_g + rib_t)
    front_feat.append(Pos((x_in + x_out) / 2, by1 - 1.5 + rib_g / 2 + 0.7, rib_z0) * Box(rib_t, 3.0 + rib_g + rib_t, ZTOP - rib_z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # top edge bar
    front_feat.append(Pos(sx * (DISP_BOARD / 2 - 3.0 + (3.0 + rib_g + rib_t) / 2), by1 + rib_g + rib_t / 2, rib_z0) * Box(3.0 + rib_g + rib_t, rib_t, ZTOP - rib_z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    # bottom edge bar
    front_feat.append(Pos(sx * (DISP_BOARD / 2 - 3.0 + (3.0 + rib_g + rib_t) / 2), by0 - rib_g - rib_t / 2, rib_z0) * Box(3.0 + rib_g + rib_t, rib_t, ZTOP - rib_z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
# The PCB is located by the rear pins and trapped with a 0.2 mm axial gap.
for px, py in key_locators:
    front_feat.append(Pos(px, py - (0.3 if px == 0 else 0), key_pcb_top_z + key_upper_gap) * Cylinder(1.8, ZTOP - key_pcb_top_z - key_upper_gap, align=(Align.CENTER, Align.CENTER, Align.MIN)))
def solids_of(shape):
    if isinstance(shape, list): return [s for child in shape for s in solids_of(child)]
    return list(shape.solids())
ff = Compound(children=solids_of(front_feat)).intersect(inner)
if isinstance(ff, list): ff = Compound(children=ff)
front_shell = front_shell.fuse(*ff.solids())

# ---------- Back-half internals ----------
back_feat = []
# Battery tray; its rim also holds the display board against the bezel
box_out = Pos(bat_c[0], (box_in_y0 + box_in_y1) / 2, wall - 0.5) * Box(2 * (box_in_x + box_t), box_in_y1 - box_in_y0 + 2 * box_t, support_top_z - wall + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN))
box_in = Pos(bat_c[0], (box_in_y0 + box_in_y1) / 2, wall) * Box(2 * box_in_x, box_in_y1 - box_in_y0, 40, align=(Align.CENTER, Align.CENTER, Align.MIN))
tray = box_out - box_in
# notch for the Grove socket, window for the XIAO, slot for the battery leads
tray = tray - Pos(0, box_in_y1, 7.8) * Box(2 * (j1_box[0] + 1.0), 10, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))
tray = tray - Pos(box_in_x + box_t / 2, 0, xiao_bottom_z) * Box(box_t + 2, XIAO_W + 1.4, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))
tray = tray - Pos(box_in_x + box_t / 2, 0, wall) * Box(box_t + 2, 6, 4, align=(Align.CENTER, Align.CENTER, Align.MIN))
# Lower the tray within the PCB envelope; retain the upper display supports.
tray = tray - Pos(0, -20, 9.5) * Box(80, 64, 30, align=(Align.CENTER, Align.CENTER, Align.MIN))
tray = tray - Pos(10.0, -18.8, 7.2) * Box(12.0, 4.0, 20, align=(Align.CENTER, Align.CENTER, Align.MIN))
back_feat.append(tray)
for py in (-6.0, 6.0):
    back_feat.append(Pos(box_in_x + box_t/2, py, wall - 0.5) * Box(box_t, 2.0, xiao_bottom_z-wall+0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
# Extra display supports near the top edge
for sx in (-15.0, 15.0):
    back_feat.append(Pos(sx, board_c[1] + 19.5, wall - 0.5) * Cylinder(1.6, support_top_z - wall + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
back_feat.append(Pos(-19.0, -4.0, wall - 0.5) * Cylinder(1.6, support_top_z-wall+0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
# XIAO ledge near its USB end (the tray wall carries the other end)
back_feat.append(Pos(xiao_x1 - 1.5, 0, wall - 0.5) * Box(3.0, 12.0, xiao_bottom_z - wall + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
# Three supports take button loads through the PCB, clear of switch legs.
for (sxp, syp), br in buttons:
    if sxp < 10:
        back_feat.append(Pos(sxp, syp, wall - 0.5) * Cylinder(key_support_r, key_pcb_bottom_z - 0.035 - wall + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    else:
        back_feat.append(Pos(28.6, syp, wall - 0.5) * Box(3.0, 2.4, key_pcb_bottom_z - 0.035 - wall + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
for px, py in key_locators:
    back_feat.append(Pos(px, py, wall - 0.5) * Cylinder(2.0, key_pcb_bottom_z - 0.035 - wall + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    back_feat.append(Pos(px, py, key_pcb_bottom_z - 0.1) * Cylinder(key_locator_r, 1.4, align=(Align.CENTER, Align.CENTER, Align.MIN)))
dupont_zone = Pos((dupont_x0 + dupont_x1) / 2, (dupont_y0 + dupont_y1) / 2, 0) * Box(dupont_x1 - dupont_x0 + 2, dupont_y1 - dupont_y0 + 4, 100)
# Alignment lip: rises above the seam inside the front half
def ring(o_out, o_in, z0, h):
    return Pos(0, 0, z0) * extrude(offset(outline, o_out) - offset(outline, o_in), h)
lip = ring(-(wall - 0.6), -(wall + 1.2), seam_z - 2.0, 2.0) + ring(-(wall + 0.15), -(wall + 1.2), seam_z - 0.01, 1.6)
lip = lip - Pos((xiao_x0 + x_outer) / 2 + 2, 0, 0) * Box(x_outer - xiao_x0 + 8, XIAO_W + 3, 60)
lip = lip - dupont_zone
back_feat.append(lip)
bf = Compound(children=solids_of(back_feat)).intersect(body)
if isinstance(bf, list): bf = Compound(children=bf)
back_shell = back_shell.fuse(*bf.solids())

# ---------- Seam shadow line ----------
groove = Pos(0, 0, seam_z) * (Box(400, 400, 2 * reveal) - extrude(offset(outline, -reveal), 10, both=True))
front_shell = front_shell - groove
back_shell = back_shell - groove

# ---------- Closing screws: M2 countersunk from the back into front-half standoffs ----------
screws = []
for i, (sx, sy) in enumerate(screw_xy):
    j = make_screw_joint_v1(
        size="M2", at=Location((sx, sy, 0), (180, 0, 0)), through=[(back_shell, wall)],
        seat="countersink", engage_depth=4.0, into=front_shell, material="PETG",
        finish="black", label=f"shell:screw-{i}",
    )
    back_shell = back_shell - j.through_cuts[0]
    front_shell = front_shell + j.bosses - j.engage_cuts
    screws.append(j)

# Clip the boss feet to the curved inner back surface; the screw-axis engagement is unchanged.
front_shell = front_shell - back_shell
front_shell = front_shell.cut(*pusher_pockets)

shell_color = srgb("#a594f0")
front_shell.color = shell_color
back_shell.color = shell_color
publish("front_shell", front_shell, "Front shell", material="petg")
publish("back_shell", back_shell, "Back shell", material="petg")
for i, j in enumerate(screws):
    publish(f"screw_{i}", j.hardware, f"M2 screw {i + 1}", material="steel", role="fastener")
screw_report = [(j.screw_length_mm, j.boss_length_mm, j.notes) for j in screws]
