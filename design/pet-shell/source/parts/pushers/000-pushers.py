f=part("form")
caps=part("buttons")
interference=param("pusher_socket_diametral_interference",0.15)
lead=param("pusher_socket_leadin",0.2)
outer_r=param("return_collar_radius",3.8)
socket_r=caps.peg_r-interference/2
for ((x,y),_),n,cap in zip(f.cap_layout,["pusher_left","pusher_mid","pusher_right"],["button_left","button_mid","button_right"]):
    collar=Pos(x,y,f.collar_z)*extrude(Circle(outer_r)-Circle(socket_r),f.collar_t)
    throat=Pos(x,y,f.collar_z+f.collar_t-lead)*Cone(socket_r,socket_r+lead,lead+0.01,align=(Align.CENTER,Align.CENTER,Align.MIN))
    collar=collar-throat
    collar.color=srgb("#8474c0")
    publish(n,collar,"Key retaining collar",material="petg")
    fit(n,cap,kind="press_fit",budget_mm=0.15,reason="Retaining collar grips the direct-acting cap stem with 0.15 mm diametral interference.")