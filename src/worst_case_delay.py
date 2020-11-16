def worst_case_delay(tsn):
    # print("worst_case_delay")
    add_priority_to_streams(tsn)            # Assign priorities to streams depending on deadline
    add_stream_to_switch_device(tsn)        # Add streams to every switch
    cycle = 0
    for d in tsn.devices:
        for s in d.egressPort:
            cycle += s.size/d.speed 
        d.cycleTime = cycle
        # print(" \033[0m", d.name," cycle time = ", d.cycleTime)


def add_priority_to_streams(tsn):
    # print("add_priority_to_streams")
    tsn.streams.sort(key=lambda x: x.deadline)
    for i in range(len(tsn.streams)):
        tsn.streams[i].priority = 8 - int(i*8/len(tsn.streams))   #divide the streams into 8 equal groups and assing priority based on deadline
        # print(tsn.streams[i].id," priority = ", tsn.streams[i].priority, " deadline = ", tsn.streams[i].deadline)


def add_stream_to_switch_device(tsn):
    # print("add_stream_to_switch_device")
    for s in tsn.streams:
        s.solution_Links(tsn)
        for l in s.solution_links:
            if l.src.type == "Switch":
                l.src.egressPort.append(s)
                # print(s.id, "uses link with source device = ", l.src.name)

    for d in tsn.devices:
        d.egressPort = list(dict.fromkeys(d.egressPort))

    # for d in tsn.devices:
    #     if d.type == "Switch":
    #         print("\033[93m", d.name)
    #         for stream in d.egressPort:
    #             print("\033[96m", stream.id)
