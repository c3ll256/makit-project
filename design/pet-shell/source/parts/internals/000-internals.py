f=part("form")
show_refs=param("show_reference_parts",1.0)
corner=param("display_pcb_corner_chamfer",0.8)
pin_size=param("display_pin_square",0.64)
hdr_body=param("display_header_body",2.5)
pin_len=param("tft154_exposed_pin_length",6.5)
bcx,bcy=f.board_c
board=Pos(bcx,bcy,f.board_back_z)*Box(f.DISP_W,f.DISP_H,f.DISP_BOARD_T,align=(Align.CENTER,Align.CENTER,Align.MIN))
board=chamfer(board.edges().filter_by(Axis.Z),corner)
holes=[]
for sx in (-1,1):
    for sy in (-1,1):
        holes.append(Pos(bcx+sx*(f.DISP_W/2-f.DISP_HOLE_INSET),bcy+sy*(f.DISP_H/2-f.DISP_HOLE_INSET),f.board_back_z-0.1)*Cylinder(f.DISP_HOLE_R,f.DISP_BOARD_T+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN)))
board=board.cut(*holes)
frame=Pos(bcx,bcy,f.board_front_z)*Box(f.DISP_LCM_W,f.DISP_LCM_H,f.DISP_LCM_T,align=(Align.CENTER,Align.CENTER,Align.MIN))
# Thin metal frame surrounds the active glass; no generic 40 mm placeholder.
active=param("tft154_active_width",27.72)
glass_cut=Pos(f.screen_cx,f.screen_cy,f.lcm_front_z)*Box(active,active,0.5)
frame=frame-glass_cut
glass=Pos(f.screen_cx,f.screen_cy,f.lcm_front_z-0.25)*Box(active,active,0.5)
hy=bcy-f.DISP_H/2+f.DISP_HEADER_Y
header=Pos(0,hy,f.board_back_z-hdr_body)*Box(20.32,2.5,hdr_body,align=(Align.CENTER,Align.CENTER,Align.MIN))
pins=[]
for i in range(8):
    pins.append(Pos((i-3.5)*2.54,hy,f.board_back_z-hdr_body-pin_len)*Box(pin_size,pin_size,pin_len,align=(Align.CENTER,Align.CENTER,Align.MIN)))
board.color=srgb("#277ba3")
frame.color=srgb("#63686d")
glass.color=srgb("#14171e")
header.color=srgb("#26282b")
for p in pins:p.color=srgb("#b9a15a")
publish("display_ref",[board,frame,glass,header,*pins],"YouXin 1.54in 8P ST7789",role="reference")
battery=Pos(f.bat_c[0],f.bat_c[1],f.bat_floor_z)*Box(f.BAT_X,f.BAT_Y,f.BAT_T,align=(Align.CENTER,Align.CENTER,Align.MIN))
battery.color=srgb("#b8b8b8")
publish("battery_ref",battery,"503035 LiPo",role="reference")