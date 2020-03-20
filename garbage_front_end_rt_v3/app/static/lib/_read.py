
import os
def readfile(file):
    text = ""
    with open(file,encoding='utf-8') as file:
        for line in file.readlines():
            text+=line
    return text

def read_garbage_info(dir,garbagetype):
    dir = os.path.join(dir,garbagetype)
    describe_file = os.path.join(dir,"describe.txt")
    deal_file = os.path.join(dir,"deal.txt")
    prevent_file = os.path.join(dir,"prevent.txt")
    describe_text = readfile(describe_file)
    deal_text = readfile(deal_file)
    prevent_text = readfile(prevent_file)
    garbageInfo = {"describe":describe_text,"deal":deal_text,"prevent":prevent_text}
    return garbageInfo