from queue import Queue
from random import randint
from threading import Thread
from time import sleep


class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None

class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name


    def run(self):
        sleep(randint(3,10))

class Cafe:
    def __init__(self, *args):
        self.queue = Queue()
        self.tables = [i for i in args]

    def guest_arrival(self,*guests):
        for cur_guest in guests:
            for cur_table in self.tables:
                if cur_table.guest is None:
                    cur_table.guest = cur_guest
                    cur_guest.start()
                    print(f"<{cur_guest.name}> сел(-а) за стол номер <{cur_table.number}>")
                    break
            if not cur_guest.is_alive():
                self.queue.put(cur_guest)
                print(f"<{cur_guest.name}> в очереди")


    def discuss_guests(self):
        while not self.queue.empty() or any(x.guest is not None for x in self.tables):
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    print(f"<{table.guest.name}> покушал(-а) и ушёл(ушла)")
                    print(f"Стол номер <{table.number}> свободен")
                    table.guest = None
                    if not self.queue.empty():
                        newGuest = self.queue.get()
                        table.guest = newGuest
                        print(f"<{newGuest.name}> вышел(-ла) из очереди и сел(-а) за стол номер <{table.number}>")
                        newGuest.start()



tables = [Table(number) for number in range(1, 6)]
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
guests = [Guest(name) for name in guests_names]
cafe = Cafe(*tables)

cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()