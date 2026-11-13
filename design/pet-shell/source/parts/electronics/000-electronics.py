f=part("form")
max_tail = param("maximum_solder_tail_below_pcb", 0.6)
socket_tail_limit = param("native_socket_tail_limit",0.6)
raw = Pos(-100,78.5,f.key_pcb_bottom_z)*asset("design/pet-shell/source/assets/1923175e7cab06faa9851cbba0d6325b141ea46cefcecbd8921588a036ad542d.step")
# Finished 1.0mm carrier: trim all through-board leads and solder peaks,
# including low socket tails, to at most0.6mm below the PCB.
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
