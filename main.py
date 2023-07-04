import boto3
import time



# This Function Creates N instances of specified Type
def create_instance(ami,inType,n):
    try :
        print("Creating EC2 instances of type "+inType)
        resource=boto3.client("ec2")
        resource.run_instances(
            ImageId=ami,
            MinCount=1,
            MaxCount=n,
            InstanceType=inType,
            KeyName="acsp",

        )
    except Exception as e:
        print(e)
# This Function Creates 1 Instance of Specified Type
def create_one_instance(ami,inType,n):
    try :
        print("Creating One EC2 instance of type "+inType)
        resource=boto3.client("ec2")
        resource.run_instances(
            ImageId=ami,
            MinCount=1,
            MaxCount=1,
            InstanceType=inType,
            KeyName="acsp",

        )
        n=n+1
        return n
    except Exception as e:
        print(e)

# This Function is used to provide information about all the instances
def describe_instance():
    try:
        print("Describing Instances")
        resource=boto3.client("ec2")
        print(resource.describe_instances())

    except Exception as e:
        print(e)

# This function returns a list of all instance ID
def get_instanceId():
    n_instances = []

    ec2client = boto3.client('ec2', region_name='us-east-1')
    response = ec2client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            x = (instance["InstanceId"])

            n_instances.append(x)

    return n_instances

# This Function returns a list of the states of all the instances
def get_states():
    states = []

    ec2client = boto3.client('ec2', region_name='us-east-1')
    response = ec2client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            x = (instance["State"]["Name"])

            states.append(x)

    return states

# This Function is used to terminate one Instance of specified ID
def terminate_instance(id):
    try :
        print("Termianting instance with id "+id)
        resource=boto3.client("ec2")
        resource.terminate_instances(InstanceIds=[id])

    except Exception as e:
        print(e)

# This Function returns a list of all the running instances
def running_instance():
    running_instances = []

    ec2client = boto3.client('ec2', region_name='us-east-1')
    response = ec2client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if instance['State']['Name'] == 'running' or instance['State']['Name'] == 'pending':
                x = (instance["InstanceId"])

                running_instances.append(x)


    return running_instances

# This function returns a list of all the running instance of specified Type
def running_instanceType(inType):
    running_instances = []

    ec2client = boto3.client('ec2', region_name='us-east-1')
    response = ec2client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if (instance['State']['Name'] == 'running' or instance['State']['Name'] == 'pending') and instance['InstanceType']==inType:
                x = (instance["InstanceId"])
                # print(x)
                running_instances.append(x)


    return running_instances


# describe_instance()
# Driver Program
print("Choose the Operating System of your Compute Resource")
print(" 1. Amazon Linux")
print(" 2. MacOS")
print(" 3. Ubuntu")
print(" 4. Windows")
ami=""
choice=input("Enter Choice ")
choice=int(choice)
if choice==1:
    ami="ami-0b0dcb5067f052a63"
elif choice==2:
    ami="ami-0fe12b543f1354e5c"
elif choice==3:
    ami="ami-08c40ec9ead489470"
elif choice==4:
    ami="ami-064d05b4fe8515623"
else :
    print("Please enter a valid choice ")
    quit()

n1=input("How many  t1.micro ( 1vCPU 0.612GB RAM ) instance do you require ")
n1=int(n1)
m1=n1
n2=input("How many  t2.micro ( 1vCPU 1GB RAM ) instance do you require ")
n2=int(n2)
m2=n2
n3=input("How many  t2.small ( 1vCPU 2GB RAM ) instance do you require ")
n3=int(n3)
m3=n3
n4=input("How many  t2.medium ( 2vCPU 4GB RAM ) instance do you require ")
n4=int(n4)
m4=n4
min1=input("Enter the number of mins for which you require Compute Resource ")
min1=int(min1)
type1=""
type2=""
type3=""
type4=""
if n1>0:
    type1="t1.micro"
    create_instance(ami, type1, n1)
    time.sleep(20)
if n2>0:
    type2="t2.micro"
    create_instance(ami,type2,n2)
    time.sleep(20)
if n3>0:
    type3="t2.small"
    create_instance(ami, type3, n1)
    time.sleep(20)
if n4>0:
    type4="t2.medium"
    create_instance(ami,type4,n2)
    time.sleep(20)


t_end = time.time() + 60 * min1
time.sleep(45)
#print("45 seconds have passed")


runningList5=running_instance()
print(runningList5)

terminate_instance(runningList5[0])
terminate_instance(runningList5[3])
time.sleep(15)
#print("15 seconds have passed")

while time.time() < t_end:
    runningList=running_instance()
    runningList1 = running_instanceType(type1)
    runningList2 = running_instanceType(type2)
    runningList3 = running_instanceType(type3)
    runningList4 = running_instanceType(type4)
    print(runningList)
    running_size1=len(runningList1)

    running_size2 = len(runningList2)
    running_size3 = len(runningList3)

    running_size4 = len(runningList4)

    dif1=n1-running_size1
    print("Difference between required t1.micro Instance with running Instance is: "+str(dif1))
    if(dif1):
        for i in range (dif1):
            if dif1!=0:
                m1=create_one_instance(ami,type1,m1)
                time.sleep(30)
        dif1=0
    dif2 = n2 - running_size2
    print("Difference between required t2.micro Instance with running Instance is: " + str(dif2))
    if (dif2):
        for i in range(dif2):
            if dif2 != 0:
                m2 = create_one_instance(ami, type2, m2)
                time.sleep(30)
        dif2 = 0
    dif3 = n3 - running_size3
    print("Difference between required t2.small Instance with running Instance is: " + str(dif3))
    if (dif3):
        for i in range(dif3):
            if dif3 != 0:
                m3 = create_one_instance(ami, type3, m3)
                time.sleep(30)
        dif3 = 0
    dif4 = n4 - running_size4
    print("Difference between required t2.medium Instance with running Instance is: " + str(dif4))
    if (dif4):
        for i in range(dif4):
            if dif4 != 0:
                m4 = create_one_instance(ami, type4, m4)
                time.sleep(30)
        dif4 = 0

print("Requested Time is over")
for i in running_instance():
    terminate_instance(i)