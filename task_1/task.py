import csv
import sys
import json
'''
Код, получающий на вход граф в виде json, значение элемента, и возвращающая родителя и соседей данного элемента.
# {
#     "1": {
#         "2": {
#             "3": {
#                 "5": {},
#                 "6": {}
#             },
#             "4": {
#                 "7": {},
#                 "8": {}

#             }
#         }
#     }
# }
'''
t = {"1": {"2": {"3": {"5": {}, "6": {}}, "4": {"7": {}, "8": {}}}}}
def rec(d, val, prev):
    k = d.keys()
    for key in k:
        if d[key] is None:
            break 
        if key == val:
             sosed = list(k).copy()
             sosed.remove(val)
             print(f"Соседи элемента: {sosed}")
             print(f"Предок элемента: {prev}")
             break
        else: 
            rec(d[key], val, key)
            
def main():
    # file_path = sys.argv[1]
    # # file_path = 'tree.json'
    # val = int(sys.argv[2])
    # # val = "4"
    # with open(file_path, 'r') as f:
    #     t = json.load(f)
    val = 4
    t = {"1": {"2": {"3": {"5": {}, "6": {}}, "4": {"7": {}, "8": {}}}}}
    print(rec(t, val, None))
            