#!/usr/bin/python

import xmlrpclib
import sys, os


def get_cpu_temp():
    pwd = sys.stdin.readline()
    print "in get_cpu_temp"
    return 0

def get_host_name():
    f = os.popen('hostname')
    l = f.readlines()
    name = l[0].split('.')[0]
    f.close()
    return name

def get_cpu_util():
    conn = init_conn()
    
    cmdMap = {  "get_cpu_temp"      :   conn.get_cpu_temp,
                "get_cpu_util"      :   conn.get_cpu_util,
                "get_cpu_freq"      :   conn.get_cpu_freq,
                "set_cpu_freq"      :   conn.set_cpu_freq,
                "get_mem_util"      :   conn.get_mem_util,
                "get_mem_CS"        :   conn.get_mem_CS,
                "get_mem_IN"        :   conn.get_mem_IN,
                "get_net"           :   conn.get_net,
                "get_self_power"    :   conn.get_self_power,
                "get_all_power"     :   conn.get_all_power,
                "get_crac_target"   :   conn.get_crac_target,
                "get_crac_in_temp"  :   conn.get_crac_in_temp,
                "get_crac_out_temp" :   conn.get_crac_out_temp,
             }

    func = "get_cpu_util"
    return cmdMap[func]()

def init_conn():
    host = get_host_name()
    return xmlrpclib.Server("http://%s:%d"%(host, 11001))

def get_power():
    conn = init_conn()
    
    cmdMap = {  "get_cpu_temp"      :   conn.get_cpu_temp,
                "get_cpu_util"      :   conn.get_cpu_util,
                "get_cpu_freq"      :   conn.get_cpu_freq,
                "set_cpu_freq"      :   conn.set_cpu_freq,
                "get_mem_util"      :   conn.get_mem_util,
                "get_mem_CS"        :   conn.get_mem_CS,
                "get_mem_IN"        :   conn.get_mem_IN,
                "get_net"           :   conn.get_net,
                "get_self_power"    :   conn.get_self_power,
                "get_all_power"     :   conn.get_all_power,
                "get_crac_target"   :   conn.get_crac_target,
                "get_crac_in_temp"  :   conn.get_crac_in_temp,
                "get_crac_out_temp" :   conn.get_crac_out_temp,
             }

    func = "get_self_power"
    power = cmdMap[func]()
    return power

def set_freq(freq):
    conn = init_conn()
    
    cmdMap = {  "get_cpu_temp"      :   conn.get_cpu_temp,
                "get_cpu_util"      :   conn.get_cpu_util,
                "get_cpu_freq"      :   conn.get_cpu_freq,
                "set_cpu_freq"      :   conn.set_cpu_freq,
                "get_mem_util"      :   conn.get_mem_util,
                "get_mem_CS"        :   conn.get_mem_CS,
                "get_mem_IN"        :   conn.get_mem_IN,
                "get_net"           :   conn.get_net,
                "get_self_power"    :   conn.get_self_power,
                "get_all_power"     :   conn.get_all_power,
                "get_crac_target"   :   conn.get_crac_target,
                "get_crac_in_temp"  :   conn.get_crac_in_temp,
                "get_crac_out_temp" :   conn.get_crac_out_temp,
             }

    func = "set_cpu_freq"

    freqList = [2395000, 2394000, 2261000, 2128000, 1995000, 1862000, 1729000, 1596000, 1463000, 1330000, 1197000]
    try:
        newFreq = int(freq)
    except ValueError:
        print "The Parameter has to be an integer"
        return 4
    if newFreq not in freqList:
        print "The frequency choices are:"
        print freqList
        return 5
    cmdMap[func](newFreq)
    return 0

def main():
    conn = init_conn()
    
    cmdMap = {  "get_cpu_temp"      :   conn.get_cpu_temp,
                "get_cpu_util"      :   conn.get_cpu_util,
                "get_cpu_freq"      :   conn.get_cpu_freq,
                "set_cpu_freq"      :   conn.set_cpu_freq,
                "get_mem_util"      :   conn.get_mem_util,
                "get_mem_CS"        :   conn.get_mem_CS,
                "get_mem_IN"        :   conn.get_mem_IN,
                "get_net"           :   conn.get_net,
                "get_self_power"    :   conn.get_self_power,
                "get_all_power"     :   conn.get_all_power,
                "get_crac_target"   :   conn.get_crac_target,
                "get_crac_in_temp"  :   conn.get_crac_in_temp,
                "get_crac_out_temp" :   conn.get_crac_out_temp,
             }
    
    freqList = [2395000, 2394000, 2261000, 2128000, 1995000, 1862000, 1729000, 1596000, 1463000, 1330000, 1197000]

#    print cmdMap["get_cpu_temp"]()
#    print cmdMap["get_cpu_util"]()
#    print cmdMap["get_cpu_freq"]()
#    print cmdMap["set_cpu_freq"](1995000)
#    print cmdMap["get_mem_util"]()
#    print cmdMap["get_mem_CS"]()
#    print cmdMap["get_mem_IN"]()
#    print cmdMap["get_net"]()
#    print cmdMap["get_self_power"]()
#    print cmdMap["get_all_power"]()
#    print cmdMap["get_crac_target"]()
#    print cmdMap["get_crac_in_temp"]()
#    print cmdMap["get_crac_out_temp"]()

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "the api takes only 1 or 2 parameters"
        return 1

    func = sys.argv[1]
    if func not in cmdMap.keys():
        print "Please type the valid command:"
        print cmdMap.keys()
        return 2
    else:
        if "set_cpu_freq" == func:
            if  len(sys.argv) < 3:
                print "Please specify the new frequency!"
                return 3
            else:
                try:
                    newFreq = int(sys.argv[2])
                except ValueError:
                    print "The Parameter has to be an integer"
                    return 4
                if newFreq not in freqList:
                    print "The frequency choices are:"
                    print freqList
                    return 5
                print cmdMap[func](newFreq)
        else:
            print cmdMap[func]()


if __name__ == "__main__":
    main()
