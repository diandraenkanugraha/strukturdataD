import streamlit as st
import time

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

node1 = Node("Lampu Merah : 40 detik")
node2 = Node("Lampu Hijau : 60 detik")
node3 = Node("Lampu Kuning : 5 detik")

node1.next = node2
node2.next = node3
node3.next = node1

curretNode = node1
startNode = node1
print(curretNode.data, end=" → ")
curretNode = curretNode.next

while curretNode != startNode:
    print(curretNode.data, end=" → ")
    curretNode = curretNode.next

print("...")