#autor: Miroslav Filas
#login: xfilas00



import re
import copy

import xml.etree.ElementTree as ET
import os
import sys

### definicie funkcii

#vrati typ premennej
def return_value_type(val_type = ''):
    #print(val_type)
    if val_type == 'int':
        return 'int'
    elif val_type == 'bool' or val_type == 'true' or val_type == 'false':
        return 'bool'
    elif val_type == None:
        sys.exit(54)
    elif val_type == 'nil':
        return 'nil'
    elif val_type == 'string':
        return 'string'
    else:
        try:
            int(val_type)
            return 'int'
        except Exception as e:
            return 'string'

#DEFVAR [var] funkcia 
def define_variable(arg = {}, GF = {}, TF = {}, frame_stack = []):
    if arg['frame'] == 'GF': #variable je v GF
        if arg['text'] in GF:
            sys.exit(52)
        else:
            GF[arg['text']] = None
    elif arg['frame'] == 'TF': #variable je v TF
        if TF['init'] == False:
            sys.exit(55)
        elif arg['text'] in TF:
            sys.exit(52)
        else:
            TF[arg['text']] = None
    elif arg['frame'] == 'LF': #variable je v LF
        try:
            if arg['text'] in frame_stack[-1]:
               sys.exit(52)
        except Exception as e:
            sys.exit(55) 
        frame_stack[-1][arg['text']] = None

   
#ziskanie hodnoty ulozenej vo variable pre instrukciu interpretu TYPE
def get_var_value_for_type (arg = {}, GF = {}, TF = {}, frame_stack = []):
    if arg['frame'] == 'GF': #variable je v GF
        if arg['text'] not in GF:
            sys.exit(54)
        elif GF[arg['text']] == None:
            return ''
        else:
            return GF[arg['text']]
    elif arg['frame'] == 'TF': #variable je v TF
        if TF['init'] == False:
            sys.exit(55)
        elif arg['text'] not in TF:
            sys.exit(54)
        elif TF[arg['text']] == None:
            return ''
        else:
            return TF[arg['text']]
    elif arg['frame'] == 'LF': #variable je v LF
        try:
            if arg['text'] not in frame_stack[-1]:
               sys.exit(54)
        except Exception as e:
            sys.exit(55) 
        if frame_stack[-1][arg['text']] == None:
            return ''
        else:
            return frame_stack[-1][arg['text']]
    

#ziskanie hodnoty ulozenej vo variable
def get_var_value (arg = {}, GF = {}, TF = {}, frame_stack = []):
    if arg['frame'] == 'GF': #variable je v GF
        if arg['text'] not in GF:
            sys.exit(54)
        elif GF[arg['text']] == None:
            sys.exit(56)
        else:
            return GF[arg['text']]
    elif arg['frame'] == 'TF': #variable je v TF
        if TF['init'] == False:
            sys.exit(55)
        elif arg['text'] not in TF:
            sys.exit(54)
        elif TF[arg['text']] == None:
            sys.exit(56)
        else:
            return TF[arg['text']]
    elif arg['frame'] == 'LF': #variable je v LF
        try:
            if arg['text'] not in frame_stack[-1]:
                sys.exit(54)
        except Exception as e:
            sys.exit(55) 
        if frame_stack[-1][arg['text']] == None:
            sys.exit(56)
        else:
            return frame_stack[-1][arg['text']]
    

#ulozenie hodnoty do variable
def save_var_value (arg = {}, GF = {}, TF = {}, frame_stack = [], save_value = None):
    if arg['frame'] == 'GF': #variable je v GF
        if arg['text'] not in GF:
            sys.exit(54)
        elif save_value == None:
            sys.exit(56)
        else:
            GF[arg['text']] = save_value
    elif arg['frame'] == 'TF': #variable je v TF
        if TF['init'] == False:
            sys.exit(55)
        elif arg['text'] not in TF:
            sys.exit(54)
        elif save_value == None:
            sys.exit(56)
        else:
            TF[arg['text']] = save_value
    elif arg['frame'] == 'LF': #variable je v LF
        try:
            if arg['text'] not in frame_stack[-1]:
               sys.exit(54)
        except Exception as e:
            sys.exit(55) 
        if save_value == None:
            sys.exit(56)
        else:
            frame_stack[-1][arg['text']] = save_value


#kontrola ci instruction order neobsahuje duplicitne alebo zaporne ocislovanie poradia instrukcii
def check_valid_order(loaded_xml = []):
    tmp_list = []
    tmp_set_list = []
    if len(loaded_xml) == 0:
        sys.exit(0)
    for line in loaded_xml: 
        tmp_list.append(line['order'])
    tmp_set_list = sorted(set(tmp_list))
    
    if len(tmp_list) == len(tmp_set_list) and tmp_set_list[0] >= 1:
        pass
    else:
        sys.exit(32)


#kontrola spravnosti opcode, poctu argumentov...
def check_instruction_validity(loaded_xml = [], labels = {}):
    for idx, line in enumerate(loaded_xml):
        if line['opcode'] in ['CREATEFRAME', 'PUSHFRAME', 'POPFRAME', 'RETURN', 'BREAK']:
            if(len(line) != 2):
                sys.exit(32)
            
        elif line['opcode'] in ['DEFVAR', 'POPS']:
            if(len(line) != 3):
                sys.exit(32)
             #check var 
            try:
                var_type = line['arg1']['type']
                var_value = line['arg1']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_variable(var_value, var_type)
            line['arg1']['frame'] = var_value[0:2]
            line['arg1']['text'] = var_value[3:]
        elif line['opcode'] in ['PUSHS', 'WRITE', 'EXIT', 'DPRINT']:
            if(len(line) != 3):
                sys.exit(32)
            try:
                var_type = line['arg1']['type']
                var_value = line['arg1']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_symbol(var_value, var_type)
            if var_type == 'var':
                line['arg1']['frame'] = var_value[0:2]
                line['arg1']['text'] = var_value[3:]

        elif line['opcode'] in ['ADD', 'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'AND', 'OR', 'STRI2INT', 'CONCAT', 'GETCHAR', 'SETCHAR']:
            if(len(line) != 5):
                sys.exit(32)
            try:
                var_type = line['arg1']['type']
                var_value = line['arg1']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_variable(var_value, var_type)
            line['arg1']['frame'] = var_value[0:2]
            line['arg1']['text'] = var_value[3:]

            try:
                var_type = line['arg2']['type']
                var_value = line['arg2']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_symbol(var_value, var_type)
            if var_type == 'var':
                line['arg2']['frame'] = var_value[0:2]
                line['arg2']['text'] = var_value[3:]

            try:
                var_type = line['arg3']['type']
                var_value = line['arg3']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_symbol(var_value, var_type)
            if var_type == 'var':
                line['arg3']['frame'] = var_value[0:2]
                line['arg3']['text'] = var_value[3:]

        elif line['opcode'] in ['READ']:
            if(len(line) != 4):
                sys.exit(32)
            try:
                var_type = line['arg1']['type']
                var_value = line['arg1']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_variable(var_value, var_type)
            line['arg1']['frame'] = var_value[0:2]
            line['arg1']['text'] = var_value[3:]

            try:
                var_type = line['arg2']['type']
                var_value = line['arg2']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_type(var_value, var_type)

        elif line['opcode'] in ['STRLEN', 'TYPE', 'INT2CHAR', 'MOVE', 'NOT']:
            if(len(line) != 4):
                sys.exit(32)
            try:
                var_type = line['arg1']['type']
                var_value = line['arg1']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_variable(var_value, var_type)
            line['arg1']['frame'] = var_value[0:2]
            line['arg1']['text'] = var_value[3:]

            try:
                var_type = line['arg2']['type']
                var_value = line['arg2']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_symbol(var_value, var_type)
            if var_type == 'var':
                line['arg2']['frame'] = var_value[0:2]
                line['arg2']['text'] = var_value[3:]

        elif line['opcode'] in ['LABEL', 'JUMP', 'CALL']:
            if(len(line) != 3):
                sys.exit(32)
            try:
                var_type = line['arg1']['type']
                var_value = line['arg1']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_label(var_value, var_type)
            if line['opcode'] == 'LABEL':
                if var_value in labels:
                    sys.exit(52)
                else:
                    labels[var_value] = idx

        elif line['opcode'] in ['JUMPIFEQ', 'JUMPIFNEQ']:
            if(len(line) != 5):
                sys.exit(32)
            try:
                var_type = line['arg1']['type']
                var_value = line['arg1']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_label(var_value, var_type)

            try:
                var_type = line['arg2']['type']
                var_value = line['arg2']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_symbol(var_value, var_type)
            if var_type == 'var':
                line['arg2']['frame'] = var_value[0:2]
                line['arg2']['text'] = var_value[3:]

            try:
                var_type = line['arg3']['type']
                var_value = line['arg3']['text']          
            except Exception as e:
                sys.exit(32)
            
            check_symbol(var_value, var_type)
            if var_type == 'var':
                line['arg3']['frame'] = var_value[0:2]
                line['arg3']['text'] = var_value[3:]
        else:
            sys.exit(32)

#kontrola spravnosti hodnoty premennej
def check_variable(value, value_type):
    variable_regex = re.compile(r'^(LF|TF|GF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$')
    if value_type == 'var' and variable_regex.match(value):
        pass
    else:
        sys.exit(32)

#kontrola spravnosti hodnoty symbolu
def check_symbol(value, value_type):
    int_regex = re.compile(r'^[+-]?[0-9]+$')
    bool_regex = re.compile(r'^(true|false)$')
    nil_regex = re.compile(r'^nil$')

    if value_type == 'var':
        check_variable(value, value_type)
    elif value_type == 'string':
        check_string(value)
    elif value_type == 'int' and int_regex.match(value):
        pass
    elif value_type == 'bool' and bool_regex.match(value):
        pass
    elif value_type == 'nil' and nil_regex.match(value):
        pass
    else:
        sys.exit(32)

#kontrola spravnosti retazca
def check_string(value):
    slashes = re.findall(r'\\', str(value))
    escapes = re.findall(r'\\[0-9][0-9][0-9]', str(value))
    if len(slashes) == len(escapes):
        pass
        
    else:
        sys.exit(32)

#kontrola spravnosti oznacenia
def check_label(value, value_type):
    label_regex = re.compile(r'^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$')
    if value_type == 'label' and label_regex.match(value):
        pass
    else:
        sys.exit(32)

#kontrola spravnosti typu
def check_type(value, value_type):
    type_regex = re.compile(r'^(int|string|bool)$')
    if value_type == 'type' and type_regex.match(value):
        pass
    else:
        sys.exit(32)

###main program


source_regex = re.compile(r'^--source=.+$')
input_regex = re.compile(r'^--input=.+$')
source_file = ""
input_file = ""

if len(sys.argv) == 2:
    if(sys.argv[1] == "--help"):
        print("pouzitie: python3 interpret.py --source=file alebo --input=file alebo --source=file --input=file")
        sys.exit(0)
    elif (source_regex.match(sys.argv[1])):
        arg, sep, source_file = sys.argv[1].partition('=')
    elif (input_regex.match(sys.argv[1])):
        arg, sep, input_file = sys.argv[1].partition('=')
    else:
        sys.exit(10)
elif len(sys.argv) == 3:
    if(source_regex.match(sys.argv[1]) and input_regex.match(sys.argv[2])):
        arg, sep, source_file = sys.argv[1].partition('=')
        arg, sep, input_file = sys.argv[2].partition('=')
    elif(source_regex.match(sys.argv[2]) and input_regex.match(sys.argv[1])):
        arg, sep, source_file = sys.argv[2].partition('=')
        arg, sep, input_file = sys.argv[1].partition('=')
    else:
        sys.exit(10)
else:
    sys.exit(10)

if not source_file:
    source_file = sys.stdin
if not input_file:
    pass
else: 
    try:
        sys.stdin = open(input_file, 'r')
    except Exception as e:
        sys.exit(11)
#parse xml
try:
    tree = ET.parse(source_file)
except ET.ParseError:
    sys.exit(31) #chybny format xml  
except Exception as e:
    sys.exit(11) #nejde otvorit subor/neexistuje

root = tree.getroot()

if(root.tag != "program" or root.attrib['language'] != "IPPcode21"):
    sys.exit(32)

instructions = []
sorted_instructions = []
for index, instruction in enumerate(root):
    if instruction.tag == "instruction" and 'opcode' in instruction.attrib.keys() and 'order' in instruction.attrib.keys() and len(instruction.attrib) == 2:
        instruction.attrib['opcode'] = instruction.attrib['opcode'].upper() #opcode na uppercase
        instruction.attrib['order'] = int(instruction.attrib['order'])
        instructions.append(instruction.attrib)
        for arg in instruction:
            instructions[index][arg.tag] = arg.attrib
            instructions[index][arg.tag]['text'] = arg.text
    else:
        sys.exit(32)

#kontrola poradia instrukcii
check_valid_order(instructions)

#zoradenie instrukcii vzostupne
sorted_instructions = sorted(instructions, key=lambda k: k['order'])

labels = {}

check_instruction_validity(sorted_instructions, labels)

GF = {}
stack = []
frame_stack = []
TF = {'init': False}
call_stack = []


#for line in sorted_instructions:
i = 0
len_of_instructions = len(sorted_instructions)
while i < len_of_instructions:
    line = sorted_instructions[i]
    save_value = ''
    #print(line)
    if line['opcode'] == 'CREATEFRAME':
        TF.clear()
        TF['init'] = True

    elif line['opcode'] == 'PUSHFRAME':
        if TF['init'] == False:
            sys.exit(55)
        else:
            frame_stack.append(copy.deepcopy(TF))
            TF.clear()
            TF['init'] = False
            
    elif line['opcode'] == 'POPFRAME':
        try:
            TF = copy.deepcopy(frame_stack.pop())
        except Exception as e:
            sys.exit(55)

    elif line['opcode'] == 'DEFVAR':
        define_variable(line['arg1'], GF, TF, frame_stack)

    elif line['opcode'] == 'MOVE':
        if line['arg2']['type'] != 'var':
            save_value = line['arg2']['text']
        else:
            save_value = get_var_value(line['arg2'], GF, TF, frame_stack)
        save_var_value(line['arg1'], GF, TF, frame_stack, save_value)
        #uz netreba, potom vymazat
        #update_variable(line['arg1'], line['arg2'], GF, TF, frame_stack)

    elif line['opcode'] == 'PUSHS':
        if line['arg1']['type'] != 'var':
            save_value = line['arg1']['text']
        else:
            save_value = get_var_value(line['arg1'], GF, TF, frame_stack)
        stack.append(save_value)

    elif line['opcode'] == 'POPS':
        try:
            save_value = stack.pop()
        except Exception as e:
            sys.exit(56)
        save_var_value(line['arg1'], GF, TF, frame_stack, save_value)

    elif line['opcode'] == 'LABEL':
        pass

    elif line['opcode'] == 'JUMP':
        if line['arg1']['text'] not in labels:
            sys.exit(52)
        else:
            i = labels[line['arg1']['text']]
            continue


    elif line['opcode'] in ['JUMPIFNEQ', 'JUMPIFEQ']:
        symb_val1 = ''
        symb_type1 = ''
        symb_val2 = ''
        symb_type2 = ''
        result = 0
        if line['arg1']['text'] not in labels:
            sys.exit(52)

        if line['arg2']['type'] == 'var':
            symb_val1 = get_var_value(line['arg2'], GF, TF, frame_stack)
            symb_type1 = return_value_type(symb_val1)
        else:
            symb_val1 = line['arg2']['text']
            symb_type1 = line['arg2']['type']

        if line['arg3']['type'] == 'var':
            symb_val2 = get_var_value(line['arg3'], GF, TF, frame_stack)
            symb_type2 = return_value_type(symb_val2)
        else:
            symb_val2 = line['arg3']['text']
            symb_type2 = line['arg3']['type']

        #print(symb_type1)
        #print(symb_type2)
        if symb_type1 == 'nil' or symb_type2 == 'nil':
            i = labels[line['arg1']['text']]
            continue   
        elif symb_type1 == symb_type2 and symb_val1 != symb_val2 and line['opcode'] == 'JUMPIFNEQ':
            i = labels[line['arg1']['text']]
            continue 
        elif symb_type1 == symb_type2 and symb_val1 == symb_val2 and line['opcode'] == 'JUMPIFEQ':
            i = labels[line['arg1']['text']]
            continue 
        else:
            pass
            #sys.exit(53)



    elif line['opcode'] == 'EXIT':
        symb = ''
        if line['arg1']['type'] == 'var':
            symb = get_var_value(line['arg1'], GF, TF, frame_stack)
        elif line['arg1']['type'] == 'int':
            symb = line['arg1']['text']
        else:
            sys.exit(53)
        try:
            num = int(symb)
            if 0 <= num <= 49:
                sys.exit(num)
            else:
                sys.exit(57) 
        except Exception as e:
            sys.exit(53)
        
    elif line['opcode'] == 'CALL':
        call_stack.append(i)     
        if line['arg1']['text'] not in labels:
            sys.exit(52)
        else:
            i = labels[line['arg1']['text']]
        continue

    elif line['opcode'] == 'RETURN':
        try:
            i = call_stack.pop()
        except Exception as e:
            sys.exit(56)
        i+=1
        continue

    elif line['opcode'] == 'WRITE':
        #print(line)
        var_to_write = ''
        if line['arg1']['type'] == 'var':
            var_to_write = get_var_value(line['arg1'], GF, TF, frame_stack)
        else:
            var_to_write = line['arg1']['text']    
        if var_to_write == 'nil':
            print('', end='')
        else:
            print(var_to_write, end='')

    elif line['opcode'] == 'DPRINT':
        var_to_write = ''
        if line['arg1']['type'] == 'var':
            var_to_write = get_var_value(line['arg1'], GF, TF, frame_stack)
        else:
            var_to_write = line['arg1']['text']    
        print(var_to_write, file=sys.stderr)

    elif line['opcode'] == 'BREAK':
        print(f'Aktualna pozicia v kode: {i}', file=sys.stderr)
        print(f'Obsah GF {GF}', file=sys.stderr)
        print(f'Obsah TF {TF}', file=sys.stderr)
        if len(frame_stack) >= 1:
            print(f'Obsah LF {frame_stack[-1]}', file=sys.stderr)
        print(f'Obsah instruction stacku: {stack}', file=sys.stderr)
        print(f'Obsah call stacku: {call_stack}', file=sys.stderr)
        print(f'Obsah label listu: {labels}', file=sys.stderr)

    elif line['opcode'] == 'TYPE':
        val_type = ''
        result = ''
        if line['arg2']['type'] != 'var':
            val_type = line['arg2']['type']
        else:
            val_type = get_var_value_for_type(line['arg1'], GF, TF, frame_stack)
        result = return_value_type(val_type)
        save_var_value(line['arg1'], GF, TF, frame_stack, result)    

    elif line['opcode'] == 'READ':
        val_value = 'nil'
        user_input = ''
        try:
            user_input = input()
        except EOFError:
            val_value = 'nil'
        if line['arg2']['text'] == 'bool':
            if user_input.lower() == 'true':
                val_value = 'true'
            else:
                val_value = 'false'
        elif line['arg2']['text'] == 'string':
            val_value = user_input
        elif line['arg2']['text'] == 'int':
            try:
                val_value = str(int(user_input))
            except Exception as e:
                val_value = 'nil'
        save_var_value(line['arg1'], GF, TF, frame_stack, val_value) 

#konverzne instrukcie
    elif line['opcode'] == 'INT2CHAR':
        val_value = ''
        conv = ''
        if line['arg2']['type'] == 'int':
            conv = line['arg2']['text']
        elif line['arg2']['type'] == 'var':
            conv = get_var_value(line['arg2'], GF, TF, frame_stack)
        else:
            sys.exit(53)
        try:
            val_value = chr(int(conv))
        except Exception as e:
            sys.exit(58)
        save_var_value(line['arg1'], GF, TF, frame_stack, val_value)

    elif line['opcode'] == 'STRI2INT':
        val_value = ''
        conv = ''
        position = 0

        if line['arg3']['type'] == 'int':
            position = line['arg2']['text']
        elif line['arg3']['type'] == 'var':
            position = get_var_value(line['arg3'], GF, TF, frame_stack)
        else:
            sys.exit(53)

        if line['arg2']['type'] == 'string':
            conv = line['arg2']['text']
        elif line['arg2']['type'] == 'var':
            conv = get_var_value(line['arg2'], GF, TF, frame_stack)
        else:
            sys.exit(53)

        try:
            val_value = ord(conv[int(position)])
        except Exception as e:
            sys.exit(58)
        save_var_value(line['arg1'], GF, TF, frame_stack, val_value)

#aritmeticke, relacne, booleovske instrukcie
    elif line['opcode'] in ['ADD', 'SUB', 'MUL', 'IDIV']:
        symb_val1 = ''
        symb_val2 = ''
        result = 0
        if line['arg2']['type'] == 'int':
            symb_val1 = line['arg2']['text']
        elif line['arg2']['type'] == 'var':
            symb_val1 = get_var_value(line['arg2'], GF, TF, frame_stack)
        
        else:
            sys.exit(53)

        if line['arg3']['type'] == 'int':
            symb_val2 = line['arg3']['text']
        elif line['arg3']['type'] == 'var':
            symb_val2 = get_var_value(line['arg3'], GF, TF, frame_stack)
        else:
            sys.exit(53)

        try:
            symb_val1 = int(symb_val1)
            symb_val2 = int(symb_val2) 
        except Exception as e:
            sys.exit(53)
        
        if line['opcode'] == 'ADD':
            result = symb_val1 + symb_val2
        elif line['opcode'] == 'SUB':
            result = symb_val1 - symb_val2
        elif line['opcode'] == 'MUL':
            result = symb_val1 + symb_val2
        elif line['opcode'] == 'IDIV':
            try:
                result = symb_val1 // symb_val2
            except Exception as e:
                sys.exit(57)

        save_var_value(line['arg1'], GF, TF, frame_stack, str(result))

    elif line['opcode'] in ['LT', 'GT','EQ']:
        
        symb_val1 = ''
        symb_val2 = ''
        result = 0
        
        if line['arg2']['type'] == 'int':
            symb_val1 = line['arg2']['text']
        elif line['arg2']['type'] == 'var':
            symb_val1 = get_var_value(line['arg2'], GF, TF, frame_stack)
        else:
            symb_val1 = line['arg2']['text']
        
        if line['arg3']['type'] == 'int':
            symb_val2 = line['arg3']['text']
        elif line['arg3']['type'] == 'var':
            symb_val2 = get_var_value(line['arg3'], GF, TF, frame_stack)
        else:
            symb_val2 = line['arg3']['text']    

        if symb_val1 == None:
            symb_val1 = ''
        elif symb_val2 == None:
            symb_val2 =''
        try:
            symb_val1 = int(symb_val1)
        except Exception as e:
            if symb_val1 == 'true':
                symb_val1 = True
            elif symb_val1 == 'false':
                symb_val1 == False

        try:
            symb_val2 = int(symb_val2)
        except Exception as e:
            if symb_val2 == 'true':
                symb_val2 = True
            elif symb_val2 == 'false':
                symb_val2 == False

        if (symb_val1 == 'nil' or symb_val2 == 'nil'):
            if line['opcode'] != 'EQ':
                sys.exit(53)
            else:
                result = symb_val1 == symb_val2
        else:
            typ1 = return_value_type(symb_val1)
            typ2 = return_value_type(symb_val2)
            if typ1 != typ2:
                sys.exit(53)

            if line['opcode'] == 'LT':

                result = symb_val1 < symb_val2
            elif line['opcode'] == 'GT':
                result = symb_val1 > symb_val2
            if line['opcode'] == 'EQ':
                result = symb_val1 == symb_val2
                
        #print(str(result))
        save_var_value(line['arg1'], GF, TF, frame_stack, str(result).lower())

    elif line['opcode'] in ['AND', 'OR','NOT']:
        symb_val1 = ''
        symb_val2 = ''
        result = 0
        if line['arg2']['type'] == 'bool':
            symb_val1 = line['arg2']['text']
        elif line['arg2']['type'] == 'var':
            symb_val1 = get_var_value(line['arg2'], GF, TF, frame_stack)
        else:
            sys.exit(53)

        if symb_val1 == 'true':
            symb_val1 = True
        elif symb_val1 == 'false':
            symb_val1 = False
        else:
            sys.exit(53)

        if line['opcode'] != 'NOT':
            if line['arg3']['type'] == 'bool':
                symb_val2 = line['arg3']['text']
            elif line['arg3']['type'] == 'var':
                symb_val2 = get_var_value(line['arg3'], GF, TF, frame_stack)
            else:
                sys.exit(53) 

            if symb_val2 == 'true':
                symb_val2 = True
            elif symb_val2 == 'false':
                symb_val2 = False
            else:
                sys.exit(53)   

        if line['opcode'] == 'AND':         
            result = symb_val1 and symb_val2
        elif line['opcode'] == 'OR':
            result = symb_val1 or symb_val2
        elif line['opcode'] == 'NOT':
            result = not symb_val1

        save_var_value(line['arg1'], GF, TF, frame_stack, str(result).lower())

    elif line['opcode'] == 'CONCAT':
        symb_val1 = ''
        symb_type1 = ''
        symb_val2 = ''
        symb_type2 = ''
        result = 0

        if line['arg2']['type'] == 'var':
            symb_val1 = get_var_value(line['arg2'], GF, TF, frame_stack)
            symb_type1 = return_value_type(symb_val1)
        else:
            symb_val1 = line['arg2']['text']
            symb_type1 = line['arg2']['type']

        if line['arg3']['type'] == 'var':
            symb_val2 = get_var_value(line['arg3'], GF, TF, frame_stack)
            symb_type2 = return_value_type(symb_val2)
        else:
            symb_val2 = line['arg3']['text']
            symb_type2 = line['arg3']['type']

        if return_value_type( symb_type1) != 'string' or return_value_type( symb_type2 )!= 'string':
            sys.exit(53)
        
        result = symb_val1 + symb_val2
        save_var_value(line['arg1'], GF, TF, frame_stack, result)

    elif line['opcode'] == 'STRLEN':
        symb_val1 = ''
        symb_type1 = ''
        result = 0

        if line['arg2']['type'] == 'var':
            symb_val1 = get_var_value(line['arg2'], GF, TF, frame_stack)
            symb_type1 = return_value_type(symb_val1)
        else:
            symb_val1 = line['arg2']['text']
            symb_type1 = line['arg2']['type']

        if symb_type1 != 'string':
            sys.exit(53)
        if symb_val1 == None:
            symb_val1 = ''
        result = len(symb_val1)  
        save_var_value(line['arg1'], GF, TF, frame_stack, result)

    elif line['opcode'] == 'GETCHAR':
        symb_val1 = ''
        symb_type1 = ''
        symb_val2 = ''
        symb_type2 = ''
        result = 0

        if line['arg2']['type'] == 'var':
            symb_val1 = get_var_value(line['arg2'], GF, TF, frame_stack)
            symb_type1 = return_value_type(symb_val1)
        else:
            symb_val1 = line['arg2']['text']
            symb_type1 = line['arg2']['type']

        if line['arg3']['type'] == 'var':
            symb_val2 = get_var_value(line['arg3'], GF, TF, frame_stack)
            symb_type2 = return_value_type(symb_val2)
        else:
            symb_val2 = line['arg3']['text']
            symb_type2 = line['arg3']['type']

        if symb_type1 != 'string' or symb_type2 != 'int':
            sys.exit(53)
        try:
            if int(symb_val2) < 0:
                sys.exit(58)
            result = symb_val1[int(symb_val2)]
        except Exception as e:
            sys.exit(58)
        save_var_value(line['arg1'], GF, TF, frame_stack, result)

    elif line['opcode'] == 'SETCHAR':
        symb_val1 = ''
        symb_type1 = ''
        symb_val2 = ''
        symb_type2 = ''
        result = get_var_value(line['arg1'], GF, TF, frame_stack)

        if line['arg2']['type'] == 'var':
            symb_val1 = get_var_value(line['arg2'], GF, TF, frame_stack)
            symb_type1 = return_value_type(symb_val1)
        else:
            symb_val1 = line['arg2']['text']
            symb_type1 = line['arg2']['type']

        if line['arg3']['type'] == 'var':
            symb_val2 = get_var_value(line['arg3'], GF, TF, frame_stack)
            symb_type2 = return_value_type(symb_val2)
        else:
            symb_val2 = line['arg3']['text']
            symb_type2 = line['arg3']['type']

        if symb_type1 != 'int' or symb_type2 != 'string':
            sys.exit(53)

        try:
            if int(symb_val1) < 0:
                sys.exit(58)
            result[int(symb_val1)] = symb_val2[0]
        except Exception as e:
            sys.exit(58)

        save_var_value(line['arg1'], GF, TF, frame_stack, result)
        
    i+=1



