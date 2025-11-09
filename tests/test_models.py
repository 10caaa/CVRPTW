import unittest
from src.models import Client, Vehicle, Solution, euclidean_distance


class TestModels(unittest.TestCase):
    
    def setUp(self):
        self.depot = Client(0, 0, 0, 0)
        self.client1 = Client(1, 3, 4, 10)
        self.client2 = Client(2, 6, 8, 15)
        self.client3 = Client(3, 9, 12, 20)
    
    def test_euclidean_distance(self):
        distance = euclidean_distance(self.depot, self.client1)
        self.assertAlmostEqual(distance, 5.0, places=2)
        
        distance = euclidean_distance(self.client1, self.client2)
        self.assertAlmostEqual(distance, 5.0, places=2)
    
    def test_vehicle_add_client(self):
        vehicle = Vehicle(capacity=50)
        
        self.assertTrue(vehicle.add_client(self.client1))
        self.assertEqual(vehicle.load, 10)
        self.assertEqual(len(vehicle.route), 1)
        
        self.assertTrue(vehicle.add_client(self.client2))
        self.assertEqual(vehicle.load, 25)
        self.assertEqual(len(vehicle.route), 2)
        
        self.assertTrue(vehicle.add_client(self.client3))
        self.assertEqual(vehicle.load, 45)
        self.assertEqual(len(vehicle.route), 3)
    
    def test_vehicle_capacity_constraint(self):
        vehicle = Vehicle(capacity=30)
        
        self.assertTrue(vehicle.add_client(self.client1))
        self.assertTrue(vehicle.add_client(self.client2))
        self.assertFalse(vehicle.add_client(self.client3))
        
        self.assertEqual(vehicle.load, 25)
        self.assertEqual(len(vehicle.route), 2)
    
    def test_solution_cost_calculation(self):
        vehicle = Vehicle(capacity=100)
        vehicle.add_client(self.client1)
        vehicle.add_client(self.client2)
        
        solution = Solution([vehicle], self.depot)
        
        expected_cost = (
            euclidean_distance(self.depot, self.client1) +
            euclidean_distance(self.client1, self.client2) +
            euclidean_distance(self.client2, self.depot)
        )
        
        self.assertAlmostEqual(solution.cost, expected_cost, places=2)
    
    def test_solution_feasibility(self):
        vehicle1 = Vehicle(capacity=100)
        vehicle1.add_client(self.client1)
        vehicle1.add_client(self.client2)
        
        solution = Solution([vehicle1], self.depot)
        self.assertTrue(solution.is_feasible())
        
        vehicle1.load = 150
        self.assertFalse(solution.is_feasible())


if __name__ == '__main__':
    unittest.main()
