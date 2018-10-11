import numpy as np
import csv
import math
import statistics 
import matplotlib.pyplot as plt
import sys
from random import randint
import copy

def sigmoid(z):
	return 1/(1+np.exp(-z))

# input_size=sys.argv[1]
# batch_size=sys.argv[2]
# hidden_list = map(int, sys.argv[3].strip('[]').split(','))

input_layer_size=2
batch_size=100
hidden_list=[5]

combined_list=[input_layer_size]+hidden_list+[1]

weights_neuralnet=[]
for i in range(0,len(combined_list)):
	if not i==len(combined_list)-1:
		#form connections
		uplist_numnodes=combined_list[i]
		downlist_numnodes=combined_list[i+1]
		helplist=[]
		for j in range(0,uplist_numnodes):
			helplist2=[]
			for k in range(0,downlist_numnodes):
				helplist2.append(float(randint(-5, 5))/10) #k
			helplist.append(helplist2)
		weights_neuralnet.append(helplist)		

outputs_neuralnet=[]

for l in range(0,len(combined_list)):
	numnodes_level=combined_list[l]
	helplist=[]
	for j in range(0,numnodes_level):
		helplist.append(0)
	outputs_neuralnet.append(helplist)	


trainX = []
with open('toy_data/toy_trainX.csv',newline='') as csvfileX:
	reader = csv.reader(csvfileX)
	for row in reader:
		row=[float(x) for x in row]
		trainX.append(row)

trainY = []
with open('toy_data/toy_trainY.csv',newline='') as csvfileX:
	reader = csv.reader(csvfileX)
	for row in reader:
		row=[int(x) for x in row]
		trainY.append(row)	


testX = []
with open('toy_data/toy_testX.csv',newline='') as csvfileX:
	reader = csv.reader(csvfileX)
	for row in reader:
		row=[float(x) for x in row]
		testX.append(row)

testY = []
with open('toy_data/toy_testY.csv',newline='') as csvfileX:
	reader = csv.reader(csvfileX)
	for row in reader:
		row=[int(x) for x in row]
		testY.append(row)			

def calculate_output(inputs,outputs_neuralnet,weights_neuralnet):
	final_output=[]
	for i in range(0,len(outputs_neuralnet)):
		helplist=[]
		for j in range(0,len(outputs_neuralnet[i])):
			helplist.append(0)
		final_output.append(helplist)	
	final_output[0]=inputs
	level=0
	maxlevel=len(outputs_neuralnet)
	for i in range(1,maxlevel):
		prev_layer=final_output[i-1]
		current_layer=final_output[i]
		weights = weights_neuralnet[i-1]
		for j in range(0,len(current_layer)):
			current_node=current_layer[j]
			linkweights = [x[j] for x in weights]
			z=sum([x*y for x,y in zip(linkweights,prev_layer)])
			current_layer[j]=sigmoid(z)
	return final_output		

def backwardpropagation(outputs_neuralnet,weights_neuralnet,tk):
	#output layer
	output_layer=outputs_neuralnet[-1]
	error_list=[]
	for i in range(0,len(outputs_neuralnet)):
		helplist=[]
		for j in range(0,len(outputs_neuralnet[i])):
			helplist.append(0)
		error_list.append(helplist)	
	error_outputlayer=error_list[-1]
	for i in range(0,len(output_layer)):
		error_outputlayer[i]=output_layer[i]*(1-output_layer[i])*(tk-output_layer[i])

	#hidden layers
	for level in range(len(outputs_neuralnet)-2,-1,-1):
		for i in range(0,len(outputs_neuralnet[level])):
			sumofnextlayer=sum([x*y for x,y in zip(error_list[level+1],weights_neuralnet[level][i])])
			error_list[level][i]=outputs_neuralnet[level][i]*(1-outputs_neuralnet[level][i])*sumofnextlayer
	return error_list	

def updatesnetworkweight(outputs_neuralnet,weights_neuralnet,error_list,n):
	example_updates=[]
	for i in range(0,len(weights_neuralnet)):
		helplist2=[]
		for j in range(0,len(weights_neuralnet[i])):
			helplist=[]
			for k in range(0,len(weights_neuralnet[i][j])):
				helplist.append(0)
			helplist2.append(helplist)	
		example_updates.append(helplist2)	

	for level in range(0,len(weights_neuralnet)):
		for i in range(0,len(weights_neuralnet[level])):
			for j in range(0,len(weights_neuralnet[level][i])):
				example_updates[level][i][j]=n*outputs_neuralnet[level][i]*error_list[level+1][j]
	return example_updates		

def sgdalgorithm(trainX,trainY,outputs_neuralnet,weights_neuralnet,n,r):
	i=0
	

	for t in range(0,100):
		for b in range(1,int(len(trainY)/r)+1):
			trainXsamples=trainX[(b-1)*r:(b*r)]
			trainYsamples=trainY[(b-1)*r:(b*r)]
			weights=[]
			# print(b)
			for l,m in zip(trainXsamples,trainYsamples):
				outputs_neuralnet=calculate_output(l,outputs_neuralnet,weights_neuralnet)
				errorlist=backwardpropagation(outputs_neuralnet,weights_neuralnet,m[0])
				example_updates=updatesnetworkweight(outputs_neuralnet,weights_neuralnet,errorlist,n)
				weights.append(example_updates)
			for i in range(0,len(weights_neuralnet)):
				for j in range(0,len(weights_neuralnet[i])):
					for k in range(0,len(weights_neuralnet[i][j])):
						for m in range(0,len(weights)):
							weights_neuralnet[i][j][k]+=weights[m][i][j][k]	
							# print(weights_neuralnet[i][j][k])
			# print(weights_neuralnet)				
	return weights_neuralnet		

# weights_neuralnet=(sgdalgorithm(trainX,trainY,outputs_neuralnet,weights_neuralnet,0.1,1))
inputs=[2.514,-1.74]
# print(weights_neuralnet)
# calculated_output=calculate_output(inputs,outputs_neuralnet,weights_neuralnet)
# print(calculated_output)
# error_list=backwardpropagation(calculated_output,weights_neuralnet,0)
# print('error')
# print(error_list)


# example_updates=updatesnetworkweight(outputs_neuralnet,weights_neuralnet,error_list,0.5)
# print('example updates:')
# print(example_updates)
print(weights_neuralnet)
weights=sgdalgorithm([[2.514,-1.74]],[[0]],outputs_neuralnet,weights_neuralnet,0.5,1)
result = calculate_output(inputs,outputs_neuralnet,weights)
print(result[-1][0])
# print(weights)

# print(weights_neuralnet)
# inputs=[1,2]
# calculated_output=calculate_output(inputs,outputs_neuralnet,weights_neuralnet)
# print('forward:',calculated_output)
# backward=backwardpropagation(calculated_output,weights_neuralnet,1)
# print(backward)
# # print(weights_neuralnet)

# print('final')

# updated=updatesnetworkweight(calculated_output,weights_neuralnet,backward,1)
# print(updated)


