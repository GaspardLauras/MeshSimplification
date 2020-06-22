from SimplificationFonctions import *
import numpy as np

# E = (0.5,0.5,1.05)
pA = np.array([1,1,1,1])

points = np.array([
	[0,0.1,1,-1.1],
	[0.1,0,1,-1.1],
	[0,1,0,-1],
	[1,0,0,-1],
	[0,-0.1,1,-1],
	[-0.1,0,1,-1]
	])

A = [[[0,0.1,1,-1.1]],[[0.1,0,1,-1.1]],[[0,1,0,-1]],[[1,0,0,-1]]]

E = [[[0,0.1,1,-1.1]],[[0.1,0,1,-1.1]],[[0,-0.1,1,-1]],[[-0.1,0,1,-1]]]

A = np.array([np.array(u) for u in A])
E = np.array([np.array(u) for u in E])

print('A : \n',A)
print('E : \n',E)

KA = [p.transpose()@p for p in A]
KE = [p.transpose()@p for p in E]

QA = np.zeros((4,4))
for mat in KA:
	QA += mat

print(pA@QA@pA.transpose())

QE = np.zeros((4,4))
for mat in KE:
        QE += mat

Q = QA + QE

error = np.array([[Q[0][0],Q[0][1],Q[0][2],Q[0][3]],
		  [Q[0][1],Q[1][1],Q[1][2],Q[1][3]],
		  [Q[0][2],Q[1][2],Q[2][2],Q[2][3]],
		  [0      ,0      ,0      ,1      ]])

inv = np.linalg.inv(error)
 
vec = np.array([[0],[0],[0],[1]])

res = inv@vec

print(res[:3])

#Ajouter la normalisation

#[[0.98701299]
# [0.98701299]
# [1.03376623]]
