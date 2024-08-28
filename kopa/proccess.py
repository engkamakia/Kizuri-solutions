PROCCESSING_FEE_PERCENTAGE = 3




def proccess_fee_calculation(amount):
    fee = int(amount) * (PROCCESSING_FEE_PERCENTAGE/100)
    return fee
    