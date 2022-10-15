number = 7
steps = []
def getGCDEquations(mod, determinant):
    """a = bq + r"""
    dividend = mod
    divisor = determinant
    remainder = divisor #just to start the loop
    
    a = mod
    b = determinant
    step_dict = {}
    step_dict['a'] = a
    while b!=0:
        
        #a is the dividend, b = remainder and divisor
        temp_b = b
        q = a // b
        b = a % b

        a = temp_b

        step_dict = {'a': a, 'b': temp_b, 'q':q, 'r':b}

        steps.append(step_dict)
    '''

    step_dict = {}
    while remainder != 0:
        step_dict['a'] = dividend
        previous_remainder = remainder
        
        #quotient = dividend // divisor
        remainder = dividend % previous_remainder
        step_dict['b'] = previous_remainder
        step_dict['r'] = remainder

        dividend = previous_remainder

        steps.append(step_dict)
    '''
        
