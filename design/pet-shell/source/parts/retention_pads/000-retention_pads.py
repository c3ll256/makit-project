f=part("form")
k=part("screen_keeper")
nominal_t=param("pad_nominal_thickness",1.0)
pad_w=param("screen_pad_width",3.2)
pad_h=param("screen_pad_height",2.8)
sp=[]
for x in (-k.pad_x,k.pad_x):
 for y in (f.board_c[1]-f.DISP_H/2+2.5,f.board_c[1]+f.DISP_H/2-2.5):
  p=Pos(x,y,k.z+k.t)*Box(pad_w,pad_h,nominal_t,align=(Align.CENTER,Align.CENTER,Align.MIN))
  p=p-Pos(x,y,k.z+k.t-0.1)*Cylinder(1.1,nominal_t+0.2,align=(Align.CENTER,Align.CENTER,Align.MIN))
  sp.append(p)
publish("screen_foam_pads",sp,"Screen corner preload foam",role="reference")
fit("screen_foam_pads","display_ref",kind="compliant",budget_mm=0.25,reason="1mm foam compressed by0.2mm on display PCB corner lands; never glass")