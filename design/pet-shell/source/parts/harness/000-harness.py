f=part("form")
wire_r=param("wire_envelope_radius",0.4)
plug_w=param("lcd_plug_width",17.78)
plug_d=param("lcd_plug_depth",2.6)
plug_h=param("lcd_plug_length",14.0)
contact_r=param("lcd_plug_contact_clearance",0.53)
hy=f.board_c[1]+f.DISP_H/2-f.DISP_HEADER_Y
screen_plug_top=f.board_back_z-2.5
screen_plug_bottom=screen_plug_top-plug_h
screen_plug=Pos(0,hy,screen_plug_bottom)*Box(plug_w,plug_d,plug_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
carrier_plug_bottom=7.235
carrier_plug_top=carrier_plug_bottom+plug_h
carrier_plug=Pos(20.2,-13,carrier_plug_bottom)*Box(plug_w,plug_d,plug_h,align=(Align.CENTER,Align.CENTER,Align.MIN))
screen_bores=[];carrier_bores=[]
for i in range(7):
    screen_bores.append(Pos((i-3)*2.54,hy,screen_plug_top-6.6)*Cylinder(contact_r,7,align=(Align.CENTER,Align.CENTER,Align.MIN)))
    carrier_bores.append(Pos(20.2-(i-3)*2.54,-13,carrier_plug_bottom-0.1)*Cylinder(contact_r,7,align=(Align.CENTER,Align.CENTER,Align.MIN)))
screen_plug=screen_plug.cut(*screen_bores)
carrier_plug=carrier_plug.cut(*carrier_bores)
screen_plug.color=srgb("#303237")
carrier_plug.color=srgb("#303237")
publish("lcd_display_plug",screen_plug,"Screen 7P cable plug",role="reference")
publish("lcd_carrier_plug",carrier_plug,"Carrier 7P cable plug",role="reference")
wires=[];wire_lengths=[]
colors=["#29292c","#b43f46","#ede8dc","#e3b944","#bd7650","#54816d","#737caa"]
for i,col in enumerate(colors):
    x=(i-3)*2.54
    d=(i-3)*0.95
    tx=20.2-(i-3)*2.54
    mid=18-(i-3)*0.9
    low=4.8+i*0.9
    high=17+i*0.7
    pts=[(x,hy,screen_plug_bottom-0.05),(x,hy,4.8),(x,hy+1.97,4.8),(x,hy+1.97,low),(x,24.0,low),(mid,24.0,low),(mid,24.0,high),(mid,0,high),(tx,-8,22.3),(tx,-13,22.3),(tx,-13,carrier_plug_top+0.05)]
    pts=[p for j,p in enumerate(pts) if j==0 or (Vector(p)-Vector(pts[j-1])).length>0.001]
    route=Polyline(*pts)
    w=sweep(Plane(origin=pts[0],z_dir=Vector(pts[1])-Vector(pts[0]))*Circle(wire_r),path=route,transition=Transition.ROUND)
    w.color=srgb(col);wires.append(w);wire_lengths.append(route.length)
print("Wire routing lengths mm:",wire_lengths)
publish("lcd_cable_route",wires,"Seven-wire cable routing",role="reference")
