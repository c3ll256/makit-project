f=part("form")
k=part("screen_keeper")
key_gap=param("bezel_key_clearance",0.2)
key_x=f.bezel_r+2.1
key_slot=Pos(key_x,f.screen_cy,f.body_h-f.wall-1.1)*Box(3+2*key_gap,4+2*key_gap,1.3,align=(Align.CENTER,Align.CENTER,Align.MIN))
front=k.front_result-key_slot
front.color=f.shell_color
publish("front_shell",front,"Front shell with hidden screen bosses",material="petg")