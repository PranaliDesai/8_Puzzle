import numpy as np
import itertools
from sys import argv
script, filename1,filename2,filename3 = argv


#InputNode-----------------------------------------------------------------------
print("Enter the First Row with space between each number- " , )
m = [int(u) for u in input().split()]			# To input first row
print("Enter the Second Row with space between each number- " , )
n = [int(u) for u in input().split()]			# To input second row
print("Enter the Third Row with space between each number- " , )
o = [int(u) for u in input().split()]			# To input third row
initial_state = np.vstack((m,n,o))

#FinalNode------------------------------------------------------------------------
F1 = np.array([[1,2,3],[4,5,6],[7,8,0]])		# Final state 

#Function_to_generate_nodecode-----------------------------------------------------
def nodecode(n):
	chain = list(itertools.chain(*n.T))
	code = ' '.join(map(str, chain))
	return code
	
#----------------------------------------------------------------------------------
G=nodecode(initial_state) 				# node code for initial state	
final_node=nodecode(F1)					# node code for final state 

#Initializations-------------------------------------------------------------------
parentnode=[]						#List containing index of parent nodes
childnode=[]						#List containing index of child nodes
backtracenode = []
child = []
All_nodecodes=[]					# List containing all node codes 
All_nodes = []						# List containing all node 
x=0
y=0
flag=0
All_nodes.append(np.array(initial_state).tolist()) 	# Appending initial state
All_nodecodes.append(G)					# Appending initial state as node code 

#Function Definations--------------------------------------------------------------

#Function to find number in a matrix------------------------------------------------
def findnum(A,num):
        for i,j in enumerate(A):
            for k,l in enumerate(j):
                if l==num:
                    x=i
                    y=k
        return x,y					# position of row and column of num 

#Function to move zero to 4 different positions-------------------------------------
def move_zero(x,y):
	move_down(x,y)
	move_right(x,y)
	move_up(x,y)
	move_left(x,y)

#Function to push zero down----------------------------------------------------------
def move_down(x,y): 
	a, b = x, y
	x = x+1
	generate_matrix(x, y, a, b)  			# sending the new index for swapping

#Function to push zero up-------------------------------------------------------------
def move_up(x,y):
	a, b = x, y
	x = x-1
	generate_matrix(x, y, a, b)			# sending the new index for swapping

#Function to push zero left-----------------------------------------------------------
def move_left(x,y): 	
	a, b = x, y
	y = y - 1
	generate_matrix(x, y, a, b)			# sending the new index for swapping


#Function to push zero right-----------------------------------------------------------
def move_right(x,y): 
	a, b = x, y
	y = y + 1
	generate_matrix(x, y, a, b)			# sending the new index for swapping

#Function to move and gerenate new matrix----------------------------------------------
def generate_matrix(x, y, a, b):
	if x in range(0, 3) and y in range(0,3):
		M=np.array(initial_state)
		M[a,b]=M[x,y] 				# Swapping 
		M[x,y]=0				# Swapping
		M1=nodecode(M)	
		add_node(np.array(M),M1)

#Function to append new generated matrix-------------------------------------------------
def add_node(L,S):
	while True:
		count=0

		if S not in All_nodecodes:
			All_nodecodes.append(S)
			All_nodes.append(np.array(L).tolist())
			child.append(S)

		else:
			break

#Tracing back the nodes--------------------------------------------------------------------
def path_node():
        NodeInfo=list(zip(parentnode,childnode))	# Generating parent and child node info(index) 
        NodeInfo1=list(zip(childnode,parentnode))	# Generating parent and child node info(index)
        final_pos=final_ans_pos-1			# Getting index of the final_state from all our nodes
        final0=NodeInfo[final_pos][0]			
        final1=NodeInfo[final_pos][1]
        m=final1	
        backtracenode.append(m)				
        m=final0
        backtracenode.append(m)				
        for q in range(0,len(NodeInfo)):   		#algorithm to trace back the nodes using the nodeinfo
            if NodeInfo[final_pos-1-q][1] == m:
                m=NodeInfo[final_pos-1-q][0]
                backtracenode.append(m)
                if m==0:
                    break
        print("Please check files")
	#Creating text file for nodeinfo[2D]------------------------------------------------
        out_file = open(filename1, 'w')
        for nodeinfo in NodeInfo1:
            out_file.write(str(nodeinfo) + '\n')
        out_file.close()

	#Creating text file for nodepath-----------------------------------------------------
        out_file = open(filename2, 'w')
        for nodepath in backtracenode[::-1]:
            out_file.write(str(All_nodecodes[nodepath]) + '\n')
        out_file.close()

	#Creating text file for nodes--------------------------------------------------------
        out_file = open(filename3, 'w')
        for nodes in All_nodecodes:
            out_file.write(str(nodes) + '\n')
        out_file.close()

#Function to check if node is valid----------------------------------------------------------
def Node_is_Valid(node):
    u=node.ravel()
    u=u.tolist()
    u=[a for a in u if a != 0]
    count=0
    for i in range(0,len(u)):
        y=u[i]
        q=0
        for j in range(i,len(u)):
            if (u[j]<y):
                q=q+1
        count=count+q
    if(count%2==0):
        return ("True")
    else:
        print("Initial State is not solvable")
	#Creating empty file for nodeinfo[2D]--------------------------------------------------
        out_file = open(filename1, 'w')
        out_file.close()

	#Creating empty file for nodepath------------------------------------------------------
        out_file = open(filename2, 'w')
        out_file.close()

	#Creating empty file for nodes---------------------------------------------------------
        out_file = open(filename3, 'w')
        out_file.close()
        exit() 

							
#Starting the main code-----------------------

# checking if initial state is solvable or not		
Node_is_Valid(initial_state) 

#Loop to move and generate new nodes to check for solution-------------------------------------
for k in All_nodes:

    #print(All_nodes.index(k))
    if final_node in child: 				#checking if final value is found
        final_ans_pos=All_nodecodes.index(final_node) 	#getting the index 
        flag=1

    if flag==1:
        break
    else:
        #print(All_nodes.index(k))
        initial_state=k
        x,y = findnum(initial_state,0)  		# position of row and column of 0 
        e = len(All_nodes)				# number of nodes before generating 
        child.clear()					# clearing all the child for that particular node
        move_zero(x,y)					# moving zero to generate nodes 
        f = len(All_nodes)				# number of nodes after new nodes are generated
        z = f-e						# calculating number of child generated 
        for j in range(0,z):            
            parentnode.append(All_nodes.index(k)) 	# Appending the parentnodes
            childnode.append(j-z+f)			# Appending the childnodes
	
#Tracing back the node-------------------------------------------------------------------------
path_node()

