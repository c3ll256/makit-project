f=part("form")
wire_r=param("wire_envelope_radius",0.4)
housing_w=param("gh_housing_width",10.0)
housing_d=param("gh_mated_external_length",3.0)
housing_h=param("gh_housing_height",3.0)
carrier_y=-12.5
carrier_z=10.735
screen_y=f.adapter_cy+3.8491679+housing_d/2
screen_z=f.adapter_bottom_z-2.22
carrier_bottom=param("carrier_gh_opening_z",8.795)
carrier_top=carrier_z+housing_h/2
carrier_plug=Pos(17,carrier_y,carrier_bottom)*Box(housing_w,housing_d,carrier_top-carrier_bottom,align=(Align.CENTER,Align.CENTER,Align.MIN))
screen_plug=Pos(0,screen_y,screen_z)*Box(housing_w,housing_d,housing_h)
carrier_plug.color=srgb("#e6e2da")
screen_plug.color=srgb("#e6e2da")
publish("lcd_carrier_plug",carrier_plug,"GH7 locked cable carrier end",role="reference")
publish("lcd_display_plug",screen_plug,"GH7 locked cable display end",role="reference")
riser_outer_x=param("wire_riser_outer_x",17.2)
riser_pitch=param("wire_riser_pitch",0.9)
riser_first_y=param("wire_riser_first_y",26.8)
cross_outer_z=param("wire_cross_outer_z",16.0)
wires=[];wire_lengths=[]
colors=["#29292c","#b43f46","#ede8dc","#e3b944","#bd7650","#54816d","#737caa"]
for i,col in enumerate(colors):
 sx=17-(i-3)*1.25
 ex=(i-3)*1.25
 j=i%3
 g=i//3
 mx=21.5 if i==6 else 23.1-j*0.8
 zz=15.1+(i//3)*0.9
 fan_y=-10.2-g+j*0.85
 fan_z=12.9+g*0.85
 low_z=5.2+i*0.8
 cross_z=cross_outer_z-i*0.85
 approach=33.0
 pts=[(sx,carrier_y,carrier_z+housing_h/2),(sx,carrier_y,fan_z),(sx+0.9,fan_y,fan_z),(mx,fan_y,fan_z),(mx,fan_y,zz),(mx,11+g,zz),(mx,11+g,low_z)]
 lx=riser_outer_x-i*riser_pitch
 lane_y=20.0-0.9*g
 rise_y=riser_first_y+0.9*g
 pts.extend([(mx,lane_y,low_z),(lx,lane_y,low_z),(lx,rise_y,low_z),(lx,rise_y,cross_z),(ex,rise_y,cross_z),(ex,approach,cross_z),(ex,approach,screen_z),(ex,screen_y+housing_d/2,screen_z)])
 pts=[p for j,p in enumerate(pts) if j==0 or (Vector(p)-Vector(pts[j-1])).length>0.001]
 route=Polyline(*pts)
 w=sweep(Plane(origin=pts[0],z_dir=Vector(pts[1])-Vector(pts[0]))*Circle(wire_r),path=route,transition=Transition.ROUND)
 assert w.is_valid, f"Invalid wire envelope {i}"
 w.color=srgb(col);wires.append(w);wire_lengths.append(route.length)
publish("lcd_cable_route",wires,"Locked 7-wire cable route",role="reference")
print("Wire route lengths",wire_lengths)