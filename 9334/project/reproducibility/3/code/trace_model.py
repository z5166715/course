

def trace_modle(arrival,service,network,para):
    fogTimeLimit=para[0]
    fogTimeToCloudTime=para[1]
    fog_depaeture=[]
    network_departure=[]
    cloud_departure=[]
    response_time=[]
    #<arrival time, dep time>

    totalNumberOfJobsCompleted=0 #compute completed jobs

    master_clock=0
    pre_master_clock=0

    job_list_fog=[]
    job_list_network=[]
    job_list_cloud=[]
    #2d list

    #--------------------------------------

    next_arr_fog=arrival[0]
    next_dep_fog_woC=float('inf')
    next_dep_fog_wC=float('inf')
    next_dep_net=float('inf')
    next_dep_cloud=float('inf')

    event_list=[next_arr_fog,next_dep_fog_woC,next_dep_fog_wC,next_dep_net,next_dep_cloud]
    #five event
    arrival_list_without_cloud=[]
    arrival_list_without_cloud2=[]
    arrival_list_with_cloud=[]
    arrival_list_with_cloud2=[]
    service_at_cloud=[]
    for i in range(len(service)):
        if service[i] <= fogTimeLimit:
            arrival_list_without_cloud.append([arrival[i],service[i]])
            arrival_list_without_cloud2.append(arrival[i])
            service_at_cloud.append(0)
        else:
            arrival_list_with_cloud.append([arrival[i],service[i]])
            arrival_list_with_cloud2.append(arrival[i])
            cloud_service=fogTimeToCloudTime*(service[i]-fogTimeLimit)
            service_at_cloud.append(cloud_service)
            service[i]=fogTimeLimit

    #build service at cloud


    master_clock = arrival[0]

    while totalNumberOfJobsCompleted<len(arrival):
        time_passed=master_clock-pre_master_clock
        event=event_list.index(min(event_list))

        if event ==0:#arrival
            if job_list_fog==[]:
                index_s=arrival.index(event_list[0])
                job_list_fog.append([event_list[0],service[index_s]])
            else:
                for ele in job_list_fog:
                    ele[1]=ele[1]-time_passed/len(job_list_fog)
                index_s=arrival.index(event_list[0])
                job_list_fog.append([event_list[0],service[index_s]])
            if job_list_network!=[]:
                for ele in job_list_network:
                    ele[1]=ele[1]-time_passed
            if job_list_cloud!=[]:
                for ele in job_list_cloud:
                    ele[1]=ele[1]-time_passed/len(job_list_cloud)
                
            #update joblist
            if index_s+1<=len(arrival)-1:
                next_arr_fog=arrival[index_s+1]
            else:
                next_arr_fog=float('inf')
            #update next_arrivl

            if len(job_list_fog)<=1:
                if arrival[index_s] in arrival_list_without_cloud2:
                    next_dep_fog_woC=service[index_s]+master_clock
                elif arrival[index_s] in arrival_list_with_cloud2:
                    next_dep_fog_wC=service[index_s]+master_clock
            else:
                l_w=[]
                l_wo=[]
                for e in job_list_fog:
                    if e[0] in arrival_list_without_cloud2:
                        l_wo.append(e[1])
                    else:
                        l_w.append(e[1])
                
                if len(l_wo)!=0:
                    next_dep_fog_woC=min(l_wo)*len(job_list_fog)+master_clock
                else:
                    next_dep_fog_woC=float('inf')
                if len(l_w)!=0:
                    next_dep_fog_wC=min(l_w)*len(job_list_fog)+master_clock
                else:
                    next_dep_fog_wC=float('inf')
                
            event_list[0]=next_arr_fog
            event_list[1]=next_dep_fog_woC
            event_list[2]=next_dep_fog_wC
            #update event_list


        if event ==1:#dep from fog without cloud 
            l_min=[]
            for ele in job_list_fog:
                ele[1]=ele[1]-time_passed/len(job_list_fog)
                l_min.append(ele[1])
            if job_list_network!=[]:
                for ele in job_list_network:
                    ele[1]=ele[1]-time_passed
            if job_list_cloud!=[]:
                for ele in job_list_cloud:
                    ele[1]=ele[1]-time_passed/len(job_list_cloud)
            #update job_listt

            #find mini time
            for el in job_list_fog:
                if el[1]==min(l_min):
                    fog_depaeture.append([el[0],master_clock])
                    response_time.append(master_clock-el[0])
                    job_list_fog.remove(el)
            if len(job_list_fog)==0:
                next_dep_fog_woC=float('inf')
            else:
                l_w=[]
                l_wo=[]
                for e in job_list_fog:
                    if e[0] in arrival_list_without_cloud2:
                        l_wo.append(e[1])
                    else:
                        l_w.append(e[1])
                if len(l_wo)!=0:
                    next_dep_fog_woC=min(l_wo)*len(job_list_fog)+master_clock
                else:
                    next_dep_fog_woC=float('inf')
                if len(l_w)!=0:
                    next_dep_fog_wC=min(l_w)*len(job_list_fog)+master_clock
                else:
                    next_dep_fog_wC=float('inf')


            event_list[1]=next_dep_fog_woC
            event_list[2]=next_dep_fog_wC
            totalNumberOfJobsCompleted=totalNumberOfJobsCompleted+1 #compute completed jobs
            

            
        if event==2:# dep from fog with cloud 
            l_min=[]
            for ele in job_list_fog:
                ele[1]=ele[1]-time_passed/len(job_list_fog)
                l_min.append(ele[1])
            if job_list_network!=[]:
                for ele in job_list_network:
                    ele[1]=ele[1]-time_passed
            if job_list_cloud!=[]:
                for ele in job_list_cloud:
                    ele[1]=ele[1]-time_passed/len(job_list_cloud)
            #update job_listt
            for el in job_list_fog:
                if el[1]==min(l_min):
                    fog_depaeture.append([el[0],master_clock])
                    n_i=arrival.index(el[0])
                    job_list_network.append([el[0],network[n_i]])
                    job_list_fog.remove(el)
            if len(job_list_fog)==0:
                next_dep_fog_wC=float('inf')
            else:
                l_w=[]
                l_wo=[]
                for e in job_list_fog:
                    if e[0] in arrival_list_without_cloud2:
                        l_wo.append(e[1])
                    else:
                        l_w.append(e[1])
                if len(l_wo)!=0:
                    next_dep_fog_woC=min(l_wo)*len(job_list_fog)+master_clock
                else:
                    next_dep_fog_woC=float('inf')
                if len(l_w)!=0:
                    next_dep_fog_wC=min(l_w)*len(job_list_fog)+master_clock
                else:
                    next_dep_fog_wC=float('inf')
            if len(job_list_network)<=1:
                next_dep_net=network[n_i]+master_clock
            else:
                min_n=[]
                for e in job_list_network:
                    min_n.append(e[1])
                next_dep_net=min(min_n)+master_clock

            event_list[1]=next_dep_fog_woC
            event_list[2]=next_dep_fog_wC
            event_list[3]=next_dep_net


        if event ==3:#depture from network
            if job_list_fog!=[]:
                for ele in job_list_fog:
                    ele[1]=ele[1]-time_passed/len(job_list_fog)
            if job_list_cloud!=[]:
                for ele in job_list_cloud:
                    ele[1]=ele[1]-time_passed/len(job_list_cloud)
            l_min=[]
            for ele in job_list_network:
                ele[1]=ele[1]-time_passed
                l_min.append(ele[1])
            #update job list
            for el in job_list_network:
                if el[1]==min(l_min):
                    network_departure.append([el[0],master_clock])
                    n_j=arrival.index(el[0])
                    job_list_cloud.append([el[0],service_at_cloud[n_j]])
                    job_list_network.remove(el)
            
            if len(job_list_network)==0:
                next_dep_net=float('inf')
            else:
                l_n=[]
                for e in job_list_network:
                   l_n.append(e[1])
                next_dep_net=min(l_n)+master_clock

            min_c=[]    
            for e in job_list_cloud:
                min_c.append(e[1])
            next_dep_cloud=min(min_c)*len(job_list_cloud)+master_clock
            event_list[3]=next_dep_net
            event_list[4]=next_dep_cloud
        if event==4:#depture from cloud
            if job_list_fog!=[]:
                for ele in job_list_fog:
                    ele[1]=ele[1]-time_passed/len(job_list_fog)
            if job_list_network!=[]:
                for ele in job_list_network:
                    ele[1]=ele[1]-time_passed
            c_min=[]
            for ele in job_list_cloud:
                ele[1]=ele[1]-time_passed/len(job_list_cloud)
                c_min.append(ele[1])
            #update joblist
            for el in job_list_cloud:
                if el[1]==min(c_min):
                    cloud_departure.append([el[0],master_clock])
                    response_time.append(master_clock-el[0])
                    job_list_cloud.remove(el)
            
            if len(job_list_cloud)==0:
                next_dep_cloud=float('inf')
            else:
                min_c=[]
                for e in job_list_cloud:
                    min_c.append(e[1])
                next_dep_cloud=min(min_c)*len(job_list_cloud)+master_clock
            event_list[4]=next_dep_cloud
            totalNumberOfJobsCompleted=totalNumberOfJobsCompleted+1       
            
            
            
        pre_master_clock=master_clock
        master_clock=min(event_list)

    #arrival_time sort
    fog_depaeture.sort()
    network_departure.sort()
    cloud_departure.sort()
        
    for x in fog_depaeture:
        x[1]=round(x[1],4)
    
    for x in network_departure:
        x[1]=round(x[1],4)
    
    for x in cloud_departure:
        x[1]=round(x[1],4)
    
    meanres=sum(response_time)/len(response_time)
    mrt=round(meanres,4)
    return fog_depaeture,network_departure,cloud_departure,mrt

