f=part("form")
step_top=param("step_pcb_top",0.995)
max_tail=param("finished_tail",0.60)
raw=Pos(-100,78.5,f.key_pcb_top_z-step_top)*asset("design/pet-shell/source/assets/9bd7e373a98483f95674f8d76e7d3f86b19858da93ef1c2d9e58967bc8d17a4e.step")
rest=[];socket=[];spk=[];xiao=[];usb=[]
for s in raw.solids():
 b=s.bounding_box();c=b.center()
 # Omit copper artwork and plated barrels from the mechanical assembly.
 if b.size.Z < 0.10 and b.max.Z < f.key_pcb_top_z+0.11: continue
 if b.size.X < 1.3 and b.size.Y < 1.3 and b.max.Z <= f.key_pcb_top_z+0.06 and b.min.Z >= f.key_pcb_bottom_z-0.06: continue
 if 23.48<c.X<27.32 and -14.4<c.Y<-9.6 and b.min.Z>=4.70 and b.max.Z<=5.98:
  continue
 if b.min.Z<f.key_pcb_bottom_z-max_tail:
  s=s-Pos(0,0,f.key_pcb_bottom_z-max_tail-50)*Box(130,130,100)
 if not s:continue
 pieces=list(s.solids())
 if -10.7<c.X<10.7 and -15.8<c.Y<-13.2 and b.max.Z>f.key_pcb_top_z+2:
  socket.extend(pieces)
 elif -20.0<c.X<-11 and -18.5<c.Y<-9.9 and b.min.Z>4.69 and b.max.Z<8.4:
  spk.extend(pieces)
 elif b.min.Z>=f.key_pcb_top_z+5 and b.max.X>31 and abs(c.Y)<4:
  usb.extend(pieces)
 elif b.min.Z>=f.key_pcb_top_z+5 and 9<c.X<32 and abs(c.Y)<9:
  xiao.extend(pieces)
 else:rest.extend(pieces)
publish("carrier_assembly",rest,"圆角 XIAO 载板",role="reference")
publish("xiao_board",xiao,"Seeed Studio XIAO ESP32S3",role="reference")
publish("usb_body",usb,"XIAO 自带 USB-C",role="reference")
publish("display_socket",socket,"J_SCREEN 八针直插屏座",role="reference")
publish("spk_socket",spk,"SPK1 两针喇叭座",role="reference")
# The connector contact springs are supplied in their unmated state.
fit("display_ref","display_socket",kind="compliant",budget_mm=0.12,reason="Both spring faces at each of the eight socket contacts deflect onto the 0.64 mm screen pin. The plastic entry stays clear.")
# The purchased XIAO reference splits its USB shell and tongue from its contact strip.
fit("usb_body","xiao_board",kind="nominal_contact",budget_mm=0.25,reason="Contact inserts embedded in the moulded USB tongue and mounting feet of the factory-assembled Seeed module, represented in one vendor STEP.")
fit("carrier_assembly","xiao_board",kind="nominal_contact",budget_mm=0.32,reason="Soldered XIAO header tails enter its plated through holes at the two 2.54 mm pitch pad rows; the supplier model includes solid pad geometry there.")