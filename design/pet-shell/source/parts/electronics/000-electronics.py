f=part("form")
max_tail = param("maximum_solder_tail_below_pcb", 0.6)
socket_tail_limit = param("native_socket_tail_limit",0.85)
raw = Pos(-100,78.5,f.key_pcb_bottom_z)*asset("design/pet-shell/source/assets/29fc2a7f6f6e4b51e461504595b95e87c341bb95897acae1e9132e302d527883.step")
# Finished assembly: trim switch/display header leads to 0.6 mm.
# Native low socket tails project about0.805 mm below carrier and fit the rear cavity; retain them.
trim_plane=f.key_pcb_bottom_z-max_tail
clip=Pos(0,0,trim_plane-100)*Box(400,400,200)
finished_solids=[]
for solid in raw.solids():
    if solid.bounding_box().min.Z >= f.key_pcb_bottom_z-socket_tail_limit-0.0001:
        finished_solids.append(solid)
    else:
        clipped=solid.cut(clip)
        if clipped is not None:
            if isinstance(clipped,list):
                for p in clipped: finished_solids.extend(p.solids())
            else: finished_solids.extend(clipped.solids())
finished=Compound(children=finished_solids)
assert any(s.volume>400 and s.volume<500 for s in finished_solids), "XIAO PCB missing from finished assembly"
assert all(s.bounding_box().min.Z>=f.key_pcb_bottom_z-socket_tail_limit-0.001 for s in finished_solids), "A lead exceeds its seating allowance"
print("Complete carrier solids:",len(raw.solids()),"after lead trimming:",len(finished_solids))
publish("carrier_assembly",finished,"XIAO socket carrier, trimmed leads",role="reference")
