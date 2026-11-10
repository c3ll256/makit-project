import math
f=part("form")
caps=part("buttons")
interference=param("pusher_socket_diametral_interference",0.15)
lead=param("pusher_socket_leadin",0.2)
socket_r=caps.peg_r-interference/2
for ((cx,cy),br),((sx,sy),_),n,cap in zip(f.cap_layout,f.buttons,["pusher_left","pusher_mid","pusher_right"],["button_left","button_mid","button_right"]):
    d=math.hypot(sx-cx,sy-cy)
    a=math.degrees(math.atan2(sy-cy,sx-cx))
    profile=Pos((cx+sx)/2,(cy+sy)/2)*(Circle(f.button_pusher_r) if d < 0.001 else SlotOverall(d+2*f.button_pusher_r,2*f.button_pusher_r,rotation=a))
    pusher=Pos(0,0,f.sw_plunger_top_z)*extrude(profile,f.button_pusher_t)
    pusher=pusher-Pos(cx,cy,f.sw_plunger_top_z-0.1)*Cylinder(socket_r,f.button_pusher_t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
    pusher=pusher-Pos(cx,cy,f.sw_plunger_top_z+f.button_pusher_t-lead)*Cone(socket_r,socket_r+lead,lead,align=(Align.CENTER,Align.CENTER,Align.MIN))
    pusher.color=srgb("#c9bfff")
    publish(n,pusher,n.replace("pusher","Retainer").replace("_"," "),material="petg")
    fit(n,cap,kind="press_fit",budget_mm=0.15,reason="Retaining disc pressed onto cap peg, 0.15 mm diametral interference; the cap peg presses the switch directly.")
