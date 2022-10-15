

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
        #print("eliminated zeros")
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
                print(in_terms_of_var, "already on LHS for", self.str)

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
                        
                #print("DONE: moving in_terms_of_var to LHS")
                #print("old LHS:", self.LHS_dict)
                #print("new LHS:", new_LHS)
                #print("old RHS:", self.RHS_dict)
                #print("new RHS:", new_RHS)

                #update
                self.LHS_dict = new_LHS
                self.RHS_dict = new_RHS

                #print("new LHS:", self.LHS_dict)
                #print("new RHS:", self.RHS_dict)

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
                        
                #print("DONE: moving in_terms_of_var to LHS")
                #print("old LHS:", self.LHS_dict)
                #print("new LHS:", new_LHS)
                #print("old RHS:", self.RHS_dict)
                #print("new RHS:", new_RHS)

                #update
                self.LHS_dict = new_LHS
                self.RHS_dict = new_RHS

                #print("new LHS:", self.LHS_dict)
                #print("new RHS:", self.RHS_dict)
                

        else:
            print("variable not in equation")

        self.str = self.strEqu() #update


    def substitute(self, equToSubIn, var_to_sub_in_by):
        """if equ_1 (this Obj): a = 2b and equ_2 (equToSubIn): c = b + a, then if var_to_sub_in_by = 'b'
        equ_2: b = c - a, then subbed into equ_1, equ_1: a = 2(c - a)
        equ_1 must have 1 term in LHS"""
        
        equToSubIn = equToSubIn
        equToSubIn.rearrange(var_to_sub_in_by)
        #equToSubIn.simplify() distrupts values
        print("equToSubIn:", equToSubIn.str)
        print("target equation:", self.str)

        if equToSubIn.isVarPresent(var_to_sub_in_by) and self.isVarPresent(var_to_sub_in_by):

            if len(self.LHS_dict) > 1:
                print("several terms in LHS of the master equation:", self.str, self)

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

                print("New master equation:", self.str, "\n")

        else:
            print("var_to_sub_in_by:", var_to_sub_in_by, "NOT present in both equations")


        self.str = self.strEqu() #update
          
