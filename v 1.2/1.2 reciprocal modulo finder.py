"""
"""

class Equation:
    """custom 'datatype' for easier handling of equations"""

    def __init__(self, LHS_dict, RHS_dict):
        """Appropriate example:
        LHS_dict = {'a':3}, LHS_dict = {'b':4, 'c':6}, resulting in 'a = bc'"""
        self.LHS_dict = LHS_dict
        self.RHS_dict = RHS_dict
        self.eliminateZeros()
        self.str = self.strEqu()

    def strEqu(self):
        LHS_str = ""
        for k,v in self.LHS_dict.items():
            LHS_str += f"{v}{k} +"
        LHS_str = LHS_str[:-1] #remove last '+'

        RHS_str = ""
        for k,v in self.RHS_dict.items():
            RHS_str += f" {v}{k} +"
        RHS_str = RHS_str[:-1] #remove last '+'
        RHS_str = RHS_str[:-1] #remove last ' '

        return LHS_str + "=" + RHS_str


    def eliminateZeros(self):
        new_LHS = {}
        new_RHS = {}
        for k,v in self.LHS_dict.items():
            if v != 0:
                new_LHS[k] = v #self.LHS_dict.pop(k)

        for k,v in self.RHS_dict.items():
            if v != 0:
                new_RHS[k] = v #self.RHS_dict.pop(k)

        self.LHS_dict = new_LHS
        self.RHS_dict = new_RHS
        print("eliminated zeros")
        self.str = self.strEqu()

    def multiply(self, scalar):
        for k,v in self.LHS_dict.items():
            self.LHS_dict[k] = v * scalar

        for k,v in self.RHS_dict.items():
            self.RHS_dict[k] = v * scalar
            
        self.str = self.strEqu()

    def divide(self, scalar):
        for k,v in self.LHS_dict.items():
            self.LHS_dict[k] = v / scalar

        for k,v in self.RHS_dict.items():
            self.RHS_dict[k] = v / scalar
            
        self.str = self.strEqu()

    def simplify(self):
        self.eliminateZeros()
        
        # divid boths sides by LHS coefficient
        if (len(self.LHS_dict)==1):
            key = next(iter(self.LHS_dict)) # get the LHS key as it is unkown
            coefficient = self.LHS_dict[key]
            #print(key, coefficient)
            if (coefficient != 1) and (self.LHS_dict[key] != 0): #only divide if needed
                '''
                self.LHS_dict[key] = 1 #dividing itself by its coefficient

                for k,v in self.RHS_dict.items():
                    print("Old RHS k,v:", k,v)
                    new_value = v/coefficient
                    self.RHS_dict[k] = new_value

                    print("New RHS k,v:", k,self.RHS_dict[k])
                '''
                self.divide(coefficient)

        self.str = self.strEqu() #update

    def rearrange(self, in_terms_of_var):
        """in_terms_of_var is a string of a variable, e.g. 'a'"""
        if (in_terms_of_var in self.LHS_dict) or (in_terms_of_var in self.RHS_dict):
            if (in_terms_of_var in self.LHS_dict) and (len(self.LHS_dict)==1):
                print("already in that form")

            elif (len(self.LHS_dict)==1) and (len(self.RHS_dict)==1):
                temp_LHS = self.LHS_dict
                self.LHS_dict = self.RHS_dict
                self.RHS_dict = temp_LHS
                print("Swapped LHS and RHS")

            elif (in_terms_of_var in self.LHS_dict): #isolate in LHS in_terms_of_var
                '''
                new_LHS = {in_terms_of_var: self.LHS_dict.pop(in_terms_of_var)*-1} #move to LHS
               
                #move other LHS terms over to RHS
                for key, value in self.LHS_dict.items():
                    self.RHS_dict[key] = value * -1 #* -1 is the moving to RHS

                print("DONE: isolating in LHS in_terms_of_var")
                print("old LHS:", self.LHS_dict)
                print("new LHS:", new_LHS)
                print("new RHS:", self.RHS_dict)

                #update
                self.LHS_dict = new_LHS
                '''

                #new way of moving terms
                new_LHS = {in_terms_of_var: self.LHS_dict.pop(in_terms_of_var)} #copy to LHS
                new_RHS = self.RHS_dict.copy()
                for k,v in self.LHS_dict.items():
                    v = v*-1 # we are subtracting original LHS terms to move to RHS
                    if k in new_RHS: #if key exists combine values
                        new_RHS[k] += v

                    else: #..just add term to new_RHS
                        new_RHS[k] = v
                        
                print("DONE: moving in_terms_of_var to LHS")
                print("old LHS:", self.LHS_dict)
                #print("new LHS:", new_LHS)
                print("old RHS:", self.RHS_dict)
                #print("new RHS:", new_RHS)

                #update
                self.LHS_dict = new_LHS
                self.RHS_dict = new_RHS

                print("new LHS:", self.LHS_dict)
                print("new RHS:", self.RHS_dict)

            elif in_terms_of_var in self.RHS_dict: #move to LHS
                '''
                new_LHS = {in_terms_of_var: self.RHS_dict.pop(in_terms_of_var)*-1} #move to LHS
                
                    
                #move LHS terms over to RHS
                for key, value in self.LHS_dict.items():
                    self.RHS_dict[key] = value * -1 #* -1 is the moving to RHS
                '''
                #new way of moving terms
                new_LHS = {in_terms_of_var: self.RHS_dict.pop(in_terms_of_var)} #move to LHS
                new_RHS = self.LHS_dict.copy()
                for k,v in self.RHS_dict.items():
                    v = v*-1 # we are subtracting original RHS to move to LHS
                    if k in new_RHS: #if key exists combine values
                        new_RHS[k] += v

                    else: #..just add term to new_RHS
                        new_RHS[k] = v
                        
                print("DONE: moving in_terms_of_var to LHS")
                print("old LHS:", self.LHS_dict)
                #print("new LHS:", new_LHS)
                print("old RHS:", self.RHS_dict)
                #print("new RHS:", new_RHS)

                #update
                self.LHS_dict = new_LHS
                self.RHS_dict = new_RHS

                print("new LHS:", self.LHS_dict)
                print("new RHS:", self.RHS_dict)
                

        else:
            print("variable not in equation")

        self.str = self.strEqu() #update


    def substitute(self, equToSubIn, var_to_sub_in_by):
        """if equ_1: a = 2b and equ_2: c = b + a, then if var_to_sub_in_by = 'b'
        equ_2: b = c - a, then subbed into equ_1, equ_1: a = 2(c - a)"""
        
        equToSubIn = equToSubIn
        equToSubIn.rearrange(var_to_sub_in_by)
        equToSubIn.simplify()
        print("equToSubIn:", equToSubIn.str)
        print("master equation:", self.str)
            

MOD_NUM = 26
steps_list = []

def step(a,b, counter=''):
    """Returns quotient and remainder formed from a = bq + r, and a message"""
    if b==0:
        return a, 0, "b=0, therefore division by zero prevented" #q, r, msg
    
    quotient = a//b
    remainder = a%b 
    equation_str = f"{a} = {b}*{quotient} + {remainder}"
    if a == b*quotient + remainder: #should always be true
        step_dict = {'a':a, 'b':b, 'q':quotient, 'r':remainder, 'equation_str':equation_str, 'step':counter}
        steps_list.append(step_dict)
        return quotient, remainder, f"Step {counter}: {equation_str}"
    else:
        return False, False, f"ERROR @ Step {counter}: a != bq + r -> {equation_str}" #q, r, msg
    
def getGCD(a, b):
    """Python also supports this natively, math.gcd()
    Returns bool and the GCD of 'a' and 'b'."""
    a = abs(a)
    b = abs(b)
    """
    abs() is an acceptable and legal move.
    We can see that 4 is the GCD in (-4, -12), (4, -12), (-4, 12), and (4, 12).
    Even in the case of (-4,-12) were -4 would seem to be correct,
    +4 is techniquely the Greatest Commond Divisor.
    The use of abs() does solve a hiccup in getGCD(-4, 12)
    """
    counter = 1
    
    quotient, remainder, msg = step(a, b, counter)
    print(msg)
    counter += 1
    
    if remainder == 0:
        print("GCD is the inputted 'b' value:", b)
        return True, b

    else: #continue to find GCD
        
        new_b = b
        while remainder != 0:
            new_a = new_b
            new_b = remainder
        
            quotient, remainder, msg = step(new_a, new_b, counter)
            print(msg)
            
            if remainder == 0:
                counter +=1
                print("GCD is the inputted 'new_b' value from the last step:", new_b)
                return True, new_b
            
            elif remainder == 1:
                counter +=1
                print("GCD is the remainder,", remainder)
                return True, remainder 

            else:
                counter +=1

    

def getModReciprocal(determinant=7):
    """For Modulo-26. Returns a bool and the value."""
    '''
    if determinant % 2 == 0:
        #divisble by 2 if there is no remainder
        return False, None

    elif determinant % 13 == 0:
        #divisble by 13 if there is no remainder
        return False, None
    '''
    if True: #above commented out code checks for 2 and 13 divisibility but results in incorrect answers (e.g. 4^-1 in mod-27 is 7 and does exist)
        is_good_for_mod_inverses, GCD = getGCD(MOD_NUM, determinant)
        if is_good_for_mod_inverses and (GCD == 1):
            #equation in form: gcd = factor_1(coefficent) - factor_2(coeffienct)
            factor_1 = steps_list[-1]['a']
            coefficient_1 = 1
            factor_2 = steps_list[-1]['b'] * -1 #because r = a -bq
            coefficient_2 = steps_list[1]['q']
            equation_str = f"{GCD} = {factor_1}*{coefficient_1} + {factor_2}*{coefficient_2}"


            master_equation_dict = {'gcd': GCD, #1
                                    'factor_1': factor_1,
                                    'coefficient_1': coefficient_1,
                                    'factor_2': factor_2,
                                    'coefficient_2': coefficient_2,
                                    'equation_str': equation_str}
            print(master_equation_dict)

            """
            #next step is sub. r = a - bq into gcd = factor_1(coefficent) - factor_2(coeffienct)
            if steps_list[-2]['r'] == factor_2:

                
            new_factor_1 = steps_list[-2]['a']
            new_coefficient_1 = 1
            new_factor_2 = steps_list[-2]['b'] * -1 #because r = a -bq
            new_coefficient_2 = steps_list[-2]['q']
            #equation_str = f"{GCD} = {factor_1}*{coefficient_1} + {factor_2}*{coefficient_2}"
            """
            

def run():
    determinant_value = int(input("Enter determinant value: "))

    print(getModReciprocal(determinant_value))
