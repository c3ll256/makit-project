import math
from screwjoint import make_screw_joint_v1
from portcut import port_cut, PortSpec

# ---------- Form (approved look) ----------
lobe_count = int(param("lobe_count", 6))
lobe_r = param("lobe_radius", 25.0)
lobe_ring_r = param("lobe_ring_radius", 13.0)
notch_r = param("notch_radius", 16.0)
body_h = param("body_thickness", 22.0)
front_edge_r = param("front_edge_radius", 7.0)
back_edge_r = param("back_edge_radius", 5.0)
wall = param("wall_thickness", 2.0)
seam_z = param("seam_height", 8.0)
reveal = param("seam_reveal", 0.5)

screen_cx, screen_cy = 0.0, param("screen_center_y", 4.3)
bezel_r = param("bezel_radius", 24.2)
bezel_gap = param("bezel_radial_gap",0.2)
btn_side_r = param("side_button_radius", 4.5)
btn_mid_r = param("mid_button_radius", 6.5)
btn_gap = 0.3
btn_pocket_depth = 0.8
btn_stem_hole_r = 2.9
button_half_span = param("button_half_span", 14.5)
button_side_y = param("button_side_y", -23.5)
button_middle_y = param("button_middle_y", -26.5)
button_stem_r = 2.6
button_pusher_r = param("button_pusher_radius", 3.7)
button_pusher_t = param("button_pusher_thickness", 1.2)
button_pusher_clearance = param("button_pusher_clearance", 0.3)
button_working_travel = param("button_working_travel", 0.25)
nub_r = param("nub_radius", 5.5)
nub_hole_r = param("nub_cord_hole_radius", 1.3)

# ---------- Purchased-part facts ----------
# Selected YouXin 1.3in module: planar geometry from seller drawing.
DISP_W = param("display_pcb_width",27.78)
DISP_H = param("display_pcb_height",39.22)
DISP_BOARD = DISP_W
DISP_BOARD_T = param("display_pcb_thickness",1.6)
DISP_LCM_W = param("display_frame_width",26.16)
DISP_LCM_H = param("display_frame_height",29.22)
DISP_LCM_T = param("display_front_thickness",2.0)
DISP_AA_OFFSET_Y = param("display_active_offset_y",1.58)
DISP_J1_H = 8.5
DISP_HEADER_Y = param("display_header_from_top",1.5)
DISP_HOLE_R = param("display_mount_hole_radius",1.0)
DISP_HOLE_INSET = param("display_mount_hole_inset",2.5)
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

# Cap and switch axes coincide at the user-marked lower-inner positions.
buttons = [((-button_half_span,button_side_y),btn_side_r),((0.0,button_middle_y),btn_mid_r),((button_half_span,button_side_y),btn_side_r)]
cap_layout = buttons
# Lanyard ball sits wholly in the front half so the seam never cuts it
nub_c = (0.0, lobe_ring_r + lobe_r + nub_r * 0.25, seam_z + reveal + nub_r + 0.3)

# Z stack, front to back
bezel_inset = 0.6
bezel_t = 2.4
bezel_bottom_z = body_h - bezel_inset - bezel_t
lcm_front_z = bezel_bottom_z
board_front_z = lcm_front_z - DISP_LCM_T
board_back_z = board_front_z - DISP_BOARD_T
support_top_z = board_back_z - 0.1
board_c = (screen_cx, screen_cy - DISP_AA_OFFSET_Y)
j1_box = (6.1, board_c[1] + 10.4, board_c[1] + 19.6)   # half-width, y0, y1 (vendor .brd)

bat_c = (param("battery_center_x", -8.6), param("battery_center_y", 1.0))
bat_floor_z = param("battery_floor_height",2.1)
box_t = 1.2
box_clear = 0.3
box_in_x = BAT_X / 2 + box_clear
box_in_y0, box_in_y1 = bat_c[1] - BAT_Y / 2 - box_clear, bat_c[1] + BAT_Y / 2 + box_clear

sw_plunger_top_z = param("switch_top_z", 19.1)
production_pcb_t = param("production_pcb_thickness", 1.0)
key_pcb_bottom_z = param("key_pcb_bottom_z", 3.740)
key_pcb_top_z = key_pcb_bottom_z + production_pcb_t - 0.055
actuator_contact_z = param("actuator_contact_z", 9.735)
guide_outer_r = param("button_guide_outer_radius", 5.2)
guide_inner_r = param("button_guide_inner_radius", 2.9)
guide_bottom_z = param("button_guide_bottom_z", 10.6)
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
screw_xy = [(27.0, 13.0), (-27.0, 13.0), (24.0, -20.0), (-24.0, -20.0)]

# ---------- Outer form ----------
outline = cloud_outline()
# Two full-height elliptical rolls share their widest section at the seam.
# The lateral radii keep the existing front/back face margins; stretching only
# the outer form in Z removes the former straight side band. All hardware
# is placed later and retains its original coordinates.
upper_roll = extrude(outline, front_edge_r + 1)
upper_roll = fillet(upper_roll.faces().sort_by(Axis.Z)[-1].edges(), front_edge_r)
upper_roll = upper_roll - Pos(0, 0, 1 - 100) * Box(400, 400, 200)
upper_roll = scale(upper_roll, by=(1, 1, (body_h-seam_z)/front_edge_r))
upper_roll = Pos(0, 0, seam_z-upper_roll.bounding_box().min.Z) * upper_roll
lower_roll = extrude(outline, back_edge_r + 1)
lower_roll = fillet(lower_roll.faces().sort_by(Axis.Z)[0].edges(), back_edge_r)
lower_roll = lower_roll - Pos(0, 0, back_edge_r + 100) * Box(400, 400, 200)
lower_roll = scale(lower_roll, by=(1, 1, seam_z/back_edge_r))
lower_roll = Pos(0, 0, -lower_roll.bounding_box().min.Z) * lower_roll
body = upper_roll + lower_roll
assert body.is_valid and len(body.solids()) == 1, "Outer rolls must join as one solid"
inner = offset(body, -wall)
assert inner.is_valid and len(inner.solids()) == 1, "Uniform wall offset failed"

# Right valley: where the USB-C opening goes
x_outer = (outline & (Pos(60, 0) * Rectangle(120, 0.05))).bounding_box().max.X
# Fixed physical carrier pose from the released STEP; changing the cloud outline
# must not move the XIAO or the already approved recessed USB-C face.
XIAO_CARRIER_PCB_END_X = 31.2833399745186
xiao_x1 = XIAO_CARRIER_PCB_END_X
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
    profile = Pos((cx+sx)/2, (cy+sy)/2) * (Circle(pr) if d < 0.001 else SlotOverall(d+2*pr, 2*pr, rotation=a))
    pusher_pockets.append(Pos(0,0,sw_plunger_top_z-button_pusher_clearance-button_working_travel) * extrude(profile, button_pusher_t+2*button_pusher_clearance+button_working_travel))
    # The rear-open install channel clears the pusher without weakening the screw engagement.
    entry_r = button_pusher_r + button_pusher_clearance
    entry_profile = Pos((cx+sx)/2,(cy+sy)/2)*(Circle(entry_r) if d < 0.001 else SlotOverall(d+2*entry_r,2*entry_r,rotation=a))
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

# Rear-open internal entry lets the front half lower over the socketed XIAO.
# The outer recessed face stays intact; retain 1.2 mm in front of this hidden channel.
usb_entry_clearance = param("usb_internal_entry_clearance",0.15)
entry_low = seam_z-0.5
entry_high = usb_z+2.5
entry = port_cut(PortSpec("rounded",10.4,entry_high-entry_low,0.8),at=(usb_socket_front_x+usb_entry_clearance,0,(entry_low+entry_high)/2),facing="+X",depth=4.0,clearance=0)
front_shell=front_shell-entry

# ---------- Front-half internals ----------
ZTOP = body_h + 1
front_feat = []
# Screen edge locators belong to the enlarged bezel, where they join its underside.
# Carrier is positively screwed to the rear half.
def solids_of(shape):
    if isinstance(shape, list): return [s for child in shape for s in solids_of(child)]
    return list(shape.solids())
for (gx, gy), br in buttons:
    front_feat.append(Pos(gx, gy, guide_bottom_z) * (Cylinder(guide_outer_r, ZTOP-guide_bottom_z, align=(Align.CENTER,Align.CENTER,Align.MIN)) - Cylinder(guide_inner_r, ZTOP-guide_bottom_z, align=(Align.CENTER,Align.CENTER,Align.MIN))))
front_clipped=[]
for feature in solids_of(front_feat):
    clip_feature=feature.intersect(inner)
    if clip_feature is not None: front_clipped.extend(solids_of(clip_feature))
ff=Compound(children=front_clipped)
flange_clear=Pos(screen_cx,screen_cy,body_h-wall-1.1)*Cylinder(bezel_r+2.2,1.3,align=(Align.CENTER,Align.CENTER,Align.MIN))
front_parts=[]
for feature in ff.solids():
    cut_feature=feature-flange_clear
    if cut_feature is not None: front_parts.extend(solids_of(cut_feature))
front_shell=front_shell.fuse(*front_parts)
# Clearance shelf for the wider bezel flange beneath the curved front skin.
front_shell=front_shell-flange_clear

# ---------- Back-half internals ----------
back_feat = []
# Raised tray clears the carrier below the battery's lower edge.
tray_top=param("battery_tray_rim_top_7p",8.3)
box_out=Pos(bat_c[0],bat_c[1],wall-0.5)*Box(BAT_X+2*(box_clear+box_t),BAT_Y+2*(box_clear+box_t),tray_top-wall+0.5,align=(Align.CENTER,Align.CENTER,Align.MIN))
box_in=Pos(bat_c[0],bat_c[1],wall)*Box(BAT_X+2*box_clear,BAT_Y+2*box_clear,30,align=(Align.CENTER,Align.CENTER,Align.MIN))
tray=box_out-box_in
# Open right side for battery leads and the cable running above the XIAO.
tray=tray-Pos(bat_c[0]+BAT_X/2+box_clear,0,4.9)*Box(5,40,20,align=(Align.CENTER,Align.CENTER,Align.MIN))
tray=tray-Pos(0,20.5,3.7)*Box(22,5,20,align=(Align.CENTER,Align.CENTER,Align.MIN))
back_feat.append(tray)
# Screen retained by the separate keeper, not tall rear posts.
# Supports under clear edge regions of the XIAO carrier.
for sx,sy in [(30.2,7.5),(30.2,-7.5),(8.0,9.5)]:
    back_feat.append(Pos(sx,sy,wall-0.5) * Cylinder(0.65,key_pcb_bottom_z-0.035-wall+0.5,align=(Align.CENTER,Align.CENTER,Align.MIN)))
# Three supports take button loads through the PCB, clear of switch legs.
for (sxp,syp),br in buttons:
    back_feat.append(Pos(sxp,syp,wall-0.5)*Cylinder(key_support_r,key_pcb_bottom_z-0.035-wall+0.5,align=(Align.CENTER,Align.CENTER,Align.MIN)))
for px, py in key_locators:
    back_feat.append(Pos(px, py, wall - 0.5) * Cylinder(2.0, key_pcb_bottom_z - 0.035 - wall + 0.5, align=(Align.CENTER, Align.CENTER, Align.MIN)))

dupont_zone = Pos((dupont_x0 + dupont_x1) / 2, (dupont_y0 + dupont_y1) / 2, 0) * Box(dupont_x1 - dupont_x0 + 2, dupont_y1 - dupont_y0 + 4, 100)
# Alignment lip: rises above the seam inside the front half
def ring(o_out, o_in, z0, h):
    return Pos(0, 0, z0) * extrude(offset(outline, o_out) - offset(outline, o_in), h)
lip = ring(-(wall - 0.6), -(wall + 1.2), seam_z - 2.0, 2.0) + ring(-(wall + 0.15), -(wall + 1.2), seam_z - 0.01, 1.6)
lip = lip - Pos((xiao_x0 + x_outer) / 2 + 2, 0, 0) * Box(x_outer - xiao_x0 + 8, XIAO_W + 3, 60)

back_feat.append(lip)
back_clipped=[]
for feature in solids_of(back_feat):
    clip_feature=feature.intersect(body)
    if clip_feature is not None: back_clipped.extend(solids_of(clip_feature))
bf=Compound(children=back_clipped)
back_shell=back_shell.fuse(*bf.solids())

# ---------- Seam shadow line ----------
groove = Pos(0, 0, seam_z) * (Box(400, 400, 2 * reveal) - extrude(offset(outline, -reveal), 10, both=True))
front_shell = front_shell - groove
back_shell = back_shell - groove

# A shallow board-shaped seating pocket clears the curved inside of the rear shell.
pcb_relief_clearance=param("pcb_edge_pocket_clearance",0.15)
pcb_ref=Pos(-100,78.5,key_pcb_bottom_z)*max(asset("design/pet-shell/source/assets/1923175e7cab06faa9851cbba0d6325b141ea46cefcecbd8921588a036ad542d.step").solids(),key=lambda s:s.volume)
pcb_face=max([a for a in pcb_ref.faces() if a.geom_type==GeomType.PLANE and abs(a.normal_at().Z)>0.99],key=lambda a:a.area)
seat_face=Pos(0,0,key_pcb_bottom_z-0.04-pcb_face.center().Z)*pcb_face
seat=extrude(offset(seat_face,pcb_relief_clearance),amount=1.8,dir=(0,0,1))
back_shell=back_shell-seat

if isinstance(back_shell,list): back_shell=Compound(children=back_shell)
# Two M2 screws clamp the carrier directly to rear bosses.
carrier_joints=[]
clamps=part("carrier_clamps")
for i,(px,py) in enumerate(key_locators):
    if isinstance(back_shell,list): back_shell=Compound(children=back_shell)
    j=make_screw_joint_v1(size="M2",at=Location((px,py,clamps.z+clamps.t)),through=[(clamps.clamp_parts[i],clamps.t),(pcb_ref,production_pcb_t-0.02)],seat="surface",head="pan",engage_depth=1.4,into=back_shell,material="PETG",lengths=(4,),label=f"carrier:{i}")
    back_shell=back_shell+j.bosses-j.engage_cuts
    carrier_joints.append(j)
# Two padded rear posts keep the screen adapter seated without battery compression.
adapter_bottom_z=board_back_z-2.5-5.7950061-(production_pcb_t-0.8)
adapter_cy=board_c[1]+DISP_H/2-DISP_HEADER_Y+3.5
for xx in (-8.5,8.5):
    back_shell=back_shell+Pos(xx,adapter_cy+2,wall-0.1)*Box(2.6,3,adapter_bottom_z-0.8-wall+0.1,align=(Align.CENTER,Align.CENTER,Align.MIN))

# Normalise boolean multi-solid results before the joint kit.
if isinstance(front_shell,list): front_shell=Compound(children=front_shell)
if isinstance(back_shell,list): back_shell=Compound(children=back_shell)
print("Shells before joints",len(front_shell.solids()),len(back_shell.solids()))
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
if isinstance(front_shell,list): front_shell=Compound(children=front_shell)
front_shell = front_shell.cut(*pusher_pockets)

shell_opacity = param("shell_opacity", 0.5)
shell_color = srgb("#a594f0", shell_opacity)
front_shell.color = shell_color
back_shell.color = shell_color
# Front finish is published by its own part after keeper receiving bosses are solved.
publish("back_shell", back_shell, "Back shell", material="petg")
for i, j in enumerate(screws):
    publish(f"screw_{i}", j.hardware, f"M2 screw {i + 1}", material="steel", role="fastener")
screw_report = [(j.screw_length_mm, j.boss_length_mm, j.notes) for j in screws]

for i,j in enumerate(carrier_joints):
    publish(f"carrier_screw_{i}",j.hardware,f"Carrier M2x4 screw {i+1}",material="steel",role="fastener")
print("Carrier joints",[(j.screw_length_mm,j.boss_length_mm,j.notes) for j in carrier_joints])