
# Brian Parsons
# Student ID - 001008912
# C950 - Data Structures & Algorithms II
# Performance Assessment

import algorithm
import hashTable


def interface(amount=None):

    # Starts time at 8:00
    # Will continue to ask for user input until input = 'X'
    cycle = 1
    time = "8:00"

    # Converts time into a minute int value for comparison
    time_minutes = sum(x * int(t) for x, t in zip([60, 1], time.split(":")))

    while cycle != 0:
        print("\n'S' to search for a single packages' status."
              "\n'C' to check the status of all packages."
              # "\n'E' to Edit an address."
              "\n'I' to insert a package to the delivery list."
              "\n'L' to load trucks."
              "\n'T' to adjust the time."
              "\n'B' to begin a truck's delivery route from the hub."
              "\n'X' to exit.\n")
        user_input = input()

        if user_input == 'S':

            # Searches for a package using the package ID as a key and
            # prints the associated information regarding that single package
            # package ID, shipping address, delivery deadline, weight, special notes, and status as of the current time
            checking = 1
            while checking == 1:

                package_id = input("\nEnter package ID# ('X' to cancel')\n")
                if package_id == 'X':
                    checking = 0
                else:
                    package = hashTable.hashtable.search(int(package_id))

                # If package is found, will provide all info for single package
                    if package != 0:
                        print("\nPackage ID: %d\nShipping Address: %s, %s, %s, %s\nDelivery By: %s\nWeight: %s\nNotes: "
                              "%s\n"
                              % (package[0], package[1], package[2], package[3], package[4], package[5],
                                 package[6], package[7]))
                        print("Status: %s" % package[8])
                    else:
                        print("Package not found.")

        elif user_input == 'C':

            # loops through the hash table using the package ID as a key
            # prints the status of each package as of the current time
            for i in range(1, hashTable.hashtable.totalcount() + 1):

                package = hashTable.hashtable.search(i)

                # print(package)
                print("The status of Package ID # %d is currently %s" % (package[0], package[8]))

        elif user_input == 'I':

            # inserts new package into hash table along with all associated information
            # (shipping address, required delivery time, etc.)

            # package = hashTable.hashtable.insert()
            package = ["", "", "", "", "", "", "", ""]

            package[0] = input("Enter new package's Package ID\n")

            package[1] = input("Enter street address\n")
            package[2] = input("Enter city\n")
            package[3] = input("Enter state\n")
            package[4] = input("Enter zip code\n")
            package[5] = input("Enter required delivery time\n")
            package[6] = input("Enter package's mass in kilograms\n")
            package[7] = input("Enter any special notes (OPTIONAL)\n")

            hashTable.hashtable.insert(int(package[0]), package)

        elif user_input == 'L':

            # Calls function to load trucks, should optimally be done first
            algorithm.load_trucks()

        elif user_input == 'T':

            # user will input a time which is converted into minutes
            print("It is currently %s.\nWhat time would you like to jump to?\n" % time)
            time = input()
            time_minutes = sum(x * int(t) for x, t in zip([60, 1], time.split(":")))

            # time in minutes is used to check if packages have been delivered
            algorithm.t1.passed_time(time_minutes)
            algorithm.t2.passed_time(time_minutes)
            algorithm.t3.passed_time(time_minutes)

        elif user_input == 'B':

            # gets truck to 'leave the hub' storing current time for future distance comparisons
            print("Which truck would you like to initialize? (1, 2, 3)\n")
            truck = input()
            if truck == '1':
                algorithm.t1.leave_hub(time_minutes)
            elif truck == '2':
                algorithm.t2.leave_hub(time_minutes)
            elif truck == '3':
                algorithm.t3.leave_hub(time_minutes)

        elif user_input == 'X':

            # Exits the program
            cycle = 0


interface()

print('\nTotal distance traveled: %.1f miles' % (algorithm.t1.length + algorithm.t2.length + algorithm.t3.length))
