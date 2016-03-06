# This is only a small script

fp = open('big_data.edge', 'rb')
fo = open('compress.edge', 'wb')
line = fp.readline()
edges = set()
ctr = 0
while line:
    pair = line.strip(' \r\n').split(':')
    source = pair[0]
    for i in pair[1].split(' '):
        edge = pair[0] + ',' + i
        edges.add(edge)
    ctr += 1
    if ctr % 100 == 0:
        print ctr, edge

    line = fp.readline()

for edge in edges:
    fo.write(edge+'\r\n')

print ('Finished!')
fp.close()
fo.close()
