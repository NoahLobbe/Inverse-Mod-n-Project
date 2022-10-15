"""
"""

from lib.equations import Equation
from lib.gui import GUI
  

equation_steps_dict = {}

def step(a,b, counter=''):
    """Returns quotient and remainder formed from a = bq + r, and a message"""
    if b==0:
        return a, 0, "b=0, therefore division by zero prevented" #q, r, msg
    
    quotient = a//b
    remainder = a%b 
    equation_str = f"{a} = {b}*{quotient} + {remainder}"
    
    if a == b*quotient + remainder: #should always be true
        equation_steps_dict[counter] =  Equation({a:1}, {b:quotient, remainder:1})
        equation_steps_dict[counter].rearrange(remainder) #may be affecting answer when determinant=1
        return quotient, remainder, f"Step {counter}: {equation_str} -> {equation_steps_dict[counter].str}"
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
    elif remainder == 1:
        print("GCD is 1") #the inputted 'b' value from the last step:", b)
        return True, 1

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

    

def getModReciprocal(MOD_NUM, determinant):
    """For Modulo-26. Returns a bool and the value."""
    equation_steps_dict.clear() #reset dict
    '''
    if determinant % 2 == 0:
        print("determinant is divisible by 2, and therefore there is no inverse")
        #no inverse, divisble by 2 if there is no remainder
        return False, None

    elif determinant % 13 == 0:
        #no inverse, divisble by 13 if there is no remainder
        return False, None

    else:'''
    if True:
        
        is_good_for_mod_inverses, GCD = getGCD(MOD_NUM, determinant)
        
        if is_good_for_mod_inverses and (GCD == 1): #double check
            print("\nGetting Inverse...\n")
            print(equation_steps_dict)
            
            num_of_steps = len(equation_steps_dict)
            MasterEquation = equation_steps_dict[num_of_steps]
            print(MasterEquation.RHS_dict)

            for step in range(1, num_of_steps): #skips if num_of_steps == 1
                step_num = num_of_steps - step

                print("step:", step, "out of:", num_of_steps, ". step_num:", step_num)
                
                step_to_sub_in = equation_steps_dict[step_num]
                print("step_to_sub_in:", step_to_sub_in.RHS_dict)
                
                #LHS_key = next(iter(step_to_sub_in.LHS_dict)) #grab the singular key
                #print("LHS_key", LHS_key)

                #print("LHS_key exists in Master Equation:", MasterEquation.isVarPresent(LHS_key))
                MasterEquation.substitute(step_to_sub_in)#, LHS_key)
                #print("Master equation:", MasterEquation.str)

            is_mod_num_in_master_equation = (MOD_NUM in MasterEquation.RHS_dict) or (MOD_NUM in MasterEquation.RHS_dict.values())

            if (len(MasterEquation.RHS_dict) == 2) and is_mod_num_in_master_equation: #(MOD_NUM in MasterEquation.RHS_dict):
                #step3.RHS_dict.pop(str(MOD_NUM)) #because any times the Mod is c0

                print("Final equation:", MasterEquation.str)
                print("RHS:", MasterEquation.RHS_dict)
                #MasterEquation.rearrange(26)
                print("value for key=26:", MasterEquation.RHS_dict[26])
                

                inverse = MasterEquation.RHS_dict[determinant]
                print("raw inverse:", inverse)

                if determinant == 1:
                    #for inverse 1 of Mod-n, we can clearly see 1 is the answer
                    #by: mod-n = 1*mod-n + 0
                    #And the initial setup of inverse = 1/determinant
                    inverse = 1
                    print("inverse modulo:", inverse)
                else:

                    while inverse >= MOD_NUM: #e.g. max is 25
                        inverse -= MOD_NUM
                        print("inverse modulo:", inverse)

                    while inverse < 0:
                        inverse += MOD_NUM
                        print("inverse modulo:", inverse)

                print(f"FINAL ANSWER: Inverse Modulo-{MOD_NUM} of {determinant} is {inverse}")


        else:
            print(is_good_for_mod_inverses)

            """
            step1 = Equation({mod_str: 1}, {det_str:3, '5':1})
            step1.rearrange('5')
            
            step2 = Equation({'7': 1}, {'5':1, '2':1})
            step2.rearrange('2')
            
            step3 = Equation({'5': 1}, {'2':2, '1':1})
            step3.rearrange('1')

            step3.substitute(step2, '2')

            step3.substitute(step1, '5')

            print(step3.str)

            if (len(step3.RHS_dict) == 2) and (mod_str in step3.RHS_dict):
                #step3.RHS_dict.pop(str(MOD_NUM)) #because any times the Mod is c0

                print(step3.str)

                inverse = step3.RHS_dict[det_str]

                while inverse >= MOD_NUM:
                    inverse -= MOD_NUM
                    print("inverse Modulo:", inverse)

                while inverse < 0:
                    inverse += MOD_NUM
                    print("inverse Modulo:", inverse)

                print("FINAL ANSWER")
                print(f"Inverse Modulo-{MOD_NUM} of {determinant} is {inverse}")



            """
            """
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

            #
            #next step is sub. r = a - bq into gcd = factor_1(coefficent) - factor_2(coeffienct)
            if steps_list[-2]['r'] == factor_2:

                
            new_factor_1 = steps_list[-2]['a']
            new_coefficient_1 = 1
            new_factor_2 = steps_list[-2]['b'] * -1 #because r = a -bq
            new_coefficient_2 = steps_list[-2]['q']
            #equation_str = f"{GCD} = {factor_1}*{coefficient_1} + {factor_2}*{coefficient_2}"
            """
            

def run():
    
    #UserInterface.run_btn['command'] = lambda: getModReciprocal(mod_num, determinant)
    
    mod_num = UserInterface.getIntInput(UserInterface.mod_input_entry)#int(input("Enter Modulo-n value: "))
    determinant = UserInterface.getIntInput(UserInterface.int_input_entry)#int(input("Enter determinant value: "))
    print("mod_num", mod_num)

    if mod_num and determinant: #won't run if .getIntInput() returns
        print("running")
        getModReciprocal(mod_num, determinant)
    else:
        print("invalid mod and integer, not running")
    
    
if __name__ == "__main__":
    UserInterface = GUI("Mod-n Inverse Finder")
    UserInterface.run_btn['command'] = run
    #UserInterface.root.mainloop()
    #run()
