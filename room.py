"""
Room: 1
desc: one bed
state: Vacant

Room 2
one bed
Vacant
"""
rooms: list
with open("room.txt") as f:
    rooms = f.readlines()

print(rooms)
print(type(rooms))
"['Room: 1\n', 'desc: one bed\n', 'state: Vacant\n', '\n', 'Room 2\n', 'one bed\n', 'Vacant\n']"

id = "1"
for index, room in enumerate(rooms):
    if room.startswith("Room"):
        if room[-2] == id:
            start = index + 1
            for y in range(start, len(rooms)):
                print(y)
                if rooms[y].startswith("state"):
                    print("State:", rooms[y][5::])
                    rooms[y] = "state: Occupied"
                    break

print(rooms)
