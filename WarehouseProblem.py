def getProduct(order: dict):
    warehouses = {
        "OH": {
            "sources": [('OR', 3)],
            "inventory": {
                "Acoustic Bloc Screen": 10,
                "Standing Desk": 100,
                "Office Chair": 12,
                "Drawer Organizer": 1,
                "Fire-proof Safe": 5
            }
        },
        "OR": {
            "sources": [('GA', 4)],
            "inventory": {
                "Acoustic Bloc Screen": 15,
                "Standing Desk": 2,
                "Drawer Organizer": 35,
                "Fire-proof Safe": 2
            },
        },
        "GA": {
            "sources": [('OR', 4), ('IA', 2), ('NH', 1)],
            "inventory": {
                "Acoustic Bloc Screen": 2,
                "Standing Desk": 2,
                "Office Chair": 2,
                "Drawer Organizer": 1,
            }
        },
        "NH": {
            "sources": [('GA', 1), ('IA', 3)],
            "inventory": {
                "Acoustic Bloc Screen": 10,
                "Standing Desk": 2,
                "Office Chair": 2,
                "Drawer Organizer": 1,
            }
        },
        "IA": {
            "sources": [('OH', 1)],
            "inventory": {
                "Acoustic Bloc Screen": 10,
                "Standing Desk": 2,
                "Office Chair": 2,
                "Drawer Organizer": 1,
            }
        },
    } # end of warehouse dict

    if not order: # edge case incase input is empty
        return "Product Not available"


    if order["originating_wh"] in warehouses: # checks if input key in dict.
        # Assigns easier to read variables.
        originating_wh = order["originating_wh"]
        product = order["product"]
        demand = order["demand"]

        if product in warehouses[originating_wh]["inventory"]:  # check if our current warehouse has the product we want
            print("demand:",order["demand"]) #
            print("Location:", originating_wh, "Time:", 0, "product amount:", "-", warehouses[originating_wh]["inventory"][product])
            currquanity = demand - warehouses[originating_wh]["inventory"][product]   # demand - currently location stock


            time = 0  # used to track time to fill order.
            visited = set()  # used to track locations we have already visited.
            visited.add(originating_wh)  # add start location

            while currquanity > 0 and len(visited) != len(warehouses):  # loops until we reach 0 quantity needed or every warehouse is visited.
                for location, distance in warehouses[originating_wh]["sources"]:  # loops through our current input Sources list of tuples

                    if location in warehouses and location not in visited and product in warehouses[location]["inventory"]:
                        print("Location:", location, "Time:", distance, "product amount:", "-", warehouses[location]["inventory"][product] )  # display purposes
                        time += distance
                        currquanity -= warehouses[location]["inventory"][product]  # updates how many products we need left
                        visited.add(location)

                    if currquanity <= 0: # due to some location having higher amount we need to be able to know if the order has been overfilled, thus completed.
                        order["time to fill order"] = time  # add time key and value to order dict so user can see the expected time to delivery
                        return order

                originating_wh = location  # updates originating_wh to curr sources warehouse, so we can check that location in next loop

            # currquantity is never reaches 0
            return "Not enough products in stock. Items left: " + str(currquanity)

# ----------------------------------------------------------------------
# Test cases
order1 = {
        'originating_wh': 'OH',
        'product': 'Acoustic Bloc Screen',
        'demand': 35 }

order2 = {}

order3 = {'originating_wh': 'OH',
        'product': 'Acoustic Bloc Screen',
        'demand': 70}  # only 47 available

print(getProduct(order1))  # return order + time taken  # Correct
print("---------------------------------------------")
print(getProduct(order2))  # Product Not available  # Correct
print("---------------------------------------------")
print(getProduct(order3))  #Not enough products in stock. Items left:', 23)  #

# Worst cases:
# Time Complexity: 0(N^2) due to having to check potentially check every warehouse twice in the Sources list of tuples until currquantity < 0 or len(visited set) == len(warehouse keys).
# Space Complexity:  0(N) as we are using a set() to store n visted locations, which in the worst case could hold every location (n)
