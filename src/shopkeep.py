from textx import metamodel_from_file

shopkeep_mm = metamodel_from_file('shopkeep.tx')
shopkeep_m = shopkeep_mm.model_from_file('main.shopkeep')

progState = {}
progCounter = 0

def varmap(var, state):
    for x in state:
        if x == var:
            return state.get(var)

def math(operands, operator):
    if operator == '+':
        if isinstance(operands[0],str) and not(isinstance(operands[1],str)):
            return varmap(operands[0],progState) + operands[1]
        elif isinstance(operands[1],str) and not(isinstance(operands[0],str)):
            return operands[0] + varmap(operands[1],progState)
        elif isinstance(operands[0],str) and isinstance(operands[1],str):
            return varmap(operands[0],progState) + varmap(operands[1],progState)
        else:
            return operands[0] + operands[1]
    elif operator == '-':
        if isinstance(operands[0],str) and not(isinstance(operands[1],str)):
            return varmap(operands[0],progState) - operands[1]
        elif isinstance(operands[1],str) and not(isinstance(operands[0],str)):
            return operands[0] - varmap(operands[1],progState)
        elif isinstance(operands[0],str) and isinstance(operands[1],str):
            return varmap(operands[0],progState) - varmap(operands[1],progState)
        else:
            return operands[0] - operands[1]
    elif operator == '*':
        if isinstance(operands[0],str) and not(isinstance(operands[1],str)):
            return varmap(operands[0],progState) * operands[1]
        elif isinstance(operands[1],str) and not(isinstance(operands[0],str)):
            return operands[0] * varmap(operands[1],progState)
        elif isinstance(operands[0],str) and isinstance(operands[1],str):
            return varmap(operands[0],progState) * varmap(operands[1],progState)
        else:
            return operands[0] * operands[1]
    elif operator == '/':
        if isinstance(operands[0],str) and not(isinstance(operands[1],str)):
            return varmap(operands[0],progState) / operands[1]
        elif isinstance(operands[1],str) and not(isinstance(operands[0],str)):
            return operands[0] / varmap(operands[1],progState)
        elif isinstance(operands[0],str) and isinstance(operands[1],str):
            return varmap(operands[0],progState) / varmap(operands[1],progState)
        else:
            return operands[0] / operands[1]
    elif operator == '%':
        if isinstance(operands[0],str) and not(isinstance(operands[1],str)):
            return varmap(operands[0],progState) % operands[1]
        elif isinstance(operands[1],str) and not(isinstance(operands[0],str)):
            return operands[0] % varmap(operands[1],progState)
        elif isinstance(operands[0],str) and isinstance(operands[1],str):
            return varmap(operands[0],progState) % varmap(operands[1],progState)
        else:
            return operands[0] % operands[1]        
    if len(operands) == 1:
        if isinstance(operands[0], str):
            return varmap(operands[0],progState)
        return operands[0]

def ifMethod(var, compOps, compOpd):
    match compOps:
        case 'gthan':
            if(var > compOpd):
                return True
            else: return False
        case 'lthan':
            if(var < compOpd):
                return True
            else: return False
        case 'geq':
            if(var >= compOpd):
                return True
            else: return False
        case 'leq':
            if(var <= compOpd):
                return True
            else: return False
        case 'eq':
            if(var == compOpd):
                return True
            else: return False  
        case 'neq':
            if(var != compOpd):
                return True
            else: return False

def interpret(shopkeep_m):
    for i in shopkeep_m.stmts:
        match i.__class__.__name__:
            case 'AssignmentStatement':
                var= i.var
                val = i.val
                progState[var]=val
            case 'UpdateStatement':
                val = math(i.expr.opd, i.expr.ops)
                var = i.var
                progState[var]=val
            case 'PrintStatement':
                print(varmap(i.var,progState))
            case 'IfStatement':
                comparing = varmap(i.var,progState)
                compOps = i.compOps
                if isinstance(i.compOpd, str):
                    compOpd = varmap(i.compOpd,progState)
                else:
                    compOpd = float(i.compOpd)
                flag = ifMethod(comparing, compOps, compOpd)
                if flag:
                    interpret(i)
                elif not flag:
                    try:
                        interpret(i.els[0])
                    except:
                        continue
            case 'WhileStatement':
                comparing = varmap(i.var, progState)
                compOps = i.compOps
                compOpd = float(i.compOpd)
                flag = ifMethod(comparing, compOps, compOpd)
                while flag:
                    interpret(i)
                    flag = ifMethod(varmap(i.var,progState), compOps,compOpd)

#print(shopkeep_m.stmts)
interpret(shopkeep_m)
