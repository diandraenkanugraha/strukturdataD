import time

class Node:
    def __init__(self, data, durasi):
        self.data = data
        self.durasi = durasi
        self.next = None

class CircularLinkedList:
    def __init__(self):
        self.head = None

    def tambah_lampu(self, data, durasi):
        new_node = Node(data, durasi)
        if not self.head:
            self.head = new_node
            new_node.next = self.head
        else:
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = new_node
            new_node.next = self.head

    def mulai_simulasi(self):
        if not self.head:
            return
        
        bantu = self.head
        while True:
            print(f"\n>>> Lampu {bantu.data} Menyala <<<")
            for i in range(bantu.durasi, 0, -1):
                print(f"Sisa waktu: {i} detik", end="\r")
                time.sleep(1)
            
            bantu = bantu.next 

lampu = CircularLinkedList()
lampu.tambah_lampu("MERAH", 40)
lampu.tambah_lampu("HIJAU", 20)
lampu.tambah_lampu("KUNING", 5)

lampu.mulai_simulasi()
lampu.tambah_lampu("MERAH", 40)
lampu.tambah_lampu("HIJAU", 20)
lampu.tambah_lampu("KUNING", 5)

lampu.mulai_simulasi()