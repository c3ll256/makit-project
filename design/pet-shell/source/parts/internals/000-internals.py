f = part("form")
show_refs = param("show_reference_parts", 1.0)

# Grove 1.2in IPS display: 40x40 board with 8 edge notches (vendor .brd), LCM on the front, Grove socket on the back
bcx, bcy = f.board_c
board = Pos(bcx, bcy, f.board_back_z) * Box(f.DISP_BOARD, f.DISP_BOARD, f.DISP_BOARD_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
for (nx, ny) in [(-10, 20), (10, 20), (-10, -20), (10, -20), (20, 10), (20, -10), (-20, 10), (-20, -10)]:
    board = board - Pos(bcx + nx, bcy + ny, f.board_back_z) * Cylinder(2.0, 10)
lcm = Pos(bcx, bcy + 0.25, f.board_front_z) * Box(f.DISP_LCM_W, f.DISP_LCM_H, f.DISP_LCM_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
j1 = Pos(bcx, (f.j1_box[1] + f.j1_box[2]) / 2, f.board_back_z) * Box(2 * f.j1_box[0], f.j1_box[2] - f.j1_box[1], f.DISP_J1_H, align=(Align.CENTER, Align.CENTER, Align.MAX))
board.color = srgb("#1f6fb8")
lcm.color = srgb("#14161c")
j1.color = srgb("#f2f2f2")
publish("display_ref", [board, lcm, j1], "Grove 1.2in IPS display", role="reference")

battery = Pos(f.bat_c[0], f.bat_c[1], f.bat_floor_z) * Box(f.BAT_X, f.BAT_Y, f.BAT_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
battery.color = srgb("#b8b8b8")
publish("battery_ref", battery, "503035 LiPo", role="reference")

xpcb = Pos(f.xiao_xc, 0, f.xiao_bottom_z) * Box(f.XIAO_L, f.XIAO_W, f.XIAO_PCB_T, align=(Align.CENTER, Align.CENTER, Align.MIN))
# USB-C receptacle: 8.94 x 3.2 shell with fully round ends
usb_len = 7.4
usb = Pos(f.xiao_x1 + f.XIAO_USB_OVERHANG - usb_len / 2, 0, f.xiao_bottom_z + f.XIAO_PCB_T + f.XIAO_USB_H / 2) * Rot(0, 90, 0) * extrude(SlotOverall(8.94, f.XIAO_USB_H, rotation=90), usb_len / 2, both=True)
xpcb.color = srgb("#2b5fa8")
usb.color = srgb("#c0c0c0")
publish("xiao_ref", [xpcb, usb], "XIAO ESP32-S3", role="reference")


# Existing detachable XIAO display harness, retained alongside the PCB.
hdr = Pos((f.dupont_x0 + f.dupont_x1)/2, -f.XIAO_W/2 + f.HDR_BODY_W/2, f.dupont_z0) * Box(f.dupont_x1-f.dupont_x0, f.HDR_BODY_W, f.HDR_BODY_H, align=(Align.CENTER,Align.CENTER,Align.MIN))
plugs=[hdr]
for k in f.dupont_pins:
    plugs.append(Pos(f.xiao_pin_x(k),-f.XIAO_W/2 + f.HDR_BODY_W + f.DUPONT_LEN/2 + 0.1,f.dupont_z0)*Box(f.DUPONT_SQ-0.1,f.DUPONT_LEN,f.HDR_BODY_H,align=(Align.CENTER,Align.CENTER,Align.MIN)))
for p in plugs: p.color=srgb("#202020")
publish("dupont_ref",plugs,"XIAO detachable display harness",role="reference")
