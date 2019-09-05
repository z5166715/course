import numpy as np

#---------------------------------------------其上为读数据，以下为主体
def random_model(arrival,service,network,para):
    lam=arrival[0]
    a1=service[0]
    a2=service[1]
    b=service[2]
    v1=network[0]
    v2=network[1]
    fogTimeLimit=para[0]
    fogTimeToCloudTime=para[1]
    time_end=para[2]
    np.random.seed(2)#seed

    def ran_arrival(lam):# 随机生成arrival_time 函数
        u=np.random.uniform(0,1)
        t=-np.log(1-u)/lam
        return t

    def ran_network(v1,v2):#随机生成network late
        n=np.random.uniform(v1,v2)
        return n


    def ran_service(a1,a2,b):
        u=np.random.uniform(0,1)
        b_=1-b
        r=b_/(a2**b_-a1**b_)
        s_t=((b_/r)*(u+((r/b_)*a1**b_)))**(1/b_)
        return s_t

    arrival=[]
    nex_arr=ran_arrival(lam)

    while nex_arr<time_end:
        arrival.append(nex_arr)
        inter_t=ran_arrival(lam)
        this_arrival=nex_arr
        nex_arr=this_arrival+inter_t
        
    network=[]
    service=[]
    for i in range(len(arrival)):
        network.append(ran_network(v1,v2))
        service.append(ran_service(a1,a2,b))

    
    fog_depaeture=[]
    network_departure=[]
    cloud_departure=[]
    response_time=[]
    #根据以上信息写文件，格式为 <arrival time, dep time>

    totalNumberOfJobsCompleted=0 #计数完成的任务，只在dep without cloud 和 dep from cloud 时发生

    master_clock=0
    pre_master_clock=0

    job_list_fog=[]
    job_list_network=[]
    job_list_cloud=[]
    #以上是二维数组

    #以下为预处理--------------------------------------

    next_arr_fog=arrival[0]
    next_dep_fog_woC=float('inf')
    next_dep_fog_wC=float('inf')
    next_dep_net=float('inf')
    next_dep_cloud=float('inf')

    event_list=[next_arr_fog,next_dep_fog_woC,next_dep_fog_wC,next_dep_net,next_dep_cloud]
    #5个event
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
            network[i]=0.0
        else:
            arrival_list_with_cloud.append([arrival[i],service[i]])
            arrival_list_with_cloud2.append(arrival[i])
            cloud_service=fogTimeToCloudTime*(service[i]-fogTimeLimit)
            service_at_cloud.append(cloud_service)
            service[i]=fogTimeLimit

    #分别将走net的和不走net的，并建立 service at cloud 表


    master_clock = arrival[0]

    while master_clock < time_end:
        time_passed=master_clock-pre_master_clock
        event=event_list.index(min(event_list))

        if event ==0:#arrival 事件发生
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
                
            #更新三个joblist
            if index_s+1<=len(arrival)-1:
                next_arr_fog=arrival[index_s+1]
            else:
                next_arr_fog=float('inf')
            #将next_arrivl 移动到下一个

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
            #更新event_list


        if event ==1:#dep from fog without cloud 发生
            l_min=[]#存入jobfog的剩余时间，便于找最小
            for ele in job_list_fog:
                ele[1]=ele[1]-time_passed/len(job_list_fog)
                l_min.append(ele[1])
            if job_list_network!=[]:
                for ele in job_list_network:
                    ele[1]=ele[1]-time_passed
            if job_list_cloud!=[]:
                for ele in job_list_cloud:
                    ele[1]=ele[1]-time_passed/len(job_list_cloud)
            #以上更新了三个job_listt

            #找最小的时间
            for el in job_list_fog:
                if el[1]==min(l_min):#这个变一下啊
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
            totalNumberOfJobsCompleted=totalNumberOfJobsCompleted+1 #计数完成的任务
            

            
        if event==2:# dep from fog with cloud 这里有些问题
            l_min=[]#存入jobfog的剩余时间，便于找最小
            for ele in job_list_fog:
                ele[1]=ele[1]-time_passed/len(job_list_fog)
                l_min.append(ele[1])
            if job_list_network!=[]:
                for ele in job_list_network:
                    ele[1]=ele[1]-time_passed
            if job_list_cloud!=[]:
                for ele in job_list_cloud:
                    ele[1]=ele[1]-time_passed/len(job_list_cloud)
            #以上更新了三个job_listt
            for el in job_list_fog:
                if el[1]==min(l_min):#这个变一下啊
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
            l_min=[]#存入jobfog的剩余时间，便于找最小
            for ele in job_list_network:
                ele[1]=ele[1]-time_passed
                l_min.append(ele[1])
            #以上更新了三个job list
            for el in job_list_network:
                if el[1]==min(l_min):#这个变一下啊
                    network_departure.append([el[0],master_clock])
                    n_j=arrival.index(el[0])
                    job_list_cloud.append([el[0],service_at_cloud[n_j]])
                    job_list_network.remove(el)
            #修改
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
            c_min=[]#存入jobcloud的剩余时间，便于找最小
            for ele in job_list_cloud:
                ele[1]=ele[1]-time_passed/len(job_list_cloud)
                c_min.append(ele[1])
            #以上更新了三个joblist
            for el in job_list_cloud:
                if el[1]==min(c_min):#这个变一下啊
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

    #根据arrival_time 排序
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
   


