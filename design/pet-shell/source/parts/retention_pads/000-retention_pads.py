f=part("form")
k=part("screen_keeper")
nominal_t=param("pad_nominal_thickness",1.0)
pad_w=param("screen_pad_width",3.2)
pad_h=param("screen_pad_height",2.8)
sp=[]
for x in (-11.39,11.39):
 for y in (f.board_c[1]-f.DISP_H/2+2.5,f.board_c[1]+f.DISP_H/2-2.5):
  p=Pos(x,y,k.z+k.t)*Box(pad_w,pad_h,nominal_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
  p=p-Pos(x,y,k.z+k.t-0.1)*Cylinder(1.1,nominal_t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
  sp.append(p)
publish("screen_foam_pads",sp,"Screen corner preload foam",role="reference")
ap=[Pos(x,f.adapter_cy+2,f.adapter_bottom_z-0.8)*Box(2.6,3,nominal_t,align=(Align.CENTER,Align.CENTER,Align.MIN)) for x in (-8.5,8.5)]
publish("adapter_foam_pads",ap,"Adapter preload foam",role="reference")
hp=Pos(18.5,0,14.785-nominal_t)*Box(5,6,nominal_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
publish("xiao_foam_pad",hp,"XIAO shield hold-down foam",role="reference")
fit("screen_foam_pads","display_ref",kind="compliant",budget_mm=0.25,reason="1mm foam compressed by0.2mm on display PCB corner lands; never glass")
fit("adapter_foam_pads","screen_adapter_assembly",kind="compliant",budget_mm=0.25,reason="1mm foam compressed0.2mm against adapter PCB underside, keeps square socket seated")
fit("xiao_foam_pad","carrier_assembly",kind="compliant",budget_mm=0.25,reason="1mm foam compressed0.2mm on rigid RF shield, prevents XIAO rocking")
