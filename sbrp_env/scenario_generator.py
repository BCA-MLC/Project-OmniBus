import numpy as np

class ScenarioGenerator:
    def __init__(self, num_stops, num_schools, max_students_per_stop=10, attendance_prob=0.9):
        self.num_stops = num_stops
        self.num_schools = num_schools
        self.max_students = max_students_per_stop
        self.attendance_prob = attendance_prob
        
    def generate_morning_scenario(self):
        """
        Generates the initial state of students waiting at stops.
        Returns:
            demands: np.array of size (num_stops,) representing students waiting.
            school_assignments: np.array of size (num_stops,) representing which school they go to.
            start_times: np.array of size (num_schools,) representing the deadline to arrive.
        """
        # Stochastic attendance
        base_demand = np.random.randint(1, self.max_students + 1, size=self.num_stops)
        attendance_mask = np.random.binomial(1, self.attendance_prob, size=self.num_stops)
        actual_demand = base_demand * attendance_mask
        
        # Multi-school assignment (each stop is assumed to have students mostly for one school to simplify)
        # In a more complex scenario, each stop could have a vector of demands for different schools
        school_assignments = np.random.randint(0, self.num_schools, size=self.num_stops)
        
        # School start times drawn from a normal distribution
        # Centered at 75 minutes from base (= 7:45 AM, since base is 6:30 AM)
        # Standard deviation of 20 minutes
        # Clipped to [45, 120] (7:15 AM to 8:30 AM) to avoid unrealistic extremes
        # Then sorted so school 0 has the earliest deadline
        start_times = np.random.normal(loc=75, scale=20, size=self.num_schools)
        start_times = np.clip(start_times, 45, 120)
        start_times = np.sort(start_times).astype(np.float32)
        
        return actual_demand, school_assignments, start_times
