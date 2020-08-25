from InventoryAllocator import InventoryAllocator
import unittest

class TestInventoryAllocator (unittest.TestCase):
    def test_exactMatch(self):
        inventory=[{ "name": "owd", "inventory": { "apple": 1 } }]
        inputs= { "apple": 1 }
        result = InventoryAllocator().SearchInventory(inputs, inventory)
        self.assertEqual(result, [{ "owd": { "apple": 1 } }])

    def test_insufficientInventory(self):
        inventory=[{ "name": "owd", "inventory": { "apple": 0 } }]
        inputs= { "apple": 1 }
        result = InventoryAllocator().SearchInventory(inputs, inventory)
        self.assertEqual(result, [])

    def test_splitInventory(self):
        inventory=[{ "name": "owd", "inventory": { "apple": 5 } }, { "name": "dm", "inventory": { "apple": 5 }}]
        inputs= { "apple": 10 }
        result = InventoryAllocator().SearchInventory(inputs, inventory)
        sortedResult = sorted(result, key=lambda x: (list(x.keys()))[0])
        expectedResult = sorted([{ "dm": { "apple": 5 }}, { "owd": { "apple": 5 } }], key=lambda x: (list(x.keys()))[0])
        self.assertEqual(sortedResult, expectedResult)

    def test_complexInputWithRepeatingLocations(self):
        inventory=[ { 'name': 'owd', 'inventory': { 'apple': 5, 'orange': 10} }, { 'name': 'dm', 'inventory': { 'apple': 5, 'orange': 10 } }, { 'name': 'dm', 'inventory': { 'apple': 2, 'orange': 2 } } ]
        inputs={ 'apple': 8 }
        result = InventoryAllocator().SearchInventory(inputs, inventory)
        self.assertEqual(result, [{'owd': {'apple': 5}}, {'dm': {'apple':3}}])

    def test_complexInputWithRepeatingLocationsAndInvalidCounts(self):
        inventory=[ { 'name': 'owd', 'inventory': { 'apple': 5, 'orange': 10, 'carrots': 0 } }, { 'name': 'dm', 'inventory': { 'apple': 5, 'orange': 10 } }, { 'name': 'dm', 'inventory': { 'apple': 2, 'orange': 2 } } ]
        inputs={ 'apple': 8 }
        result = InventoryAllocator().SearchInventory(inputs, inventory)
        self.assertEqual(result, [{'owd': {'apple': 5}}, {'dm': {'apple':3}}])

if(__name__ == '__main__'):
    unittest.main()