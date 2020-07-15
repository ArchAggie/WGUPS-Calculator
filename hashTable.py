
# Brian Parsons
# Student ID - 001008912
# C950 - Data Structures & Algorithms II
# Performance Assessment

import csv

global hashtable


# chaining hash table
class ListHash:

    table = []

    # initializes the table with a default of 10 buckets
    # O(n)
    def __init__(self, length=10):

        # assigns each bucket an empty list
        self.table = []
        for i in range(length + 1):
            self.table.append([])

        # self.hashtable = self.get_packages('WGUPS Packages.csv')
        self.count = 0

    # O(n)
    def insert(self, key, package):

        # this function uses the first index (package ID) as a key
        # and inserts the entire list into the bucket
        package[0] = int(package[0])
        bucket = key % len(self.table)
        self.table[bucket].append(package)
        package.append('At Hub')
        self.count += 1

    # O(1)
    def search(self, key):

        # finds bucket just like insert function
        bucket = key % len(self.table)
        bucket_list = self.table[bucket]

        # once bucket is found, searches bucket for given key
        for package in bucket_list:
            if package[0] == key:
                return package

        # returns 0 if package isn't found
        return 0

    # O(n)
    def remove(self, key):

        # finds bucket and package just like search
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # if package is found, removes package
        # does nothing otherwise
        for package in bucket_list:
            if package[0] == key:
                bucket_list.remove(package)
                self.count -= 1

    # O(1)
    def add(self, key):

        # adds a new package to the list
        bucket = key % len(self.table)
        bucket_list = self.table[bucket]

        return 0

    # O(n)
    def totalcount(self):
        return self.count

    # O(1)
    def package(self, index):
        return self.table[index]


# O(n)
def get_packages(filename):

    # creates a hash table based off of csv file data
    new_hash = ListHash()
    with open(filename) as csvDataFile:

        csv_reader = csv.reader(csvDataFile)

        # each line in the csv is a complete formatted package
        # inserts entire row into the hash table with row[0] being package ID
        for row in csv_reader:
            new_hash.insert(int(row[0]), row)
    return new_hash


# calls function to make the table using our csv
hashtable = get_packages('WGUPS Packages.csv')
