import typing
import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np
class courseAssignment: 
    preferences = None
    course_capacety = None

    def weight(self, student, course) -> int:
        """Get score for combination of student and course. Lower is better

        Args:
            student (str): key of the student in the preferences dict
            course (str): key of the student in the preferences dict

        Returns:
            int: score for the combination of student and course. Lower is better
        """
        result = None
        # if student did not specify course in preference penalty is 100000
        if course in preferences[student]: 
            result = preferences[student].index(course)
        else: 
            result = 100000
        return result 

    def get_best_assignment(self) -> None:
        """Prints the best assignment for every student. 
        """
        m = gp.Model("Model")
        # array of tuples. Each tuple is (student, course) and is used for the assignment to the guroby binary variable indecating if the student selected the course.
        possible_assignments =  [(student,course) for student in preferences.keys() for course in course_capacety.keys()]
        assigments_gurobi = m.addVars(possible_assignments, vtype=GRB.BINARY)
        # get a cost dict in order to avoid recomputation in every simplex iteration. 
        costs = {}
        for possible_assignment in possible_assignments:
            costs[possible_assignment] = self.weight(possible_assignment[0],possible_assignment[1])
        # set the objective function
        m.setObjective(quicksum(assigments_gurobi[assignment] * costs[assignment] for assignment in possible_assignments), GRB.MINIMIZE)
        # add constraint to not exceed the capacity of a course
        m.addConstrs(quicksum(assigments_gurobi[student,course] for student in preferences.keys()) <= course_capacety[course] for course in course_capacety.keys())
        # add constraint to guarantee that every student is assigend to exactly one course
        m.addConstrs(quicksum(assigments_gurobi[student,course] for course in course_capacety.keys()) == 1 for student in preferences.keys() )
        m.optimize()
        
        # get every positive assignment
        optimized_assignments = [a for a in possible_assignments if assigments_gurobi[a].x > 0.99]
        for entry in optimized_assignments: 
            print(f"Studente {entry[0]} is assigened to {entry[1]}")
        print(f"Overall score: {np.sum([costs[entry] for entry in optimized_assignments ])}")



    def __init__(self, preferences:dict, course_capacety: dict):
        self.preferences = preferences
        self.course_capacety = course_capacety
        self.get_best_assignment()
   
preferences = {
                "Student 1"	 : [ "Course 1","Course 4","Course 2","Course 3"],
                "Student 2"	 : [ "Course 5","Course 3","Course 4","Course 1"],
                "Student 3"	 : [ "Course 3","Course 2","Course 5","Course 1"],
                "Student 4"	 : [ "Course 3","Course 5","Course 4","Course 2"],
                "Student 5"	 : [ "Course 1","Course 5","Course 3","Course 2"],
                "Student 6"	 : [ "Course 2","Course 4","Course 1","Course 3"],
                "Student 7"	 : [ "Course 5","Course 4","Course 2","Course 1"],
                "Student 8"	 : [ "Course 4","Course 5","Course 2","Course 1"],
                "Student 9"	 : [ "Course 3","Course 2","Course 4","Course 1"],
                "Student 10" : [ "Course 1","Course 3","Course 4","Course 2"],
                "Student 11" : [ "Course 1","Course 3","Course 5","Course 4"],
                "Student 12" : [ "Course 3","Course 2","Course 4","Course 5"],
                "Student 13" : [ "Course 1","Course 4","Course 3","Course 2"],
                "Student 14" : [ "Course 1","Course 2","Course 5","Course 4"],
                "Student 15" : [ "Course 5","Course 2","Course 4","Course 3"],
                "Student 16" : [ "Course 5","Course 4","Course 3","Course 1"],
                "Student 17" : [ "Course 2","Course 3","Course 4","Course 5"],
                "Student 18" : [ "Course 2","Course 5","Course 1","Course 3"],
                "Student 19" : [ "Course 4","Course 2","Course 3","Course 5"],
                "Student 20" : [ "Course 2","Course 1","Course 4","Course 5"]
            }
course_capacety= {
    'Course 1': 2, 
    'Course 2': 2, 
    'Course 3': 2, 
    'Course 4': 5, 
    'Course 5': 5, 
    'Overfow' : float('inf')
}
courseAssignment(preferences, course_capacety)
