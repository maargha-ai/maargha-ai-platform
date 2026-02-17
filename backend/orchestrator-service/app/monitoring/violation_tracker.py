# app/monitoring/violation_tracker.py

MAX_WARNINGS = 3

class ViolationTracker:
    def __init__(self):
        self.warnings = 0

    def register_violation(self):
        self.warnings += 1
        return self.warnings

    def should_terminate(self):
        return self.warnings >= MAX_WARNINGS
    
    def reset(self):
        self.warnings = max(0, self.warnings - 1)
