## Calculate worst case delay and save result to device class objects.
#
#   @param tsn               TSN object (input data saved in classes)
#
# @return Nothing.
def worst_case_delay(tsn):
    add_stream_to_switch_device(tsn)        # Add streams to every switch
    for device in tsn.devices:
        cycle = 0
        for s in device.egressPort:
            cycle += s.stream_bandwidth/device.speed
        device.cycleTime = cycle

## Adds the streams to only those devices that are switches. Saved streams are kept in Device.egressPort[].
#
#   @param tsn               TSN object (input data saved in classes)
#
# @return Nothing.
def add_stream_to_switch_device(tsn):
    for s in tsn.streams:
        s.solution_Links(tsn)
        for l in s.solution_links:
            if l.src.type == "Switch":
                l.src.egressPort.append(s)

    for d in tsn.devices:
        d.egressPort = list(dict.fromkeys(d.egressPort)) 

