import sys
from orangeNode import OrangeNode

""""print("Escriba su numero de IP")
ip = input()
print("Escriba su numero de puerto.")
puerto = int(input())
print("Escriba la prioridad")
id = int(input())"""
ip = sys.argv[1]
puerto = int(sys.argv[2])
id = int(sys.argv[3])
orange = OrangeNode(id, ip, puerto)
orange.start("grafoPrueba.csv", "grafoNaranjas.txt")
