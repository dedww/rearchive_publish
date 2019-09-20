import json_worl

def my_function():
    array = list()   
    for x in range(2):
        node =  {'id':x,'data':'data'}
        data = {'data':node}
        array.append(data)
    edge = {'source':0,'target':1}
    edgearray = list()
    edgearray.append(edge)

    final = {'nodes':array,'edges':edgearray}
    print(final)
    
my_function()
