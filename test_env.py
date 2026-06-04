import unittest
from sbrp_env.env import HackensackSBRPOptimizationEnv

class TestSBRPEnv(unittest.TestCase):
    def test_env_initialization(self):
        env = HackensackSBRPOptimizationEnv(num_stops=5, num_schools=1, num_buses=2)
        obs, info = env.reset()
        
        self.assertEqual(env.bus_states.shape, (2, 4))
        self.assertEqual(env.stop_states.shape, (5, 2))
        self.assertTrue("bus_states" in obs)
        self.assertTrue("stop_states" in obs)
        self.assertTrue("global_time" in obs)
        self.assertTrue("current_bus" in obs)
        
    def test_valid_action_mask(self):
        env = HackensackSBRPOptimizationEnv(num_stops=5, num_schools=1, num_buses=2)
        obs, info = env.reset()
        mask = env.valid_action_mask()
        
        self.assertEqual(len(mask), 6) # 1 school + 5 stops
        
        # At start, buses should be able to go to stops that have students
        valid_actions = sum(mask)
        self.assertTrue(valid_actions > 0)
        
if __name__ == '__main__':
    unittest.main()
