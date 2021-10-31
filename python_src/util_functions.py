import random

list_rooms = ["workRoom", "meetRoom", "breakRoom", "kitchen", "bathroom"]


def generate_rooms(num_rooms=None):
    '''Generates rooms to test room placement.'''
    if not num_rooms:
        num_rooms = 10

    room_list = []
    for i in range(num_rooms):
        room_list.append({
            "id": i + 1,
            "width": random.randint(2, 6),
            "height": random.randint(2, 6),
            "type": random.choice(list_rooms)
        })

    return room_list


def get_floor_dims():
    '''Get height/width for the floor.'''
    return random.randint(7, 12), random.randint(7, 12)


def print_floor(floor_map):
    print('\n'.join([''.join(['{:4}'.format(int(item)) for item in row])
                     for row in floor_map]))
