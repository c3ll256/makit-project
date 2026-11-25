import math
from screwjoint import make_screw_joint_v1
from portcut import port_cut, PortSpec

# The front photograph is 1000 pixels wide. The ten intersections below
# come from extending the straight flanks; the fitted radii restore their tangencies.
photo_scale = param("reference_outline_scale",0.1168)
face_y = param("reference_face_y",1.9)
body_h = param("body_thickness", 22.0)
front_edge_r = param("front_edge_radius", 7.0)
back_edge_r = param("back_edge_radius", 5.0)
wall = param("wall_thickness", 2.0)
seam_z = param("seam_height", 8.0)
reveal = param("seam_reveal", 0.5)

screen_cx, screen_cy = 0.0, param("screen_center_y", 4.3)
bezel_r = param("reference_face_diameter", 52.0)/2
bezel_gap = param("bezel_radial_gap",0.2)
btn_gap = 0.3
btn_pocket_depth = 1.7
btn_stem_hole_r = 2.9
button_stem_r = 2.6
button_pusher_r = param("button_pusher_radius", 3.7)
button_pusher_t = param("button_pusher_thickness", 1.2)
button_pusher_clearance = param("button_pusher_clearance", 0.3)
button_working_travel = param("button_working_travel", 0.25)
ring_od = param("photo_ring_diameter", 30.0)
ring_wire = param("keyring_wire_diameter", 1.6)
ring_clearance = param("keyring_running_clearance", 0.7)
ring_seat_depth = param("photo_ring_embed", 15.7)

# ---------- Purchased-part facts ----------
# Selected YouXin 1.54in 8P module: planar geometry from seller drawing.
DISP_W = param("tft154_board_width",32.0)
DISP_H = param("tft154_board_height",43.72)
DISP_BOARD = DISP_W
DISP_BOARD_T = param("tft154_board_thickness",1.2)
DISP_LCM_W = param("tft154_glass_width",31.52)
DISP_LCM_H = param("tft154_glass_height",33.72)
DISP_LCM_T = param("display_front_thickness",2.0)
DISP_AA_OFFSET_Y = param("tft154_active_offset",1.55)
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
def star_outline():
    # Clockwise in photo coordinates, counterclockwise in the model.
    # Crown, shoulder, wing, waist, foot and lower valley; mirror about x=500.
    corners=[(500,364,86),(310,688,70),(0,688,78),(201,965,69),
             (4,1368,70),(500,1229,60),(996,1368,70),(799,965,69),
             (1000,688,78),(690,688,70)]
    pts=[Vector((x-500)*photo_scale,face_y+(910-y)*photo_scale,0) for x,y,r in corners]
    transitions=[]
    for i,corner in enumerate(pts):
        u=(pts[i-1]-corner).normalized()
        v=(pts[(i+1)%len(pts)]-corner).normalized()
        angle=math.acos(max(-1,min(1,u.dot(v))))
        radius=corners[i][2]*photo_scale
        d=radius/math.tan(angle/2)
        bisector=(u+v).normalized()
        mid=corner+bisector*(radius/math.sin(angle/2)-radius)
        transitions.append((corner+u*d,mid,corner+v*d))
    edges=[]
    for i,(a,m,b) in enumerate(transitions):
        edges.extend([Edge.make_line(transitions[i-1][2],a),Edge.make_three_point_arc(a,m,b)])
    return Face(Wire(edges))

# Cap centres are taken from the three painted locations; the new PCB shares these axes.
primary=(param("cluster_primary_x",-28.25),param("cluster_primary_y",-20.5))
lower=(param("cluster_lower_x",-32.25),param("cluster_lower_y",-33.0))
inner_key=(param("cluster_inner_x",-19.0),param("cluster_inner_y",-28.0))
aux_radius=param("cluster_aux_radius",4.0)
cap_layout=[(primary,param("cluster_primary_radius",6.0)),(lower,aux_radius),(inner_key,aux_radius)]
buttons=cap_layout
collar_z=param("key_collar_bottom",13.0)
collar_t=param("key_collar_thickness",1.3)

# Z stack, front to back
bezel_inset = 0.6
bezel_t = 2.4
bezel_bottom_z = body_h - bezel_inset - bezel_t
lcm_front_z = bezel_bottom_z + param("xiao_screen_recess",0.75)
board_front_z = lcm_front_z - DISP_LCM_T
board_back_z = board_front_z - DISP_BOARD_T
support_top_z = board_back_z - 0.1
board_c = (screen_cx, screen_cy + DISP_AA_OFFSET_Y)
j1_box = (6.1, board_c[1] + 10.4, board_c[1] + 19.6)   # half-width, y0, y1 (vendor .brd)

bat_c = (param("battery_center_x", -8.6), param("xiao_cell_center_y", 8.0))
bat_floor_z = param("xiao_cell_base_z",5.74)
box_t = 1.2
box_clear = 0.3
box_in_x = BAT_X / 2 + box_clear
box_in_y0, box_in_y1 = bat_c[1] - BAT_Y / 2 - box_clear, bat_c[1] + BAT_Y / 2 + box_clear

sw_plunger_top_z = param("switch_top_z", 19.1)
production_pcb_t = param("production_pcb_thickness", 1.0)
key_pcb_bottom_z = param("xiao_carrier_base",3.74)
key_pcb_top_z = key_pcb_bottom_z + production_pcb_t
actuator_contact_z = key_pcb_top_z + SW_BODY_H + SW_PLUNGER_H
guide_outer_r = param("button_guide_outer_radius", 5.2)
guide_inner_r = param("button_guide_inner_radius", 2.9)
guide_bottom_z = param("xiao_key_guide_bottom",10.6)
key_locator_r = param("key_locator_radius", 0.9)
key_support_r = param("key_support_radius", 1.5)
key_upper_gap = param("key_upper_retention_gap", 0.2)
key_locators = [(7.5,-22.0),(-7.5,-22.0)]
sw_base_z = sw_plunger_top_z - SW_PLUNGER_H - SW_BODY_H

# USB-C sits just behind the wall; the plug reaches it through a recessed opening that stays
# clear of the seam (at least 0.8 mm of front-half rim under it)
USB_PLUG_POCKET_H = 7.6          # port kit plug pocket height incl. clearance
usb_z = seam_z + reveal + 0.8 + USB_PLUG_POCKET_H / 2
xiao_bottom_z = usb_z - XIAO_USB_H / 2 - XIAO_PCB_T
usb_recess = wall + 0.1

# Screws on the upper-side lobes and between the bottom buttons, on the flat of the back face,
# clear of the bezel, display and tray
screw_xy = [(27.0, 13.0), (-27.0, 13.0), (24.0, -20.0), (-38.5, -23.2)]

# ---------- Outer form ----------
outline = star_outline()
# Two full-height elliptical rolls share their widest section at the seam.
# The lateral radii keep the existing front/back face margins; stretching only
# the outer form in Z removes the former straight side band. All hardware
# is placed later and retains its original coordinates.
def rolled_body(profile, top_radius, base_radius, z0, z1):
    upper = extrude(profile, top_radius + 1)
    upper = fillet(upper.faces().sort_by(Axis.Z)[-1].edges(), top_radius)
    upper = upper - Pos(0, 0, 1 - 100) * Box(400, 400, 200)
    upper = scale(upper, by=(1, 1, (z1-seam_z)/top_radius))
    upper = Pos(0, 0, seam_z-upper.bounding_box().min.Z) * upper
    lower = extrude(profile, base_radius + 1)
    lower = fillet(lower.faces().sort_by(Axis.Z)[0].edges(), base_radius)
    lower = lower - Pos(0, 0, base_radius + 100) * Box(400, 400, 200)
    lower = scale(lower, by=(1, 1, (seam_z-z0)/base_radius))
    lower = Pos(0, 0, z0-lower.bounding_box().min.Z) * lower
    return upper + lower

body = rolled_body(outline, front_edge_r, back_edge_r, 0, body_h)
inner = rolled_body(offset(outline, -wall), front_edge_r-wall, back_edge_r-wall, wall, body_h-wall)
# The back of each lower point curves forward beyond the main PCB.
# Shift the same underside profile up by one wall for the inner floor.
taper_start=param("foot_taper_start_y",-30.8)
taper_run=param("foot_taper_run",25.0)
taper_lift=param("foot_taper_lift",7.5)
tip=taper_start-taper_run
curve=Edge.make_bezier((taper_start,-0.18),(taper_start-taper_run/2,-0.18),(tip,taper_lift))
perimeter=[curve,Edge.make_line((tip,taper_lift),(tip,-8)),Edge.make_line((tip,-8),(taper_start,-8)),Edge.make_line((taper_start,-8),(taper_start,-0.18))]
taper_tool=extrude(Plane.YZ*Face(Wire(perimeter)),amount=80,both=True)
body=body-taper_tool
inner=inner-Pos(0,0,wall)*taper_tool
assert body.is_valid and inner.is_valid, "Invalid star surface"

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
shell = shell - Pos(screen_cx, face_y, body_h) * Cylinder(bezel_r + bezel_gap, 8)
for (bx, by), br in cap_layout:
    shell = shell - Pos(bx, by, body_h - btn_pocket_depth) * Cylinder(br + btn_gap, 10, align=(Align.CENTER, Align.CENTER, Align.MIN))
    shell = shell - Pos(bx, by, body_h - wall - 1) * Cylinder(btn_stem_hole_r, wall + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))

# Keycaps slide directly onto the tactile switch axes.
# The curved ring tunnel stays in a solid bridge entirely in the front shell.
ring_major = (ring_od-ring_wire)/2
tip_y = outline.bounding_box().max.Y
ring_cy = tip_y - ring_seat_depth + ring_major
ring_cz = seam_z + (body_h-seam_z)*0.46
bridge_y0 = tip_y-ring_seat_depth-ring_wire-ring_clearance-wall
bridge_z0 = seam_z+reveal+0.3
bridge = Pos(0,bridge_y0,bridge_z0)*Box(ring_od+wall*2,ring_od,body_h-bridge_z0,align=(Align.CENTER,Align.MIN,Align.MIN))
bridge = bridge.intersect(body)
ring_channel = Pos(0,ring_cy,ring_cz)*Torus(ring_major,ring_wire+ring_clearance)
shell = (shell + bridge)-ring_channel

# A round-ended moulded-plug pocket replaces the kit's rectangular recess.
# Start outside the whole curved valley so the capsule stays continuous across its width.
usb_clearance = param("usb_opening_clearance", 0.3)
usb_pocket_w = param("usb_pocket_width", 13.0)
usb_pocket_h = param("usb_pocket_height", 7.0)
usb_cut_face_x = outline.bounding_box().max.X + 1.0
usb_throat = port_cut("usb_c", at=(usb_cut_face_x, 0, usb_z), facing="+X", depth=usb_cut_face_x - xiao_x1 + 1, clearance=usb_clearance)
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
guide_base=collar_z+collar_t+0.20
for (gx,gy),br in cap_layout:
    sleeve=extrude(Circle(max(4.2,br+0.65))-Circle(guide_inner_r),body_h-wall+0.08-guide_base)
    front_feat.append(Pos(gx,gy,guide_base)*sleeve)
front_clipped=[]
for feature in solids_of(front_feat):
    clip_feature=feature.intersect(inner)
    if clip_feature is not None: front_clipped.extend(solids_of(clip_feature))
ff=Compound(children=front_clipped)
flange_clear=Pos(screen_cx,face_y,body_h-wall-1.1)*Cylinder(bezel_r+2.2,1.3,align=(Align.CENTER,Align.CENTER,Align.MIN))
front_parts=[]
for feature in ff.solids():
    cut_feature=feature-flange_clear
    if cut_feature is not None: front_parts.extend(solids_of(cut_feature))
front_shell=front_shell.fuse(*front_parts)
# Clearance shelf for the wider bezel flange beneath the curved front skin.
front_shell=front_shell-flange_clear

# ---------- Back-half internals ----------
back_feat = []
# Flush rear ledge supports the portion of the pouch beyond the top PCB edge.
ledge_y0=10.10
ledge_y1=bat_c[1]+BAT_Y/2+0.3
ledge=Pos(bat_c[0],(ledge_y0+ledge_y1)/2,wall-0.35)*Box(BAT_X-2,ledge_y1-ledge_y0,key_pcb_top_z-wall+0.35,align=(Align.CENTER,Align.CENTER,Align.MIN))
back_feat.append(ledge)
for x in (bat_c[0]-BAT_X/2-0.9,bat_c[0]+BAT_X/2+0.9):
 back_feat.append(Pos(x,16,wall-0.35)*Box(1.0,10,bat_floor_z+1.4-wall+0.35,align=(Align.CENTER,Align.CENTER,Align.MIN)))
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
board_outline=[[-21.15,7.75],[-21.15,-12.0723],[-21.1701,-12.0761],[-21.5165,-12.2939],[-23.9351,-14.5397],[-24.0059,-14.5869],[-24.0881,-14.6093],[-32.1131,-15.459],[-32.4712,-15.5603],[-32.7751,-15.7751],[-33.6778,-16.6778],[-33.9163,-17.0347],[-34,-17.4556],[-34,-23.907],[-34.0149,-23.9948],[-34.0581,-24.0726],[-37.759,-28.6987],[-37.938,-29.0218],[-38,-29.3859],[-38,-36.5234],[-37.9093,-36.9607],[-37.6523,-37.3259],[-36.7173,-38.2025],[-36.3695,-38.4229],[-35.965,-38.5],[-30.1735,-38.5],[-29.8349,-38.4466],[-13.0777,-33.0251],[-12.9184,-32.9986],[-10.1552,-32.9526],[-9.9348,-32.9743],[-9.15,-33],[3.5,-33],[4.9811,-32.9593],[6.4577,-32.8375],[7.9254,-32.6349],[9.3798,-32.352],[10.8164,-31.9898],[12.2311,-31.5493],[13.6194,-31.0319],[14.9773,-30.4391],[16.3006,-29.7727],[17.5854,-29.0348],[18.8278,-28.2275],[20.024,-27.3532],[21.1704,-26.4146],[22.2636,-25.4146],[22.4783,-25.1543],[22.6294,-24.8526],[22.7093,-24.5248],[22.7138,-24.1874],[22.6429,-23.8576],[22.5,-23.5519],[22.2924,-23.2859],[22.0306,-23.0731],[21.6059,-22.7552],[21.2319,-22.3791],[20.9163,-21.9527],[20.6658,-21.4851],[20.4857,-20.9861],[20.3799,-20.4664],[20.3505,-19.9367],[20.3983,-19.4084],[20.522,-18.8926],[20.7193,-18.4002],[20.9858,-17.9415],[21.316,-17.5264],[21.7029,-17.1635],[22.1383,-16.8605],[22.613,-16.6238],[23.117,-16.4584],[23.6397,-16.3678],[24.17,-16.354],[24.6967,-16.4171],[25.2086,-16.5559],[25.6951,-16.7675],[26.1457,-17.0473],[26.4393,-17.2137],[26.7625,-17.3103],[27.0992,-17.3322],[27.4323,-17.2782],[27.7449,-17.1512],[28.0212,-16.9576],[28.2472,-16.707],[28.4115,-16.4123],[28.8041,-15.4182],[29.157,-14.4093],[29.4698,-13.3872],[29.7418,-12.3535],[29.9727,-11.3099],[30.1621,-10.2579],[30.3098,-9.1993],[30.4154,-8.1356],[30.4788,-7.0687],[30.5,-6],[30.5,7.75],[30.4499,8.195],[30.3019,8.6178],[30.0637,8.997],[29.747,9.3137],[29.3678,9.5519],[28.945,9.6999],[28.5,9.75],[-19.15,9.75],[-19.595,9.6999],[-20.0178,9.5519],[-20.397,9.3137],[-20.7137,8.997],[-20.9519,8.6178],[-21.0999,8.195]]
board_profile=Polygon(*[(x,y) for x,y in board_outline],align=None)
pcb_ref=Pos(0,0,key_pcb_bottom_z)*extrude(board_profile,amount=production_pcb_t,dir=(0,0,1))
seat_profile=offset(board_profile,pcb_relief_clearance)
seat=Pos(0,0,key_pcb_bottom_z-0.04)*extrude(seat_profile,amount=1.8,dir=(0,0,1))
back_shell=back_shell-seat
for px,py in key_locators:
    front_shell=front_shell-Pos(px,py,key_pcb_top_z-0.01)*Cylinder(3.0,3.7,align=(Align.CENTER,Align.CENTER,Align.MIN))
front_shell=front_shell-Pos(0,0,key_pcb_bottom_z-0.18)*extrude(offset(board_profile,0.3),amount=production_pcb_t+0.36,dir=(0,0,1))

if isinstance(back_shell,list): back_shell=Compound(children=back_shell)
# Two M2 screws clamp the carrier directly to rear bosses.
carrier_joints=[]
clamps=part("carrier_clamps")
for i,(px,py) in enumerate(key_locators):
    if isinstance(back_shell,list): back_shell=Compound(children=back_shell)
    j=make_screw_joint_v1(size="M2",at=Location((px,py,key_pcb_top_z+clamps.t)),through=[(Pos(0,0,key_pcb_top_z-clamps.z)*clamps.clamp_parts[i],clamps.t),(pcb_ref,production_pcb_t-0.02)],seat="surface",head="pan",engage_depth=1.4,into=back_shell,material="PETG",lengths=(4,),label=f"carrier:{i}")
    back_shell=back_shell+(j.bosses-Pos(px,py,key_pcb_bottom_z+4.99)*Box(14,14,10))-j.engage_cuts
    carrier_joints.append(j)
# Kept as references for previous display wiring builds.
adapter_bottom_z=board_back_z-2.5-5.7950061-(production_pcb_t-0.8)
adapter_cy=board_c[1]+DISP_H/2-DISP_HEADER_Y+3.5
# Normalise boolean multi-solid results before the joint kit.
if isinstance(front_shell,list): front_shell=Compound(children=front_shell)
if isinstance(back_shell,list): back_shell=Compound(children=back_shell)
print("Shells before joints",len(front_shell.solids()),len(back_shell.solids()))
# ---------- Closing screws: M2 countersunk from the back into front-half standoffs ----------
screws = []
for i, (sx, sy) in enumerate(screw_xy):
    j = make_screw_joint_v1(
        size="M2", at=Location((sx, sy, 0), (180, 0, 0)), through=[(back_shell, wall + (0.45 if i == 3 else 0))],
        seat="countersink", engage_depth=(3.55 if i == 3 else 4.0), into=front_shell, material="PETG",
        finish="black", label=f"shell:screw-{i}",
    )
    back_shell = back_shell - j.through_cuts[0]
    for root in j.bosses.solids():
        trimmed = root.intersect(body)
        if trimmed:
            front_shell = front_shell.fuse(*trimmed.solids())
            if isinstance(front_shell,list): front_shell=Compound(children=front_shell)
    front_shell = front_shell - j.engage_cuts
    if isinstance(front_shell,list): front_shell=Compound(children=front_shell)
    screws.append(j)

# Clip the boss feet to the curved inner back surface; the screw-axis engagement is unchanged.
front_shell = front_shell - back_shell
if isinstance(front_shell,list): front_shell=Compound(children=front_shell)
# Vertical entry for the fixed carrier past the lower tips of the front bosses.
front_shell=front_shell-extrude(offset(board_profile,0.22),amount=key_pcb_top_z+0.15,dir=(0,0,1))
# Relieve only the inner lip for the pouch corner and placement tolerance.
cell_relief=Pos(bat_c[0],bat_c[1],bat_floor_z-0.15)*Box(BAT_X+0.6,BAT_Y+0.6,BAT_T+0.45,align=(Align.CENTER,Align.CENTER,Align.MIN))
back_shell=back_shell-cell_relief
front_shell=front_shell-cell_relief


# Left speaker lies on its long side. Its factory mesh seals to the seating rim.
spk_x = param("speaker_x", -28.35)
spk_y = param("cluster_speaker_y", -6.8)
spk_z = param("speaker_z", 7.65)
spk_angle = param("speaker_angle", 16.0)
spk_l = param("speaker_length", 15.0)
spk_w = param("speaker_height", 11.0)
spk_t = param("speaker_installed_thickness", 3.4)
spk_pose = Pos(spk_x, spk_y, spk_z) * Rot(0,0,spk_angle)
spk_face = -spk_t/2
def speaker_block(x0,x1,yspan,zspan):
    return spk_pose * Pos((x0+x1)/2,0,0) * Box(x1-x0,yspan,zspan)
spk_space = speaker_block(spk_face, spk_t/2+0.5, spk_l+0.5,spk_w+0.5)
# Outer plenum joins the lower skin. Its upper half stays inside the lid.
lower_half = Pos(0,0,seam_z/2)*Box(100,100,seam_z)
spk_plenum = speaker_block(spk_face-3.3,spk_face,spk_l,spk_w)
speaker_path = outline.bounding_box().max.X - abs(spk_x) + spk_l
lower_root = speaker_block(-speaker_path,spk_face,spk_l,spk_w).intersect(body).intersect(lower_half)
upper_rim = spk_plenum.intersect(inner)
back_shell = (back_shell + (lower_root-seat) + (upper_rim-seat)) - spk_space
spk_air = speaker_block(spk_face-2.4,spk_face+0.1,spk_l-2.6,spk_w-2.6)
back_shell = back_shell-spk_air
slot_h = param("speaker_slot_height",1.6)
for sy in (-4.2,0,4.2):
    # Three round-ended slots share the plenum and sit below the shell seam.
    hole = Plane.YZ * SlotOverall(3.2,slot_h)
    back_shell = back_shell - spk_pose * Pos(-speaker_path,sy,-1.7) * extrude(hole,amount=speaker_path-1)
# Upper shell and screen bracket lower onto the seated transducer.
speaker_relief = speaker_block(spk_face-3.5, spk_t/2+0.55, spk_l+0.6,spk_w+0.6)
front_shell = front_shell - speaker_relief
# Right microphone uses a removable flexible sound guide after board installation.
mic_x = param("xiao_mic_x",25.4)
mic_y = param("mic_port_y", -10.96)
mic_top = param("xiao_mic_top",5.94)
mic_bore = param("mic_channel_diameter", 1.6)
mic_axis_z = mic_top+1.18
mic_wall_blank = back_shell
mic_outer = outline.bounding_box().max.X + wall
mic_tunnel = Pos((mic_x+mic_outer)/2,mic_y,mic_axis_z) * Rot(0,90,0) * Cylinder(mic_bore/2,mic_outer-mic_x)
mic_seat_x = param("mic_guide_end_x",33.35)
mic_seat = Pos((mic_x-2+mic_seat_x)/2,mic_y,mic_top+2.14)*Box(mic_seat_x-mic_x+2,3.8,4.4)
# Continue the TPU outlet through the star flank with a rigid, enclosed duct.
mic_duct = Pos((mic_outer+mic_seat_x-0.2)/2,mic_y,mic_axis_z) * Box(mic_outer-mic_seat_x+0.2, 3.8, 3.8)
mic_duct = mic_duct.intersect(body)
# The roof of the rigid duct belongs to the rear half along with the locating lip.
duct_roof_limit = extrude(offset(outline, -wall-0.3), body_h)
duct_roof = mic_duct.intersect(inner).intersect(duct_roof_limit)
back_shell = back_shell + mic_duct.intersect(lower_half) + duct_roof
back_shell = back_shell-mic_seat-mic_tunnel
front_shell = front_shell-mic_seat-mic_tunnel

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