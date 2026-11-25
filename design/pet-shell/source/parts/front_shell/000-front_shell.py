f=part("form")
k=part("screen_keeper")
key_gap=param("bezel_key_clearance",0.2)
key_x=f.bezel_r+2.1
key_slot=Pos(key_x,f.face_y,f.body_h-f.wall-1.1)*Box(3+2*key_gap,4+2*key_gap,1.3,align=(Align.CENTER,Align.CENTER,Align.MIN))
front=k.front_result-key_slot
# The top PCB stop is attached directly to the fixed roof.
pcb_y1=f.board_c[1]+f.DISP_H/2
stop=Pos(0,pcb_y1+0.8,f.board_back_z-0.6)*Box(4,1.2,f.body_h-f.wall+0.2-f.board_back_z+0.6,align=(Align.CENTER,Align.CENTER,Align.MIN))
front=front+stop
front.color=f.shell_color
publish("front_shell",front,"Front shell with hidden screen bosses",material="petg")