import numpy as np
import trace_model as tm
import random_model as rm
with open('num_tests.txt', 'r') as f:
    for line in f.readlines():
        number_test=line.strip()
def wr_in_txt(fog_depaeture,network_departure,cloud_departure,mrt,str_indes,file_ext):
    #open("fog_dep_"+str_indes+file_ext, 'w')
    fog_depaeture=np.array(fog_depaeture)
    network_departure=np.array(network_departure)
    cloud_departure=np.array(cloud_departure)
    np.savetxt("fog_dep_"+str_indes+file_ext,fog_depaeture,fmt="%.4f	%.4f",delimiter="\n")
    np.savetxt("net_dep_"+str_indes+file_ext,network_departure,fmt="%.4f	%.4f",delimiter="\n")
    np.savetxt("cloud_dep_"+str_indes+file_ext,cloud_departure,fmt="%.4f	%.4f",delimiter="\n")

    file_write_obj4 = open("mrt_"+str_indes+file_ext, 'w')
    file_write_obj4.write("%.4f"%(mrt))
    file_write_obj4.close()

number_test=int(number_test)
file_ext=".txt"
#test
for test_index in range(1,number_test+1):
    with open('mode_'+str(test_index)+file_ext, 'r') as f:
        for line in f.readlines():
            mode=line.strip()
    arrival=[]
    with open('arrival_'+str(test_index)+file_ext, 'r') as f:
        for line in f.readlines():
            arrival.append(float(line.strip()))
    service=[]
    with open('service_'+str(test_index)+file_ext, 'r') as f:
        for line in f.readlines():
            service.append(float(line.strip()))
    network=[]
    with open('network_'+str(test_index)+file_ext, 'r') as f:
        for line in f.readlines():
            network.append(float(line.strip()))

    para=[]
    with open('para_'+str(test_index)+file_ext, 'r') as f:
        for line in f.readlines():
            para.append(float(line.strip()))

    str_indes=str(test_index)
    if mode=="trace":
        fog_depaeture,network_departure,cloud_departure,mrt=tm.trace_modle(arrival,service,network,para)
        wr_in_txt(fog_depaeture,network_departure,cloud_departure,mrt,str_indes,file_ext)
    elif mode=="random":
        fog_depaeture,network_departure,cloud_departure,mrt=rm.random_model(arrival,service,network,para)
        wr_in_txt(fog_depaeture,network_departure,cloud_departure,mrt,str_indes,file_ext)

    

    #call simulation function
    #Write the output files %This can be in the wrapper or your simulation function（每次dep需要清零）

