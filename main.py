import typing
import gurobipy as gp
from gurobipy import GRB, quicksum
import numpy as np
class courseAssignment: 
    preferences = None
    courseCapacety = None

    def weight(self, student, course) -> int:
        result = None
        if course in preferences[student]: 
            result = preferences[student].index(course)+1
        else: 
            result = 100000
        return result 

    def get_best_assignment(self) -> dict:
        m = gp.Model("Model")
        # array of tuples. Each tuple is (student, course) an is used for the assignment
        possible_assignments =  [(student,course) for student in preferences.keys() for course in CourseCapacety.keys()]
        costs = {}
        for possible_assignment in possible_assignments:
            costs[possible_assignment] = self.weight(possible_assignment[0],possible_assignment[1])

        assigments_gurobi = m.addVars(possible_assignments, vtype=GRB.BINARY)
        m.setObjective(quicksum(assigments_gurobi[assignment] * costs[assignment] for assignment in possible_assignments), GRB.MINIMIZE)
        # we cannot exceed the capacity of a course
        m.addConstrs(quicksum(assigments_gurobi[i,j] for i in preferences.keys()) <= CourseCapacety[j] for j in CourseCapacety.keys())

        # each student needs to be assigned to one course
        m.addConstrs(quicksum(assigments_gurobi[i,j] for j in CourseCapacety.keys()) == 1 for i in preferences.keys() )

        
        
        m.optimize()
        optimized_assignments = [a for a in possible_assignments if assigments_gurobi[a].x > 0.99]
        for entry in optimized_assignments: 
            print(f"Studente {entry[0]} is assigened to {entry[1]}")
        for entry in optimized_assignments: 
            print(entry[1].removeprefix('Course '))
        print(np.sum([costs[entry] for entry in optimized_assignments ]))



    def __init__(self, preferences:dict, courseCapacety: dict):
        self.preferences = preferences
        self.courseCapacety = courseCapacety
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
                "Student 17" : ["Course 2",	"Course 3","Course 4","Course 5"],
                "Student 18" : ["Course 2",	"Course 5","Course 1","Course 3"],
                "Student 19" : [ "Course 4","Course 2","Course 3","Course 5"],
                "Student 20" : ["Course 2",	"Course 1","Course 4","Course 5"]
            }
CourseCapacety= {
    'Course 1': 5, 
    'Course 2': 5, 
    'Course 3': 5, 
    'Course 4': 5, 
    'Course 5': 5
}
courseAssignment(preferences, CourseCapacety)
