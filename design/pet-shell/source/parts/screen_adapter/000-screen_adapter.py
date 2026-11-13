f=part("form")
tail=param("adapter_solder_tail_limit",0.6)
raw=asset("design/pet-shell/source/assets/61ba7b0521c247fbcb54fc5878295b841b6ab5a899b6dd0c7517b12351e67239.step")
parts=[]
for s in raw.solids():
 b=s.bounding_box()
 if abs(b.center().Y+103.5)<1.3 and b.size.X<1.5:
  s=s-Pos(100,-100,-100-tail)*Box(100,100,200)
  if s is None:continue
 if isinstance(s,list):parts.extend([a for p in s for a in p.solids()])
 else:parts.extend(s.solids())
assembly=Pos(-100,100+f.adapter_cy,f.adapter_bottom_z)*Compound(children=parts)
publish("screen_adapter_assembly",assembly,"Thin screen adapter, trimmed tails",role="reference")
