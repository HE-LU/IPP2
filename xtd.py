#!/usr/bin/env python

#XTD:xherma25

#------------------- MODULES -------------------
import re, sys, string, os
import argparse
import xml.etree.ElementTree as ET
#------------------- MODULES -------------------

#------------------- GLOBALS -------------------
type_values_table = {"NONE":0, "BIT":1, "INT":2, "FLOAT":3, "NTEXT":4, "NVARCHAR":4}
parsed_tree = {}
counter_list = {}
args = '';
#------------------- GLOBALS -------------------

#------------------- get_type -------------------
def get_type(actual_type, text, attrib):
  
  new_type = "NONE"
  if text == 0 or text == 1 or text == "true" or text == "false":
    new_type = "BIT"
  elif is_int(text):
    new_type = "INT"
  elif is_float(text):
    new_type = "FLOAT"
  else:
    new_type = "NTEXT"
  
  if attrib and new_type == "NTEXT":
    new_type = "NVARCHAR"
  
  if text == "":
    new_type = "INT"
  
  if type_values_table[new_type] < type_values_table[actual_type]:
    new_type = actual_type
    
  return new_type

def is_int(string):
  try:
    int(string)
    return True
  except ValueError:
    return False
    
def is_float(string):
  try:
    float(string)
    return True
  except ValueError:
    return False
#------------------- get_type -------------------

#------------------ PARSE_XML -------------------

def make_etc_elements(root, child):
  for i in range(1, int(args.etc)):
    del parsed_tree[root][child+str(i)+"_id"]
  
  if int(args.etc) == 1:
    del parsed_tree[root][child+"1_id"]
    
  if not parsed_tree.has_key(child):
    parsed_tree[child]={}
  
  parsed_tree[child][root+"_id"] = "INT" 
  counter_list[root][child] = -1
  
  return

def parse_xml(root):
  # -------------------- Create new {} in parsed_tree
  if not parsed_tree.has_key(root.tag):
    parsed_tree[root.tag]={}
  
  # -------------------- Create new {} in counter_list
  if not counter_list.has_key(root.tag):
    counter_list[root.tag]={}
  
  have_childs = 0
  # -------------------- loop for each child in root
  for child in root:
    have_childs = 1
    
    # ------------------- if new value!
    if child not in parsed_tree[root.tag]:
      if child.tag in counter_list[root.tag]:      
        # ---------------- if more than one of same name, count it!
        
        if counter_list[root.tag][child.tag] != -1:
          if counter_list[root.tag][child.tag] == 1:
            parsed_tree[root.tag][child.tag+'1' + "_id"] = parsed_tree[root.tag].pop(child.tag+"_id")
          
          counter_list[root.tag][child.tag] = counter_list[root.tag][child.tag]+1
          if counter_list[root.tag][child.tag] >= int(args.etc):
            make_etc_elements(root.tag, child.tag)
          else:
            pom_child = child.tag + str(counter_list[root.tag][child.tag]) + "_id"      
            parsed_tree[root.tag][pom_child] = "INT"
      else:
        pom_child = child.tag + "_id"
        counter_list[root.tag][child.tag] = 1     
        parsed_tree[root.tag][pom_child] = "INT"
        
      # ---------------- add attributes if set!
      if not args.a:
        for atr,atr_val in root.items():
          parsed_tree[root.tag][atr] = get_type("NONE", atr_val, 1) # Numba one for attribute!
          
    # ------------------- if existing value found, update!
    else:
      print("UPDATE?")
      actual_type = parsed_tree[root.tag][pom_child]
      parsed_tree[root.tag][pom_child] = get_type(actual_type, child.text, 0) # 0 cuz not attribute
      # ---------------- update attributes if set!
      if not args.a:
        for atr,atr_val in root.items():
          actual_type = parsed_tree[root.tag][atr]
          parsed_tree[root.tag][atr] = get_type(actual_type, atr_val, 1) # Numba one for attribute!

  # ------------------- if root element have no chield!
  if not have_childs:
    pom_child = "value"
    # ------------------- should we do update?!
    if root not in parsed_tree[root.tag]:
      parsed_tree[root.tag][pom_child] = get_type("NONE", root.text, 0) # 0 cuz not attribute
    else:
      actual_type = parsed_tree[root.tag][pom_child]
      parsed_tree[root.tag][pom_child] = get_type(actual_type, root.text, 0) # 0 cuz not attribute
    
    # ---------------- do attributes if set!
    if not args.a:
      for atr in root.attrib:
        # ---------------- update attributes if set!
        if atr not in parsed_tree[root.tag]:
          parsed_tree[root.tag][atr] = get_type("NONE", atr, 1) # Numba one for attribute!
        else:
          actual_type = parsed_tree[root.tag][atr]
          parsed_tree[root.tag][atr] = get_type(actual_type, atr, 1) # Numba one for attribute!

  # ------------------ recursive call for all elements
  for child in root:
    parse_xml(child)   
  
  # ------------------ remove root element after each recursive call
  del counter_list[root.tag]
  
  return
#------------------ PARSE_XML -------------------

#--------------------- MAIN --------------------
if __name__ == '__main__':
  #------------------------
  #+++++++++++++ ARGS ++++++++++++
  #------------------------
  parser = argparse.ArgumentParser(description='XML2DDL by XHERMA25')         
  parser.add_argument('--input', dest='input', default=sys.stdin, help='Input file with xml')
  parser.add_argument('--output', dest='output', default=sys.stdout, help='Output file with xml')
  parser.add_argument('--header', dest='header', default="", help='Header included on the top of the output')
  parser.add_argument('--etc', dest='etc', default=-1, help='Maximal number of columns from the same element type')
  parser.add_argument('-a', dest='a', default=0, help='Columns from attributes is not created')
  parser.add_argument('-b', dest='b', default=0, help='More same elements seem like one')
  parser.add_argument('-g', dest='g', default=0, help='XML with relations are on the output')
                    
  args = parser.parse_args()
  #if args.g!=0 or args.b!=0 or args.a!=0 or args.etc!=-1 or args.header!="":
    #if args.h == 1:
      #print("nepouzivej nic s napovedou vole")
      #sys.exit(90)
  
  if not is_int(args.etc):
    print("ETC is not a number!")
    sys.exit(90)
  
  #------------------------
  #---------- ARGS ---------
  #------------------------
  
  #------------------------
  #+++++++++++++ XML +++++++++++++
  #------------------------
  
  tree = ET.parse(args.input)
  root = tree.getroot()

  print("\n")
  
  if root.tag != "catalog":
    print("Nespravne XML!")
    sys.exit(90)
    
  print("Ok lets parse it!")  
  for child in root:
    parse_xml(child)
  
  print("");
  print("");
  for key, value in parsed_tree.items():
    for key2, value2 in parsed_tree[key].items():
      print("["+key+"] - ["+key2+"]\t-\t["+value2+"]")
  
  #------------------------
  #---------- XML ----------
  #------------------------
  
#--------------------- MAIN --------------------
