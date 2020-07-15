
# Brian Parsons
# Student ID - 001008912
# C950 - Data Structures & Algorithms II
# Performance Assessment

import distances
import copy
from hashTable import hashtable

# reads csv and populates a graph with addresses and weights
distance_graph = distances.get_graph('WGUPS Distances.csv')
distance_graph.populate_address(hashtable)

# B1 - Pseudocode to show algorithm's process
# While packages remain in the list
#   for each package
#       if at start, go forward
#       find the next package with the shortest shipping address distance
#           remove the used package from the list

# B3 - Big O Notation = O(n^2)

# Greedy algorithm. Chooses smallest length first out of given list


# O(n)
def greedy_path(path, start='4001 South 700 East'):

    # gets the list of distances from the graph made by the graph file
    weight_list = distance_graph.edge_weights
    address_list = copy.copy(path)

    # takes a starting point as input
    # note: starting point should not already be part of path
    greed_path = [start]

    while len(address_list) != 0:

        minimum = [0, start]
        for address in address_list:

            # skips address if the start address and end address are the same
            if address == start:
                continue

            # compares distances for each address from the last entry in greed_path
            # minimum distance is stored with its address
            distance = weight_list[greed_path[-1], address]
            if minimum[0] == 0:
                minimum = [distance, address]
            if distance < minimum[0] and distance != 0:
                minimum = [distance, address]

        # appends the new minimum distance address to greed_path and removes from remaining list
        if minimum[1] not in greed_path:
            greed_path.append(minimum[1])
        address_list.remove(minimum[1])

    # removes the hub from the new path
    # makes future comparisons much easier
    if '4001 South 700 East' in greed_path:
        greed_path.remove('4001 South 700 East')
    return greed_path


# O(n)
def total_distance(path):

    # gives a cumulative total distance of a path based on distance_graph weights
    weight_list = distance_graph.edge_weights
    total = 0
    for i in range(0, len(path) - 1):
        total += weight_list[path[i], path[i+1]]

    # adds the distance from last index in path to hub since all trucks return to hub
    total += weight_list[path[-1], '4001 South 700 East']
    return total


# O(n)
def current_distance(path, address):

    # same as total_distance, but only calculates until a given address
    # will use this to see if a truck has gone far enough to have 'visited' address
    weight_list = distance_graph.edge_weights
    total = 0
    for i in range(0, path.index(address)):
        total += weight_list[path[i], path[i+1]]
    return total


# making trucks into a class will make keeping up with packages, addresses, and time much easier
class Truck:
    def __init__(self):

        self.packages = []
        self.route = []
        self.start_time = 'None'

        # total distance of truck route
        self.length = 0

    # O(n)
    def insert(self, address):

        # inserting addresses instead of just packages so that packages going to same address are loaded together
        # this makes the sorting algorithm more efficient as # addresses will always be <= # packages
        self.route.append(address)
        for package in distance_graph.address_list[address]:
            self.packages.append(package)

    # O(n)
    def remove(self, address):

        # removes address from truck route
        self.route.remove(address)

        # removes all packages associated with removed address
        for item in distance_graph.address_list[address]:
            self.packages.remove(item)

        # recalculates route distance
        self.length = total_distance(self.route)

    # O(1)
    def individual_insert(self, package):

        if package[1] != '':

            # if the package has an address, this will insert the address and package individually
            self.route.append(package[1])
            self.packages.append(package)

            # removes hub address to make greed algorithm work
            self.route.remove('4001 South 700 East')
            self.route = greedy_path(self.route)

            # inserts hub address at the beginning for accurate total_distance calculation
            self.route.insert(0, '4001 South 700 East')
            self.length = total_distance(self.route)

    # O(1)
    def leave_hub(self, time):

        # sets a start time to be compared to for distance calculations
        self.start_time = time

        # edits status of package
        for package in self.packages:
            package[8] = 'En Route'

    # O(n^2)
    def passed_time(self, time):

        if self.start_time != 'None':

            # sees how much time has passed since truck left hub (in minutes)
            delta_time = time - self.start_time

            # trucks go 18 mi/hr == 0.3 mi/min
            distance_traveled = delta_time * 0.3
            for location in self.route:

                # check each location on the route to see if it has been reached
                if distance_traveled > current_distance(self.route, location):
                    for item in distance_graph.address_list[location]:

                        # if location has been reached, goes through all of the items in the truck associated
                        # with that location and 'delivers'
                        if item in self.packages:
                            item[8] = 'Delivered'
                            self.packages.remove(item)
                            print('Package %d Delivered' % item[0])


# initializes the 3 trucks as well as an address list to load packages from
t1 = Truck()
t2 = Truck()
t3 = Truck()
addresses = []


# O(5n^2)
def load_trucks():

    for address in distance_graph.address_list:

        # doesn't check hub address as no packages will go here
        # makes a list of addresses to check for packages with set criteria
        if address != '4001 South 700 East':
            addresses.append(address)

        # puts all packages with the earliest due time into truck1 as it will leave first
        for item in distance_graph.address_list[address]:
            if item[5] == '9:00':
                t1.insert(address)

                # removes address from list to avoid redundancies
                addresses.remove(address)
                break

    # this will be used as an index so the high priority packages aren't moved from their point in queue
    checker1 = t1.route.index(t1.route[-1])

    for address in addresses:
        for item in distance_graph.address_list[address]:

            # loads items with time constraints and special notes second since they have both priority
            # and special parameters
            if item[5] == '10:30' and item[7] != '':

                # since it would be impossible to code for all possible special notes, user is prompted to load
                # these manually based on the special notes
                print("Package %d has special note: %s\nLoad into which truck?\n(1, 2, 3)" % (item[0], item[7]))
                truck = input()
                if truck == '1':
                    t1.insert(address)
                elif truck == '2':
                    t2.insert(address)
                elif truck == '3':
                    t3.insert(address)

                # removes address from list to avoid redundancies
                addresses.remove(address)
                break

    for address in addresses:
        for item in distance_graph.address_list[address]:

            # next the packages with time constraints but no special notes are loaded
            if item[5] == '10:30':

                # the total distance change is compared between truck 1 and 2 using a greedy algorithm
                # the algorithm will run multiple times, making this not exactly efficient
                # however, it gives better results than just adding an item to the end of the list
                delta1 = total_distance(greedy_path(t1.route + [address], t1.route[checker1])) - \
                         total_distance(greedy_path(t1.route, t1.route[checker1]))
                delta2 = total_distance(greedy_path(t2.route + [address])) \
                    - total_distance(greedy_path(t2.route))

                # truck 1 will leave before truck 2, so I gave time restricted packages a slight bias for truck 1
                if delta1 < delta2 + 1:
                    t1.insert(address)
                else:
                    t2.insert(address)

                # removes address from list to avoid redundancies
                addresses.remove(address)
                break

    # sorts addresses, leaving the higher time priority packages in place in queue
    # checker indexes will secure the place in queue for the time priority packages
    t1.route = greedy_path(t1.route, t1.route[checker1])
    checker1 = t1.route.index(t1.route[-1])
    t2.route = greedy_path(t2.route)
    checker2 = t2.route.index(t2.route[-1])

    for address in addresses:
        for item in distance_graph.address_list[address]:

            # next are the packages with special notes but no time constraints
            # these are also loaded manually
            if item[7] != '':
                print("Package %d has special note: %s\nLoad into which truck?\n(1, 2, 3)" % (item[0], item[7]))
                truck = input()
                if truck == '1':
                    t1.insert(address)
                elif truck == '2':
                    t2.insert(address)
                elif truck == '3':
                    t3.insert(address)

                # removes address from list to avoid redundancies
                addresses.remove(address)
                break

    for address in addresses:

        # at this point, the 16 package limit becomes a concern, so we need to start tracking that
        # counts the number of packages associated with an address
        packages = 0
        for item in distance_graph.address_list[address]:
            packages += 1

        # just like before, compares the total distances after greed sort starting at the checker indexes
        delta1 = total_distance(greedy_path(t1.route + [address], t1.route[checker1])) - total_distance(
            greedy_path(t1.route, t1.route[checker1]))
        delta2 = total_distance(greedy_path(t2.route + [address], t2.route[checker2])) - total_distance(
            greedy_path(t2.route, t2.route[checker2]))

        # looks at truck 3 as well
        # if truck 3 has no packages, compares instead to the distance from the hub to the address
        if len(t3.route) > 0:
            delta3 = total_distance(greedy_path(t3.route + [address])) - total_distance(greedy_path(t3.route))
        else:
            delta3 = distance_graph.edge_weights[address, '4001 South 700 East']

        # inserts into the truck with the smallest delta AND won't be overfilled
        if delta1 < delta2 and delta1 < delta3 and len(t1.packages) + packages <= 16:
            t1.insert(address)
        elif delta2 < delta3 and len(t2.packages) + packages <= 16:
            t2.insert(address)
        else:
            t3.insert(address)

    # sorts the new addresses into new list without interfering with the old queue
    append1 = greedy_path(t1.route[checker1:], t1.route[checker1])
    append2 = greedy_path(t2.route[checker2:], t2.route[checker2])

    # adds the new lists to the end of the old without interrupting the time-priority queue
    t1.route = t1.route[:checker1] + append1
    t2.route = t2.route[:checker2] + append2
    t3.route = greedy_path(t3.route)

    # adds the hub as the first index in each route in order to calculate total distance
    t1.route.insert(0, '4001 South 700 East')
    t2.route.insert(0, '4001 South 700 East')
    t3.route.insert(0, '4001 South 700 East')

    # calculates the total distance of each route
    t1.length = total_distance(t1.route)
    t2.length = total_distance(t2.route)
    t3.length = total_distance(t3.route)
