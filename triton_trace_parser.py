 #!/usr/bin/python3

import json
import operator

def trace(json_data):

    time = {}
    timesum = {}
    num = 1
    count = 0
    starttime = 0
    for data in json_data:
        if data["id"]==num+1:
            if "GRPC_WAITREAD_START" in time:
                count += 1
                time.clear()
            num += 1
            if num == 2+count:
                timesum = time.copy()
            else:
                for k,v in time.items():
                    timesum[k] += v
            time.clear()

        if data["id"]==num and "timestamps" in data:
            timestamps = data["timestamps"]
            for timestamp in timestamps:
                if timestamp["name"]=="HTTP_RECV_START":
                    starttime = timestamp["ns"]
                time[timestamp["name"]] = timestamp["ns"]- starttime

    if num == 1+count:
        timesum = time.copy()
    else:
        for k,v in time.items():
            timesum[k] += v

    stime= sorted(timesum.items(), key=operator.itemgetter(1))
    print_func(stime,num-count)



def print_func(stime,num):

    value = []
    for i in range(10):
        value.append(stime[i+1][1]-stime[i][1])

    ### print ###
    flag=True

    print()
    for t in stime:
        print('%-21s'%(t[0]), end="")
    print()

    for t in stime:
        print('%-21s'%(str(t[1]//num)+" ns"), end="")
    print()
    for i in stime:
        print("----+----------------",end="")
    print(">")
    for v in value:
        if flag:
            print('%17s ns'%(v//num), end="")
            flag=False
            continue
        print('%18s ns'%(v//num), end="")
    print("\n")

    print("time")
    for t in stime:
        print('%s'%(str(t[1]//num)))
    print("\n")
    print("interval")
    for v in value:
        print('%s'%(v//num))
    print("\n")



if __name__ == '__main__':

    with open("/tmp/trace.json", "r") as f:
        contents = f.read()
        json_data = json.loads(contents)

    trace(json_data)


    
