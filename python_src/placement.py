import numpy as np
import json
import pprint
import copy


class RoomPlacer:

    def place(self, filepath=None):
        # Read input problem
        if filepath:
            floor_plan, rooms = self.parse_json(filepath)
        else:
            self.generate(10)

        # Floor width/height
        self.fp_width, self.fp_height = self.find_floor_dimensions(floor_plan)

        # Create 2D numpy array 'map' where values are room ids
        floor_map = np.zeros((self.fp_height, self.fp_width))

        # Sort rooms by type and move it to dict
        room_type_dict = self.create_room_type_dict(rooms)

        # Add work rooms first
        floor_map = self.add_rooms(
            floor_map, room_type_dict['workRoom'], float('inf'))

        # Add the remaining room types in an arbitrary order
        # TODO: Use a seach tree to find the order that gives the minimum avg. room square height.
        for type in room_type_dict:
            floor_map = self.add_rooms(
                floor_map, room_type_dict[type], float('inf'))

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

        # To get a feeling for what our data looks like, let's print the contents
        # print(f'Coordinate array:')
        # pprint.pprint(floor_plan)
        # print('\n')
        # print(f'Room dictionary:\n')
        # pprint.pprint(room_dict)
        # print('\n')
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

    def create_room_type_dict(rooms):
        '''Creates a dictionary where rooms of the same type are placed together'''
        type_dict = {}

        for room in rooms:
            if not type_dict.get(room['type']):
                type_dict[room['type']] = [room]
            else:
                type_dict[room['type']] += [room]

        # TODO: Sort lists by decreasing size.
        # TODO: Split lists with length >4 to get smaller clusters.

        return type_dict

    def add_rooms(self, floor_map, rooms):
        '''Places rooms of the same type optimally'''

        # TODO: Currently adds rooms in an arbitrary order.
        #       Use a seach tree to find the order that gives the minimum avg. room square height.

        for room in rooms:
            free_spots = self.find_available_placement(floor_map, room)

            min_avg_height = float('inf')
            cur_best_map = copy.deepcopy(floor_map)

            for spot in free_spots:
                temp_floor_map = copy.deepcopy(floor_map)

                room['anchorTopLeftX'] = spot[0]
                room['anchorTopLeftY'] = spot[1]

                self.place_room(temp_floor_map, room)

                current_avg_height = self.average_height(
                    temp_floor_map, rooms[0]['type'])

                if current_avg_height < min_avg_height:
                    cur_best_map = temp_floor_map

            floor_map = cur_best_map

        self.add_path(floor_map, [room['id'] for room in rooms])

    def find_available_placement(floor_map, room):
        '''Finds the top-left anchor points where the room can be placed. A list of anchor points is returned.'''
        anchor_points = []

        for y in reversed(range(room['height'])):
            count = 0  # Count consequtive path squares encountered horizontally
            for x in range(room['width']):
                if floor_map[y, x] == -1:
                    count += 1

                    if count == room['width']:
                        anchor_points += (x - (room['width'] - 1),
                                          y - (room['height'] - 1))
                else:
                    count = 0

        return anchor_points

    def add_path(self, floor_map, id_list):
        '''Simple initial path implementation. Adds path (-1) on top of a group of rooms of the same type.'''
        for y in reversed(range(self.fp_height)):
            for x in range(self.fp_width):
                if floor_map[y, x] in id_list:  # Check id_list number format
                    floor_map[y-1, x] = -1
                    break

        # TODO: connect paths

    def place_room(self, floor_map, room):
        '''Adds the room to the floor map.'''
        for x in range(room['width']):
            for y in range(room['height']):

                floor_map[room['anchorTopLeftY'] + y,
                          room['anchorTopLeftX'] + x] = room['id']

    def average_height(self, floor_map, type_int):
        '''Heuristic to compare search solutions'''
        count = 0
        sum_height = 0

        for x in range(self.fp_width):
            for y in range(self.fp_height):
                if floor_map[y, x] == type_int:
                    count += 1
                    sum_height += y

        return sum_height / count


if __name__ == '__main__':
    result = RoomPlacer().place('./TASK_examples/basic_example_input.json')

    print('Results of brute-force:\n')
    print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                     for row in result]))
