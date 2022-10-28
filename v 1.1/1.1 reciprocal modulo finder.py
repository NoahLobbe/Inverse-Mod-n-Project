"""
"""

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

    

def getModReciprocal(determinant):
    """For Modulo-26. Returns a bool and the value."""
    '''
    if determinant % 2 == 0:
        #divisble by 2 if there is no remainder
        return False, None

    elif determinant % 13 == 0:
        #divisble by 13 if there is no remainder
        return False, None
    '''
    if True: #commented above out as  checks for 2 and 13 divisibility resulted in incorrect answers (e.g. 4^-1 in mod-27 is 7 and does exist)
        GCD = getGCD(MOD_NUM, determinant)
        if GCD == 1:
            pass #use steps_list to reverse engineer

def run():
    determinant_value = int(input("Enter determinant value: "))

    print(getModReciprocal(determinant_value))
