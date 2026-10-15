import Challenge
open ThreeVisitsScheduling
example : visits [1,4] 2 [0,0,1,1] = true := by native_decide
example : visits [1,4] 2 [0,1,0,1] = false := by native_decide
example : visits [1] 3 [0,0,0] = true := by native_decide
