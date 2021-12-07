'''
simple sample make json from dtsi, dts, device tree
'''

link_file = "dtsi_sample.dtsi"
# link_file = "imx8mm.dtsi"

use_args = 0
if use_args == 1:
    import sys

    # print("Number of arguments:", len(sys.argv), "arguments.")
    # print ('Argument List:', str(sys.argv))

    if len(sys.argv) < 2:
        exit(0)

    link_file = sys.argv[1]
    # print("Link", sys.argv[1])


file1 = open(link_file, 'r')

# Lines = file1.readlines()
Lines = file1.read().splitlines()


scop_level = 0

def get_last_char(line):
    last_char = ""
    
    if(len(line)==0):
        # print("NULL", line)
        return "NULL"
    
    i = 1
    
    try:
        # print("line", line)


        while (len(line)-i)>=0 and last_char != ";" and last_char != "," and last_char != "{" and last_char != "}":
            last_char = line[len(line)-i]
            # print("last_char", last_char)
            i+=1
        
    except Exception as e:
        if scop_level > 0:
            return line
        return "NULL"
        
    # print("text", text)
    # print("last_char", last_char)
    return last_char


'''
a b c
d e f;
-> a b c d e f;
'''
def fix_one_line_format(Lines):
    global scop_level
    New_text = ""
    line_pre = ""
    for line in Lines:
        last_char = get_last_char(line)

        if line.count("{")==line.count("}") and line.count("{")>0 or line.count("}")>1:
            line_split = line.split("}")
            new_line = "\n}".join(line_split)
            New_text += new_line + "\n"
            continue

        if last_char == "{":
            scop_level += 1
        if last_char == "}":
            scop_level -= 1
        if scop_level == 0:
            continue

        if last_char == "NULL":
            continue
        # print("last_char", last_char)

        if get_last_char(line)!=";" and get_last_char(line)!="{":
            line_pre += line
            continue

        all_line = line_pre + line

        # print(all_line)
        New_text += all_line + "\n"
        line_pre = ""

    return New_text
#1. STEP 1
New_text = fix_one_line_format(Lines)
# print(New_text)
New_Lines = New_text.split("\n")
# print(New_Lines)

def get_last_scop_level(line):
    last_char = ""
    
    if(len(line)==0):
        # print("NULL", line)
        return "NULL"
    
    i = 1
    
    try:
        # print("line", line)
        while (len(line)-i)>=0 and last_char != "{" and last_char != "}":
            last_char = line[len(line)-i]
            # print("last_char", last_char)
            i+=1
        
    except Exception as e:
        if scop_level > 0:
            return line
        return "NULL"
        
    # print("text", text)
    # print("last_char", last_char)
    return last_char
scop_level = 0
dtsi_data = {}
num_dict = 0
def create_dict(text_dict, dtsi_data):   
    global scop_level  
    global num_dict 
    while(num_dict<len(text_dict)-1):
        line = text_dict[num_dict]
        line = line.replace("\t", "")
        line = line.replace(";", "")
        line = line.replace("<", "")
        line = line.replace(">", "")
        line = line.replace("\"", "")


        if scop_level>0:
            split_line = line.split("=")
            # print("len(split_line) ", len(split_line))
            if len(split_line) > 1:
                dtsi_data[split_line[0].replace(" ","")] = split_line[1]
        # print(line)
        last_char = get_last_scop_level(line)
        # print("last_char", last_char)
        if last_char == "{":
            # print(line)
            scop_level += 1
            string_key = line.replace("{", "").replace(" ", "")
            dtsi_data[string_key] = {}
            
            num_dict += 1
            create_dict(text_dict, dtsi_data[string_key])
            pass
        if last_char == "}":
            scop_level -= 1
            # print("return")
            return
        
        
        num_dict += 1

#2. STEP 2
create_dict(New_Lines, dtsi_data) 
 
import json 
json_object = json.dumps(dtsi_data, indent = 4) 
# print(json_object)


with open(link_file + '.json', 'w', encoding='utf-8') as f:
    json.dump(dtsi_data, f, ensure_ascii=False, indent=4)

print("save as " + link_file + ".json")


exit(0)

