one_deep_dictionary = {'start here': 1, 'k1': [1,2,3,{'k2':[1,2,{'k3':['keep going',{'further':[1,2,3,4,[{'k4':'Python'}]]}]}]}]}

print(type(one_deep_dictionary))

print(one_deep_dictionary['k1'][3]['k2'][2]['k3'][1]['further'][4][0]['k4'])

A = True; B = False

C = A or B

D  = A and B

D_not = not D 

XOR = C and D_not

print(XOR)

XOR1 = (A or B) and not (A and B)

print(XOR1)

x = 10

n = int(input())

if n > x: 
    print(f"{n} is greater than {x}")

# False and True being typecasted
print(99 > 5)
print(0 == False)
print(1 == True)
print(6.2 < 7)
print(9 >= 9)
print(False < True)