"""
ModInverseFinder to be run on https://www.online-python.com/
"""



class Equation:
    """custom 'datatype' for easier handling of equations"""

    def __init__(self, LHS_dict, RHS_dict, dev_prints=False):
        
        self.dev_prints = dev_prints
        
        self.LHS_dict = LHS_dict
        self.RHS_dict = RHS_dict
        self.eliminateZeros()
        self.str = self.strEqu()

    def devOutput(self, *args):
        if self.dev_prints:
            str_output = ""
            for arg in args:
                str_output += str(arg)

            print(args)


    def strEqu(self):
        LHS_str = ""
        for k,v in self.LHS_dict.items():
            LHS_str += f"{v}*{k} +"
        LHS_str = LHS_str[:-1] #remove last '+'

        RHS_str = ""
        for k,v in self.RHS_dict.items():
            RHS_str += f" {v}*{k} +"
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
        self.devOutput("eliminated zeros")
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

    def isVarPresent(self, var_to_check_for):
        if (var_to_check_for in self.LHS_dict) or (var_to_check_for in self.RHS_dict):
            return True
        else:
            return False

    def simplify(self):
        self.eliminateZeros()
        
        # divid boths sides by LHS coefficient
        if (len(self.LHS_dict)==1):
            key = next(iter(self.LHS_dict)) # get the LHS key as it is unkown
            coefficient = self.LHS_dict[key]
            self.devOutput(key, coefficient)
            if (coefficient != 1) and (self.LHS_dict[key] != 0): #only divide if needed
                
                self.divide(coefficient)

        self.str = self.strEqu() #update

    def rearrange(self, in_terms_of_var):
        """in_terms_of_var is a string of a variable, e.g. 'a'"""
        if (in_terms_of_var in self.LHS_dict) or (in_terms_of_var in self.RHS_dict):
            if (in_terms_of_var in self.LHS_dict) and (len(self.LHS_dict)==1):
                self.devOutput(in_terms_of_var, "already on LHS for", self.str)

            elif (len(self.LHS_dict)==1) and (len(self.RHS_dict)==1):
                temp_LHS = self.LHS_dict
                self.LHS_dict = self.RHS_dict
                self.RHS_dict = temp_LHS
                self.devOutput("Swapped LHS and RHS")

            elif (in_terms_of_var in self.LHS_dict): #isolate in LHS in_terms_of_var
                
                #new way of moving terms
                new_LHS = {in_terms_of_var: self.LHS_dict.pop(in_terms_of_var)} #copy to LHS
                new_RHS = self.RHS_dict.copy()
                for k,v in self.LHS_dict.items():
                    v = v*-1 # we are subtracting original LHS terms to move to RHS
                    if k in new_RHS: #if key exists combine values
                        new_RHS[k] += v

                    else: #..just add term to new_RHS
                        new_RHS[k] = v

                #update
                self.LHS_dict = new_LHS
                self.RHS_dict = new_RHS

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

                #update
                self.LHS_dict = new_LHS
                self.RHS_dict = new_RHS
                

        else:
            self.devOutput("variable not in equation")

        self.str = self.strEqu() #update


    def substitute(self, equToSubIn):
        """if equ_1 (this Obj): a = 2b and equ_2 (equToSubIn): c = b + a, then if var_to_sub_in_by = 'b'
        equ_2: b = c - a, then subbed into equ_1, equ_1: a = 2(c - a)
        equ_1 must have 1 term in LHS"""
        
        equToSubIn = equToSubIn
        var_to_sub_in_by = next(iter(equToSubIn.LHS_dict)) #grab the singular key  #equToSubIn.rearrange(var_to_sub_in_by)
        self.devOutput("equToSubIn:", equToSubIn.str)
        self.devOutput("target equation:", self.str)

        if  self.isVarPresent(var_to_sub_in_by): 

            if len(self.LHS_dict) > 1:
                self.devOutput("several terms in LHS of the master equation:", self.str, self)

            else:
                equation_scalar = self.RHS_dict.pop(var_to_sub_in_by)#scalar for the subbed equation on the RHS

                new_master_RHS = self.RHS_dict.copy()

                for k,v in equToSubIn.RHS_dict.items():
                    v = v * equation_scalar
                    if k in new_master_RHS: #if key exists combine values
                        new_master_RHS[k] += v

                    else: #..just add term to new_RHS
                        new_master_RHS[k] = v

                self.RHS_dict = new_master_RHS
                self.str = self.strEqu() #update

                self.devOutput("New master equation:", self.str, "\n")

        else:
            self.devOutput("var_to_sub_in_by:", var_to_sub_in_by, "NOT present in both sides of target equation")


        self.str = self.strEqu() #update
          

  

DEV_MODE = False 
GUI_DEV_OUTPUT = False

class ModInverseFinder:
    """class for finding inverse mod-n numbers"""

    def __init__(self):
        """"""

        self.equation_steps_dict = {} #keeps track of the steps


    def devOutput(self, *args):
        if DEV_MODE:
            str_output = ""
            for arg in args:
                str_output += str(arg)

            print(str_output)

            

    def step(self, a,b, counter=''):
        if b==0:
            return a, 0, "b=0, therefore division by zero prevented" #q, r, msg
    
        quotient = a//b
        remainder = a%b 
        equation_str = f"{a} = {b}*{quotient} + {remainder}"
    
        if a == b*quotient + remainder: #should always be true
            self.equation_steps_dict[counter] =  Equation({a:1}, {b:quotient, remainder:1}, DEV_MODE) #adding object to record variable
            self.equation_steps_dict[counter].rearrange(remainder)
            return quotient, remainder, f"Step {counter}: {equation_str} -> {self.equation_steps_dict[counter].str}" #q, r, msg
        else:
            return False, False, f"ERROR @ Step {counter}: a != bq + r -> {equation_str}" #q, r, msg
    
    def getGCD(self, a, b):
        """Returns bool and the GCD of 'a' and 'b'."""
        a = abs(a)
        b = abs(b)
        """
        abs() is an acceptable and legal move.
        For example, we can see that 4 is the GCD in (-4, -12), (4, -12), (-4, 12), and (4, 12).
        Even in the case of (-4,-12) were -4 would seem to be correct +4 is techniquely the Greatest Commond Divisor.
        """
        counter = 1 #to keep track and name the steps
    
        quotient, remainder, msg = self.step(a, b, counter)
        self.devOutput(msg)
        counter += 1
    
        if remainder == 0:
            self.devOutput("GCD is the inputted 'b' value:", b)
            return True, b
        elif remainder == 1:
            self.devOutput("GCD is 1")
            return True, 1

        else: #continue to find GCD
        
            new_b = b
            while remainder != 0:
                new_a = new_b
                new_b = remainder
        
                quotient, remainder, msg = self.step(new_a, new_b, counter)
                self.devOutput(msg)
            
                if remainder == 0:
                    counter +=1
                    self.devOutput("GCD is the inputted 'new_b' value from the last step:", new_b)
                    return True, new_b
            
                elif remainder == 1:
                    counter +=1
                    self.devOutput("GCD is the remainder,", remainder)
                    return True, remainder 

                else:
                    counter +=1


    def getModReciprocal(self, MOD_NUM, integer):
        """For Modulo-n. Returns a success bool and the inverse."""
        integer = abs(integer) #negatives just have an extra factor of -1 and thus -3 and 3 will have the same inverse
        
        if integer == 1:
            """
            breaks the program (spits out 0) but this legal because any number outside of the MOD_NUM range gets reduced after calculation
            I 1/a = x mod-n OR 1 mod-n = a * x, where when a=1, there is no remainder meaning the significant number (inverse) is a
            Think of the Euclidean Algorithm used for GCD, described as a= bq + r, when r = 0 the GCD is b.
            """
            integer += MOD_NUM

        else:
        
            is_good_for_mod_inverses, GCD = self.getGCD(MOD_NUM, integer)
        
            if is_good_for_mod_inverses and (GCD == 1): #double check
                self.devOutput("\nGetting Inverse...\n")
                self.devOutput(self.equation_steps_dict)
            
                num_of_steps = len(self.equation_steps_dict)
                MasterEquation = self.equation_steps_dict[num_of_steps]
                self.devOutput(MasterEquation.RHS_dict)

                for step in range(1, num_of_steps): #skips if num_of_steps == 1
                    step_num = num_of_steps - step

                    self.devOutput("step:", step, "out of:", num_of_steps, ". step_num:", step_num)
                
                    step_to_sub_in = self.equation_steps_dict[step_num]
                    self.devOutput("step_to_sub_in:", step_to_sub_in.RHS_dict)
        
                    MasterEquation.substitute(step_to_sub_in)

                is_mod_num_in_master_equation = (MOD_NUM in MasterEquation.RHS_dict) or (MOD_NUM in MasterEquation.RHS_dict.values())
                self.devOutput("is_mod_num_in_master_equation:", is_mod_num_in_master_equation)
                
                if (len(MasterEquation.RHS_dict) == 2) and is_mod_num_in_master_equation: #something will be wrong if MOD_NUM not in the equation to cancel one out of two terms
                    
                    self.devOutput("Final equation:", MasterEquation.str)
                    self.devOutput("RHS:", MasterEquation.RHS_dict)
                    self.devOutput(f"when key=Mod ({MOD_NUM}), value= {MasterEquation.RHS_dict[MOD_NUM]}")
                
                    inverse = MasterEquation.RHS_dict[integer]
                    self.devOutput("raw inverse:", inverse)
                    
                    #bring into MOD_NUM range
                    while inverse >= MOD_NUM: #e.g. max is 25 for Mod-26
                        inverse -= MOD_NUM
                        self.devOutput("inverse modulo:", inverse)

                    while inverse < 0:
                        inverse += MOD_NUM
                        self.devOutput("inverse modulo:", inverse)

                    self.devOutput(f"FINAL ANSWER: Inverse Modulo-{MOD_NUM} of {integer} is {inverse}")
                    return True, inverse

                else:
                    msg = "ERROR, len(MasterEquation.RHS_dict) == 2) and is_mod_num_in_master_equation: ", (len(MasterEquation.RHS_dict) == 2) and (is_mod_num_in_master_equation)
                    self.devOutput(msg)
                    self.UserInterface.output_lbl['text'] = "Error"
                    return False, None

            else:
                self.devOutput("is_good_for_mod_inverses:", is_good_for_mod_inverses)
                return False, None

    def run(self, mod_num, integer):
        self.equation_steps_dict.clear()
        
        self.devOutput("running")
        is_successful, result = self.getModReciprocal(mod_num, integer)
        if is_successful:
            print(f"Inverse of {integer} (mod-{mod_num}) is: {result}")
        else:
            print(f"Inverse of {integer} (mod-{mod_num}) does not exist")





if __name__ == "__main__":
    app = ModInverseFinder()
    run_app = True

    print("Please enter the Modulo number: ")
    while True:
        try:
            MOD = input()
            if MOD.lower() == 'q' or MOD.lower() == 'quit':
                run_app = False
            else:
                MOD = int(MOD)
            break
        except ValueError: #if input isn't an int
            print("Please try again: ")

    print("Please enter the Integer number: ")
    while True:
        try:
            integer = input()
            if integer.lower() == 'q' or integer.lower() == 'quit':
                run_app = False
            else:
                integer = int(integer)
            break
        except ValueError: #if input isn't an int
            print("Please try again: ")
    if run_app:
        app.run(MOD, integer)
