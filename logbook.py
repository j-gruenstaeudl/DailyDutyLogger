import matplotlib.pyplot as plt
import datetime
import numpy as np

from weeklylog import weeklylog # Import numpy for arange

class logbook:
    def __init__(self):
        self.days_of_work = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.num_days = len(self.days_of_work)
        self.activity_mapping = {
            'F': 0, # Driving
            'P': 1, # Break
            'A': 2 # Work
        }
        self.colors = {
            'F': 'blue',
            'P': 'yellow',
            'A': 'blue'
        }
        
        self.weeklylog = weeklylog("03.05.25 bis 04.05.25", "Manfred", 31)