#!/usr/bin/env python

#XTD:xherma25

#------------------- MODULES -------------------
import re, sys, string, os
import argparse
import xml.etree.ElementTree as ET
#------------------- MODULES -------------------

#------------------- GLOBALS -------------------
type_values_table = {"NONE":0, "BIT":1, "INT":2, "FLOAT":3, "NVARCHAR":4, "NTEXT":5}
parsed_tree = {}
parsed_g_tree = {}
counter_list = {}
#------------------- GLOBALS -------------------

def clear_white_chars(text):
  if text == None:
    return ""
  tmp = text
  tmp = ''.join(tmp.split())
  return tmp

#------------------- get_type -------------------
def get_type(actual_type, text, attrib):
  
  if text == None:
    return "BIT"
  if clear_white_chars(text) == "":
    return "INT"
  
  #new_type = "NONE"
  new_type = actual_type
  if text == 0 or text == 1 or text == "true" or text == "false"or text == "True" or text == "False":
    new_type = "BIT"
  elif is_int(text):
    new_type = "INT"
  elif is_float(text):
    new_type = "FLOAT"
  else:
    new_type = "NTEXT"
  
  if attrib and new_type == "NTEXT":
    new_type = "NVARCHAR"
  
  #if text == "":
    #new_type = "INT"
  
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



#-------------- MAKE_ETC_ELEMENTS ---------------
def make_etc_elements(root, child):
  del parsed_tree[root][child]
  
  if child not in parsed_tree:
    parsed_tree[child]={}
  
  parsed_tree[child][root] = [1,"INT","_id"] 
  counter_list[root][child] = -1
  return
#-------------- MAKE_ETC_ELEMENTS ---------------

#------------------ FWRITE -------------------
def fwrite(f_out,msg):
  if args.output != sys.stdout:
    f_out.write(msg)
  else:
    sys.stdout.write(msg)
  
  return
#------------------ FWRITE -------------------

#------------------ PARSE_XML -------------------
def parse_xml(root):
  root.tag = root.tag.lower()
  # -------------------- Create new {} in parsed_tree
  if root.tag not in parsed_tree:
    parsed_tree[root.tag]={}
  
  # -------------------- Create new {} in counter_list
  if root.tag not in counter_list:
    counter_list[root.tag]={}
    
  have_childs=0
  
  # ----------------------------------------
  # -------------------- If he have childs!
  # ----------------------------------------
  for child in root:
    have_childs = 1
    if not args.a:
      # -------------------- Now add all these attributes :)!
      for atr,atr_val in root.items():
        atr = atr.lower()
        parsed_tree[root.tag][atr]=[0,"NONE",""]
        parsed_tree[root.tag][atr][0] = 1
        parsed_tree[root.tag][atr][1] = get_type("NONE", atr_val, 1) # Numba one for attribute! Hurray!
        parsed_tree[root.tag][atr][2] = ""
   
    if child.tag+"_id" in parsed_tree[root.tag]:
      print("OMG WTF! NOOOOOOO!")
      sys.exit(90)

    if child.tag not in parsed_tree[root.tag]:
      # -------------------- If child.tag is new.
      if child.tag in counter_list[root.tag]:
        if counter_list[root.tag][child.tag] == -1:
          continue
      counter_list[root.tag][child.tag] = 1     
      parsed_tree[root.tag][child.tag]=[1,"NONE",""]
      parsed_tree[root.tag][child.tag][0] = 1
      parsed_tree[root.tag][child.tag][1] = "INT"
      parsed_tree[root.tag][child.tag][2] = "_id"
    else:
      # -------------------- If child.tag already exist, change number of them!

      #if child.tag in counter_list[root.tag]: 
        #counter_list[root.tag][child.tag] = counter_list[root.tag][child.tag] + 1    
        #parsed_tree[root.tag][child.tag][0] = counter_list[root.tag][child.tag]
      #else:
        #parsed_tree[root.tag][child.tag][0] = 1
        #counter_list[root.tag][child.tag] = 1
        
      if child.tag in counter_list[root.tag]: 
        counter_list[root.tag][child.tag] = counter_list[root.tag][child.tag] + 1    
        if parsed_tree[root.tag][child.tag][0] < counter_list[root.tag][child.tag]:
          parsed_tree[root.tag][child.tag][0] = counter_list[root.tag][child.tag]
      else:
        counter_list[root.tag][child.tag] = 1
      
      parsed_tree[root.tag][child.tag][1] = "INT"
      parsed_tree[root.tag][child.tag][2] = "_id"

    if parsed_tree[root.tag][child.tag][0] > int(args.etc) and args.etc != "-1":
      make_etc_elements(root.tag, child.tag)
  # ----------------------------------------
  # -------------------- If he dont have childs!
  # ----------------------------------------
  if not have_childs:
    #if root.tag not in parsed_tree[root.tag] and clear_white_chars(root.text) != "":
    if clear_white_chars(root.text) != "":
      # -------------------- Create new instance for root.tag, only if its empty!
      parsed_tree[root.tag]["value"]=[1,"NONE",""]
      parsed_tree[root.tag]["value"][0] = 1
      parsed_tree[root.tag]["value"][1] = get_type("NONE", root.text, 0) # 0 cuz not attribute
      parsed_tree[root.tag]["value"][2] = ""
    #else:
      ## -------------------- If root.tag already exist, check his type!
      #parsed_tree[root.tag][root.tag][1] = get_type("NONE", root.text, 0) # 0 cuz not attribute
      #parsed_tree[root.tag][root.tag][2] = "_id"
    if not args.a:
      # -------------------- Now add all these attributes :)!
      for atr,atr_val in root.items():
        atr = atr.lower()
        parsed_tree[root.tag][atr]=[0,"NONE",""]
        parsed_tree[root.tag][atr][0] = 1
        parsed_tree[root.tag][atr][1] = get_type("NONE", atr_val, 1) # Numba one for attribute! Hurray!
        parsed_tree[root.tag][atr][2] = ""
    # nasledujici podminka je uplna blbost...
    #if parsed_tree[root.tag].keys() != ["value"]:
      #del parsed_tree[root.tag]["value"]
    
  # ------------------ recursive call for all elements
  for child in root:
    parse_xml(child) 
  
  # ------------------ remove root element after each recursive call
  del counter_list[root.tag]
  
  return
#------------------ PARSE_XML -------------------

#------------------ PARSE_G_TREE -------------------
def parse_g_tree():
  
  for root in parsed_tree:
    parsed_g_tree[root] = {}
    for child in parsed_tree:
      parsed_g_tree[root][child] = "0:0"
      
  for root in parsed_tree:
    for child in parsed_tree[root]:
      if parsed_tree[root][child][2] == "_id":
        parsed_g_tree[root][child] = "N:1"
        parsed_g_tree[child][root] = "1:N"
        parsed_g_tree[root][root] = "1:1"
        parsed_g_tree[child][child] = "1:1"
  
  change = 1
  while change:
    change = 0
    for root in parsed_g_tree:
      for child in parsed_g_tree[root]:
        if parsed_g_tree[root][child] == "N:1":
          for child2 in parsed_g_tree[child]:
            if parsed_g_tree[child][child2] == "N:1":
              if parsed_g_tree[root][child2] != "N:1":
                parsed_g_tree[root][child2] = "N:1"
                change = 1
  
  change = 1
  while change:
    change = 0
    for root in parsed_g_tree:
      for child in parsed_g_tree[root]:
        if parsed_g_tree[root][child] == "1:N":
          for child2 in parsed_g_tree[child]:
            if parsed_g_tree[child][child2] == "1:N":
              if parsed_g_tree[root][child2] != "1:N":
                parsed_g_tree[root][child2] = "1:N"
                change = 1
  
  for root in parsed_g_tree:
    for child in parsed_g_tree[root]:
      if parsed_g_tree[root][child] == "0:0":
        parsed_g_tree[root][child] = "N:M"
  
  return
#------------------ PARSE_G_TREE -------------------
  
#--------------------- MAIN --------------------
if __name__ == '__main__':
  #------------------------
  #+++++++++++++ ARGS ++++++++++++
  #------------------------
  parser = argparse.ArgumentParser(description='XML2DDL by XHERMA25',add_help=False)         
  parser.add_argument('--input', dest='input', default=sys.stdin, help='Input file with xml')
  parser.add_argument('--output', dest='output', default=sys.stdout, help='Output file with xml')
  parser.add_argument('--header', dest='header', default="", help='Header included on the top of the output')
  parser.add_argument('--etc', dest='etc', default="-1", help='Maximal number of columns from the same element type')
  parser.add_argument('-a', action='store_true', dest='a', default=0, help='Columns from attributes is not created')
  parser.add_argument('-b', action='store_true', dest='b', default=0, help='More same elements seem like one')
  parser.add_argument('-g', action='store_true', dest='g', default=0, help='XML with relations are on the output')
  parser.add_argument('-h', action='store_true', dest='h', default=0, help='Print this help')
  parser.add_argument('--help', action='store_true', dest='h', default=0, help='Print this help')
  
  args = parser.parse_args()
  if args.g!=0 or args.b!=0 or args.a!=0 or args.etc!="-1" or args.header!="" or args.input!=sys.stdin or args.output!=sys.stdout:
    if args.h == 1:
      print("Help with other attributes set! You failed!")
      sys.exit(1)
  
  if args.h == 1:
    parser.print_help()
    sys.exit(0)
  
  if args.b!=0 and args.etc!="-1":
    print("Attribute B set, and etc is set also... I don't like it!")
    sys.exit(1)
  
  if not is_int(args.etc):
    print("ETC is not a number!")
    sys.exit(666)
  
  #------------------------
  #---------- ARGS ---------
  #------------------------
  
  #------------------------
  #+++++++++++++ XML +++++++++++++
  #------------------------
  
  try:
    tree = ET.parse(args.input)
  except:
    print("Spatny vstpnisoubor, nebo se neco posralo")
    sys.exit(2)
  root = tree.getroot()

  print("\n")
  
  if root.tag != "catalog":
    print("Nespravne XML!")
    sys.exit(90)
      
  for child in root:
    parse_xml(child)
    
  #------------------------
  #---------- XML ----------
  #------------------------
  
  if args.output != sys.stdout:
    try:
      f_out = open(args.output,"w")
    except:
      print("ou ou fucking poh!")
      sys.exit(3)
  else:
    f_out = None
  #------------------------
  #++++++++++ Normal Write +++++++++
  #------------------------
  if not args.b and not args.g:
    if args.header!="":
      fwrite(f_out,"--"+args.header+"\n\n")
      
    for key, value in parsed_tree.items():
      fwrite(f_out,"CREATE TABLE "+key+"(\n")
      fwrite(f_out,"\tprk_"+key+"_id INT PRIMARY KEY")
      for key2, value2 in parsed_tree[key].items():     
        if value2[0] <= 1:
          fwrite(f_out,",\n\t")
          fwrite(f_out,key2+value2[2]+" "+value2[1])
        else:
          for i in range(1,value2[0]+1):
            fwrite(f_out,",\n\t")
            fwrite(f_out,key2+str(i)+value2[2]+" "+value2[1])
      fwrite(f_out,"\n);\n\n")
  #------------------------
  #------- Normal Write -------
  #------------------------
  
  #------------------------
  #++++++++++ B Write +++++++++++++
  #------------------------
  if args.b and not args.g:
    if args.header!="":
      fwrite(f_out,"--"+args.header)
    
    for key, value in parsed_tree.items():
      fwrite(f_out,"CREATE TABLE "+key+"(\n")
      fwrite(f_out,"\tprk_"+key+"_id INT PRIMARY KEY")
      for key2, value2 in parsed_tree[key].items():     
        fwrite(f_out,",\n\t")
        fwrite(f_out,key2+value2[2]+" "+value2[1])
      fwrite(f_out,"\n);\n\n")      
  #------------------------
  #-------- B Write ----------
  #------------------------
  
  #------------------------
  #+++++++++++ G Write +++++++++++++
  #------------------------
  if args.g:
    parse_g_tree()
    
    if args.header!="":
      fwrite(f_out,"--"+args.header)
      
    fwrite(f_out,"<tables>")
    fwrite(f_out,"\n")
    for key, value in parsed_g_tree.items():
      fwrite(f_out,"\t<table name=\""+key+"\">\n\t")
      for key2, value2 in parsed_g_tree[key].items():     
        fwrite(f_out,"\t<relation to=\""+key2+"\" relation_type=\""+value2+"\" />\n\t")
      fwrite(f_out,"</table>\n")
    fwrite(f_out,"</tables>\n")  
  #------------------------
  #-------- G Write ----------
  #------------------------
  
  if args.output != sys.stdout:
    f_out.close() 
  
#--------------------- MAIN --------------------
