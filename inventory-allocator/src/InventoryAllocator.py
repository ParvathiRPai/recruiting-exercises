import copy

class InventoryAllocator:
    def SearchInventory(self, inputs, inventory):
        if not inputs or not inventory:
            return []
        
        #de-dup and removes items whose count is 0
        cleanedInventories = self.cleanInventories(inventory)
        inventoryLocationItemMaplist = self.listInventoryLocationsItemCountMapping(inputs, cleanedInventories)
        return inventoryLocationItemMaplist

    def cleanInventories(self, inventories):
        mergedInventories = {}
        for currentInv in inventories:
            currentInvName = currentInv["name"]
            currenInvInv = currentInv["inventory"]
            if (not currentInvName in mergedInventories):
                mergedInventories[currentInvName]=currentInv
            else:
                for item, count in currenInvInv.items():
                    if (item in mergedInventories[currentInvName]["inventory"].keys()):
                        mergedInventories[currentInvName]["inventory"][item] += count
                    else:
                        mergedInventories[currentInvName]["inventory"][item] = count
        mergedInventories = [value for key, value in mergedInventories.items()]

        for currentInv in mergedInventories:
            deletedItems = []
            currentInvInv = currentInv["inventory"]
            for item, count in currentInvInv.items():
                if not count:
                    deletedItems.append(item)
            for item in deletedItems:
                del currentInvInv[item]
        
        return mergedInventories

    # inventory = { name: someName, inventory: { itemName: itemCount }}
    def listInventoryLocationsItemCountMapping(self, inputItemCountMapping, inventoryList):
        remainingItemCounts = copy.deepcopy(inputItemCountMapping)
        satisfiedOrderInvList = {}
        for inventory in inventoryList:
            invInv = inventory["inventory"]
            invName = inventory["name"]
            # add potentially empty location to result
            satisfiedOrderInvList[invName] = {}
            for item, count in remainingItemCounts.items():
                if(item in invInv):
                    if(remainingItemCounts[item] >= invInv[item]):
                        remainingItemCounts[item] -= invInv[item]
                        satisfiedOrderInvList[invName][item] = invInv[item]
                    else:
                        satisfiedOrderInvList[invName][item] = remainingItemCounts[item]
                        remainingItemCounts[item] = 0
        if(any([True for item, count in remainingItemCounts.items() if count > 0])):
            return []
        return [{k: v} for k, v in satisfiedOrderInvList.items()]