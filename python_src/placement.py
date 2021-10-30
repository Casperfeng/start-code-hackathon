import numpy as np
import json
import pprint
import copy


class RoomPlacer:

    def place(self, filepath):
        # Read input problem
        floor_plan, rooms = self.parse_json(filepath)

        # Floor width/height
        self.fp_width, self.fp_height = self.find_floor_dimensions()

        # Create 2D numpy array 'map' where values are room ids
        floor_map = np.zeros((self.fp_height, self.fp_width))

        # Sort rooms by type and move it to dict
        room_type_dict = self.create_room_type_dict(rooms)

        # Add work rooms first
        floor_map = self.add_rooms(
            floor_map, room_type_dict['workRoom'], float('inf'))

        # Add the remaining room types in an arbitrary order
        for type in room_type_dict:
            floor_map = self.add_rooms(
                floor_map, room_type_dict[type], float('inf'))

        # Update the top-left anchor values of rooms
        self.fill_rooms_values(floor_map,)

        return rooms

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

        return type_dict

    def add_rooms(self, floor_map, rooms):
        '''Recursive method that places room of the same type optimally'''

        for room in rooms:
            free_spots = self.find_available_placement(floor_map, room)

            min_avg_height = float('inf')
            best_floor_map = copy.deepcopy(floor_map)

            for spot in free_spots:
                temp_floor_map = copy.deepcopy(floor_map)

                current_avg_height = self.average_height(
                    temp_floor_map, rooms['type'])

                if current_avg_height < min_avg_height:

        return None

        # if added_room['type'] == 'workRoom':
        #     squares = self.find_work_room_squares(cur_floor_map, added_room)
        # else:
        #     squares = self.find_room_squares(cur_floor_map, added_room)

        # # Add more checks below that reduces squares

    # NOT YET IN USE

    def place_room(self, floor_map, room):
        '''Adds the room to the floor map.'''
        for x in range(room['width']):
            for y in range(room['height']):

                floor_map[room['anchorTopLeftY'] + y,
                          room['anchorTopLeftX'] + x] = room['id']

    def find_placement_squares(self, room):
        '''Finds top-left squares where the given room can be placed'''
        squares = []  # list of tuples

        # TODO

        return squares

    def average_height(self, floor_map, type_int):
        '''Heuristic to compare search solutions'''
        count = 0
        sum_height = 0

        for x in range(room['width']):
            for y in range(room['height']):
                if floor_map[y, x] == type_int:
                    count += 1
                    sum_height += y

        return sum_height / count

    def fill_rooms_values(floor_map, rooms):
        rooms_found = []


if __name__ == '__main__':
    result = RoomPlacer().place('./TASK_examples/basic_example_input.json')
    print('Results of brute-force:\n')
    pprint.pprint(result)

    # def find_work_room_squares(self, floor_map, room):
    #     '''Finds possible top-left work_room squares.'''
    #     for x_val in range(floor_map.shape[1] - room['width']):
    #         if floor_map[0, x_val] == 0:
    #             pass
    #         if floor_map[floor_map.shape[0] - room['height'], x_val] == 0:

    #     for x in range(floor_map.shape[1] - room['width']):
    #         for y in range(floor_map.shape[0] - room['height']):
    #             pass

    # def uses_unassigned_squares(floor_map, room):
    #     for x in range(room['width']):
    #         for y in range(room['height']):
    #             if floor_map[room['anchorTopLeftX'] + x, room['anchorTopLeftY'] +y] != 0:
    #                 return False

    #     return True
