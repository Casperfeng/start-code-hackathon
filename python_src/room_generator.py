import random

list_rooms = ["workRoom", "meetRoom", "breakRoom", "kitchen", "bathroom"]

# Create a list of dictionaries


def create_list():
    numOfRooms = random.randint(1, 10)
    i = 0
    list_dict = []
    for i in range(numOfRooms):
        roomDict = {
            "id": i + 1,
            "width": random.randint(1, 6),
            "height": random.randint(1, 4),
            "type": random.choice(list_rooms)
        }
        list_dict.append(roomDict)

    return list_dict
