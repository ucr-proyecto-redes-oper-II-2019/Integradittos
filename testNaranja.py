from orangeNode import OrangeNode
print("Escriba su numero de IP")
ip = input()
print("Escriba su numero de puerto.")
puerto = int(input())
print("Escriba la prioridad")
id = int(input())
orange = OrangeNode(id, ip, puerto)
orange.start("grafoPrueba.csv", "grafoNaranjas.txt")
