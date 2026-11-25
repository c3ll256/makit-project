# External envelope and port from LinkMems package drawing, page 7.
width = param("package_width", 3.76)
length = param("package_length", 4.72)
height = param("seated_height", 1.20)
port_d = param("port_diameter", 0.84)
inset = param("port_from_short_edge", 1.32)
# Visual approximations for features without thickness and radius callouts.
base_t = param("substrate_thickness", 0.26)
pad_t = param("terminal_thickness", 0.025)
lid_margin = param("lid_edge_inset", 0.10)
lid_r = param("lid_corner_radius", 0.22)
zbase = (Align.CENTER, Align.CENTER, Align.MIN)
substrate = Pos(0,0,pad_t)*Box(width,length,base_t-pad_t,align=zbase)
substrate.color = srgb("#343a36")
lid = Pos(0,0,base_t)*Box(width-2*lid_margin,length-2*lid_margin,height-base_t,align=zbase)
lid = fillet(lid.edges().filter_by(Axis.Z),lid_r)
lid = fillet(lid.edges().group_by(Axis.Z)[-1],0.09)
lid = lid - Pos(0,length/2-inset,base_t)*Cylinder(port_d/2,height,align=zbase)
lid.color = srgb("#bec4c8")
pads=[]
for x in [-1.17,1.17]:
    for y in [-1.65,0,1.65]:
        terminal = Pos(x,y,0)*Cylinder(0.91/2,pad_t,align=zbase)
        terminal.color = srgb("#bf9b4b")
        pads.append(terminal)
publish("mic1", [substrate,lid]+pads,"MIC1 贴片麦克风",role="reference")