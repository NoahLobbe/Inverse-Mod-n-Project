"""
ModInverseFinder version 1.5
"""

from lib.equations import Equation
from lib.gui import GUI
  

DEV_MODE = False 
GUI_DEV_OUTPUT = False

class ModInverseFinder:
    """class for finding inverse mod-n numbers"""

    def __init__(self):
        """"""

        self.equation_steps_dict = {} #keeps track of the steps

        self.UserInterface = GUI("Mod-n Inverse Finder", DEV_MODE, GUI_DEV_OUTPUT)
        self.UserInterface.run_btn['command'] = self.run
        

        self.UserInterface.root.mainloop()


    def devOutput(self, *args):
        if DEV_MODE:
            str_output = ""
            for arg in args:
                str_output += str(arg)

            print(str_output)

        if GUI_DEV_OUTPUT:
            self.UserInterface.devTextOutput(args)
            

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
        
        if integer % 2 == 0:
            self.devOutput("integer is divisible by 2, and therefore there is no inverse")
            return False, None

        elif integer % 13 == 0:
            self.devOutput("integer is divisible by 13, and therefore there is no inverse")
            return False, None

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
                    self.devOutput((len(MasterEquation.RHS_dict) == 2) and is_mod_num_in_master_equation)
                    self.UserInterface.output_lbl['text'] = "error"
                    return False, None

            else:
                self.devOutput(is_good_for_mod_inverses)
                return False, None

            

    def run(self):
        self.equation_steps_dict.clear() #reset
        
        mod_num = self.UserInterface.getIntInput(self.UserInterface.mod_input_entry)#int(input("Enter Modulo-n value: "))
        integer = self.UserInterface.getIntInput(self.UserInterface.int_input_entry)#int(input("Enter determinant value: "))
        self.devOutput("mod_num", mod_num)

        if mod_num and integer: #won't run if .getIntInput() returns Falses
            self.devOutput("running")
            is_successful, result = self.getModReciprocal(mod_num, integer)
            if is_successful:
                self.UserInterface.output_lbl['text'] = f"Inverse of {integer} (mod-{mod_num}) is: {result}"
            else:
                self.UserInterface.output_lbl['text'] = f"Inverse of {integer} (mod-{mod_num}) does not exist"
        else:
            self.devOutput("invalid mod and integer, not running")
    
    
if __name__ == "__main__":
    app = ModInverseFinder()
