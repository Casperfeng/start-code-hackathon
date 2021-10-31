import numpy as np
import json
import copy
from util_functions import generate_rooms, get_floor_dims, print_floor


class RoomPlacer:

    def run(self, filepath=None):
        '''Starts the floor placement.'''
        # Read input problem
        if filepath:
            floor_plan, rooms = self.parse_json(filepath)
            self.fp_width, self.fp_height = self.find_floor_dimensions(
                floor_plan)
        else:
            self.fp_width, self.fp_height = 20, 40  # get_floor_dims()
            rooms = generate_rooms(20)

        # Floor width/height

        # Create 2D numpy array 'map' where values are room ids
        floor_map = np.zeros((self.fp_height, self.fp_width))
        # print_floor(floor_map)

        # Sort rooms by type and move it to dict
        room_type_dict = self.create_room_type_dict(rooms)

        # Add work rooms first
        # if room_type_dict.get('workRoom'):
        #     floor_map = self.add_rooms(
        #         floor_map, room_type_dict['workRoom'])

        # Add the remaining room types in an arbitrary order
        # TODO: Use a seach tree to find the order that gives the minimum avg. room square height.
        count = 0
        for type in room_type_dict:
            if count < 4:
                floor_map = self.add_rooms(
                    floor_map, room_type_dict[type])
            count += 1

        # TODO: Update the top-left anchor values of rooms and return rooms instead of floor map
        #       self.fill_rooms_values(floor_map)

        return floor_map

    def parse_json(self, filepath):
        """
        Function for converting the input JSON, to a dictionary and an array of coordinates
        :param filepath:
            string containing the location of the input-JSON
        :return:
            A tuple, where the first value is an array containing the coordinates of the floor plan, and
            the other a dictionary containing all the rooms to be fitted in the floor
        """

        # Read the JSON file and dump the contents
        with open(filepath, 'r') as input_JSON:
            data = json.load(input_JSON)
            floor_plan = data['planBoundary']
            room_dict = data['rooms']

        return floor_plan, room_dict

    def find_floor_dimensions(self, floor_plan):
        '''Finds the floor plan width and height.'''
        min_x_coord = min(floor_plan, key=lambda coord: coord['x'])['x']
        max_x_coord = max(floor_plan, key=lambda coord: coord['x'])['x']
        fp_width = min_x_coord + max_x_coord

        min_y_coord = min(floor_plan, key=lambda coord: coord['y'])['y']
        max_y_coord = max(floor_plan, key=lambda coord: coord['y'])['y']
        fp_height = min_y_coord + max_y_coord

        return fp_width, fp_height

    def create_room_type_dict(self, rooms):
        '''Creates a dictionary where rooms of the same type are placed together'''
        type_dict = {}

        for room in rooms:
            if not type_dict.get(room['type']):
                type_dict[room['type']] = [room]
            else:
                type_dict[room['type']] += [room]

        # Sort lists by decreasing width size.
        for type in type_dict:
            type_dict[type] = sorted(
                type_dict[type], key=lambda room: room['width'], reverse=True)

        # TODO: Split lists with length >4 to get smaller clusters.

        return type_dict

    def add_rooms(self, floor_map, rooms):
        '''Places rooms of the same type optimally'''
        # TODO: Currently adds rooms in an arbitrary order.
        #       Use a seach tree to find the order that gives the minimum avg. room square height.

        for room in rooms:
            free_spots = self.find_available_placement(floor_map, room)

            if not free_spots:
                self.add_path(floor_map, [room['id'] for room in rooms])

            min_avg_height = float('inf')
            cur_best_map = copy.deepcopy(floor_map)
            cur_best_spot = (-1, -1)  # (x, y)
            spot_found = False

            for spot in free_spots:
                temp_floor_map = copy.deepcopy(floor_map)

                room['anchorTopLeftX'] = spot[0]
                room['anchorTopLeftY'] = spot[1]

                self.place_room(temp_floor_map, room)

                current_avg_height = self.average_height(temp_floor_map)

                # With equal min_avg_height select the leftmost one
                if (current_avg_height < min_avg_height) \
                        or (current_avg_height == min_avg_height and spot[0] < cur_best_spot[0]):
                    min_avg_height = current_avg_height
                    cur_best_map = temp_floor_map
                    cur_best_spot = spot

                    spot_found = True

            floor_map = cur_best_map

            self.add_path(floor_map, [room['id'] for room in rooms])

            if not spot_found:
                print('Room not placed:')
                print(room)

        return floor_map

    def find_available_placement(self, floor_map, room):
        '''Finds the top-left anchor points where the room can be placed. A list of anchor point tuples is returned.'''
        # TODO: Ensure a placement does not block access to a path for another room
        # TODO: Ensure workspace face a wall. Placing them first is not enough

        anchor_points = []

        for y in reversed(range(self.fp_height)):
            count = 0  # Count consecutive path squares encountered horizontally

            for x in range(self.fp_width):
                # Path encounter. See if a room can be placed below.
                if (y > 0) and (-1 in floor_map[y-1]) and (floor_map[y, x] == 0):
                    count += 1

                    if count == room['width']:
                        anchor_points.append((x - (room['width'] - 1), y))

                # Top edge encounter. See if a room can be placed here.
                elif y == 0 and floor_map[y, x] == 0:
                    count += 1

                    if count >= room['width']:
                        anchor_points.append((x - (room['width'] - 1), y))

                else:
                    count = 0

        return anchor_points

    def add_path(self, floor_map, id_list):
        '''Simple initial path implementation. Adds path (-1) on top of and to the left of a group of rooms of the same type.'''
        for x in range(1, self.fp_width-1):
            for y in range(1, self.fp_height-1):
                if floor_map[y, x] == 0:
                    surrounding_values = [
                        floor_map[y, x-1],
                        floor_map[y-1, x-1],
                        floor_map[y-1, x],
                        floor_map[y-1, x+1],
                        floor_map[y, x+1]
                    ]

                    for val in surrounding_values:
                        if val in id_list:
                            floor_map[y, x] = -1
                            break

        # TODO: connect paths

    def place_room(self, floor_map, room):
        '''Adds the room to the floor map.'''

        for x in range(room['width']):
            for y in range(room['height']):

                floor_map[room['anchorTopLeftY'] + y,
                          room['anchorTopLeftX'] + x] = room['id']

    def average_height(self, floor_map):
        '''Heuristic to compare search solutions. Lower is better.'''
        count = 0
        sum_height = 0

        for x in range(self.fp_width):
            for y in range(self.fp_height):
                if floor_map[y, x] > 0:
                    count += 1
                    sum_height += y

        if count > 0:
            return sum_height / count

        return 0


if __name__ == '__main__':
    result = RoomPlacer().run()  # './TASK_examples/basic_example_input.json'

    print('Result:\n')
    print_floor(result)
    print('0: unused floor')
    print('-1: floor allocated for path between rooms')
    print('>0: room id')
