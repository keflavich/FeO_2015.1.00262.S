import paths
import datetime
import glob
import os

def get_ant_pos(fn):
    ants = {}
    with open(fn, 'r') as fh:
        start = False
        for line in fh.readlines():
            if start and 'East' not in line and 'Station' not in line:
                ls = line.split()
                ID, east, north = ls[0],ls[7],ls[8]
                size = ls[3]
                ants[ID] = (east,north)
            if 'Antennas:' in line:
                start = True

    return ants, size

def ants_to_baselines(ants):
    bls = {}
    for ant1 in ants:
        for ant2 in ants:
            if ant1==ant2:
                continue
            else:
                x1,y1 = float(ants[ant1][0]), float(ants[ant1][1])
                x2,y2 = float(ants[ant2][0]), float(ants[ant2][1])
                d = ((x1-x2)**2 + (y1-y2)**2)**0.5
                bls[ant1+"-"+ant2] = d
    return bls


def longest_baseline(fn):
    return max(ants_to_baselines(get_ant_pos(fn)[0]).values())
def shortest_baseline(fn):
    return min(ants_to_baselines(get_ant_pos(fn)[0]).values())

def get_date(fn):
    with open(fn, 'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if 'Observed from' in line:
                dateline = line
                break
        start_date = dateline.split()[2].split("/")[0]
        end_date = dateline.split()[4].split("/")[0]

    return start_date, end_date

def get_total_time(fn):
    with open(fn, 'r') as fh:
        lines = fh.readlines()
        for line in lines:
            if 'Total elapsed time' in line:
                timeline = line
                break
        time = timeline.split()[-2]
    return time

def get_metadata_line(fn, DEBUG=False):
    ants,size = get_ant_pos(fn)
    start_date, end_date = get_date(fn)
    baselines = ants_to_baselines(ants)
    longestbl = max(baselines.values())
    shortestbl = min(baselines.values())
    integrationtime = get_total_time(fn)

    if start_date != end_date:
        return None
    
    line = "{0} & {1}m & {2} & {3}-{4} & {5}\\\\".format(start_date, int(round(float(size))),
                                                     int(round(float(integrationtime))),
                                                     int(round(shortestbl)),
                                                     int(round(longestbl)),
                                                     len(ants))
    if DEBUG:
        print(line)
    return line, (start_date, size, integrationtime, shortestbl, longestbl, len(ants))

def make_meta_tables(listobspath=os.path.join(paths.root, 'listobs'), DEBUG=False):
    searchstr = os.path.join(listobspath, '*.listobs')
    listfiles=glob.glob(searchstr)

    lines = [get_metadata_line(fn, DEBUG=DEBUG) for fn in listfiles]
    lines = [l for l in lines if l is not None]
    print()
    print()

    dct = {}
    dct1 = {}
    for prtline,(date, size, integrationtime, shortestbl, longestbl, nants) in lines:
        if date in dct:
            if DEBUG:
                print("old integration time for {0} = {1}".format(date, integrationtime))
                print("will add {0}".format(dct1[date][2]))
                print("new sum is {0}".format(float(dct1[date][2])+float(integrationtime)))
            integrationtime = float(dct1[date][2]) + float(integrationtime)
            if DEBUG:
                print("new integration time for {0} = {1}".format(date, integrationtime))
            dct[date] = "{0} & {1}m & {2} & {3}-{4} & {5}\\\\".format(date,
                                                                      int(round(float(size))),
                                                                      int(round(float(integrationtime))),
                                                                      int(round(shortestbl)),
                                                                      int(round(longestbl)),
                                                                      nants)
            dct1[date] = [date,size,integrationtime,shortestbl,longestbl]
        else:
            dct[date] = prtline
            dct1[date] = [date,size,integrationtime,shortestbl,longestbl]


    printlines = []
    for k,v in sorted(dct.items(), key=lambda x: datetime.datetime.strptime(x[0][:11],'%d-%b-%Y')):
        print("LINE {0}: {1}".format(k, v))
        printlines.append(v)

    return lines, printlines

if __name__ == "__main__":
    listobspath = os.path.join(paths.root, 'reduction/listobs/')
    table_12m, prttable_12m = make_meta_tables(DEBUG=True, listobspath=listobspath)

    
    table_string = r'''
\begin{{table*}}[htp]
\centering
\caption{{Observation Summary}}
\begin{{tabular}}{{lllll}}
\label{{tab:observations}}
Date & Array & Observation Duration &  Baseline Length Range  & \# of antennae\\
     &       & seconds              & meters                    & \\
\hline

{data}

\hline
\end{{tabular}}
\end{{table*}}
'''

    print(table_string.format(data="\\\\\n".join(prttable_12m)))

    with open(paths.tpath('obs_metadata.tex'), 'w') as fh:
        fh.write(table_string.format(data="\\\\\n".join(prttable_12m)))
