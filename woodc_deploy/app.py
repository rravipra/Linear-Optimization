import numpy as np
from copy import deepcopy
from math import *
from collections import *
import sys
import streamlit as st
import time
import json


def getDesired(des_dict, Bo="No"):
    if Bo == "No":
        return des_dict
    exis = st.selectbox("Is there existing inventory?", ["Yes", "No"])
    if exis == "Yes":
        for i in des_dict.keys():
            val = st.number_input(
                "How many boards of size %d are in existing inventory: " % i,
                min_value=0,
                step=1,
            )
            des_dict[i] = (des_dict[i] - val) if des_dict[i] >= val else 0
    st.write(des_dict)
    return des_dict


def getMin(des, prov):
    minQua = sum([(k * v) for k, v in des.items()]) / prov
    return dict(minQua)


def expansion(des):
    cutlist = []
    for k, v in des.items():
        cutlist += [k] * v
    return cutlist


def simplify(des, prov):
    for i in des.keys():
        val = prov // i
        des[i] = val if val <= des[i] else des[i]
    return des


def optimization(sols, des, prov):
    des_keys = list(des.keys())
    min_c = []
    for i in range(len(prov)):
        min_c += [prov[i]] * len(sols[i])
    c = np.array(min_c)
    A = [[] for i in range(len(des))]
    for i in range(len(sols)):
        for j in range(len(sols[0])):
            for k in range(len(des)):
                A[k].append(sols[i][j][des_keys[k]])
    B = [((-1) * des[k]) for k in des.keys()]
    print(B)
    pass


def modulize(des, prov1, prov2, res, res_complete):
    if len(des.keys()) == 0:
        return res_complete
    if min(des.keys()) > prov2:
        return res_complete
    des2 = deepcopy(des)
    for i in des.keys():
        des2.pop(i)
        if prov2 % i == 0:
            cnt = prov2 // i
            if cnt > des[i]:
                continue
            res += [i] * cnt
            if sum(res) == prov1:
                res_complete.append(res)
            res = []
        if prov2 >= i:
            cnt = prov2 // i
            if cnt > des[i]:
                cnt = des[i]
            for coun in range(1, cnt + 1):
                remain = prov2 - (coun * i)
                res_min = [i] * coun
                res_complete = modulize(
                    des2, prov1, remain, res + res_min, res_complete
                )
    return res_complete


def generate_cut_list(cut_dict):
    cut_list = []
    for key, value in cut_dict.items():
        for i in range(value):
            cut_list.append(int(key))
    return cut_list


def wood_cutting(cut_list, sheet_size, max_sheets):
    sheets = 0
    rem_sheets = [0] * max_sheets
    cuts_per_sheet = []

    # loops through all cuts
    for i in range(len(cut_list)):
        j = 0

        # Algorithm to find the best sheet to assign the cut
        min_waste = sheet_size + 1
        best_index = 0
        for j in range(sheets):
            if rem_sheets[j] >= cut_list[i] and rem_sheets[j] - cut_list[i] < min_waste:
                best_index = j
                min_waste = rem_sheets[j] - cut_list[i]

        # If no sheet can accommodate the cut, then we create new sheet
        if min_waste == sheet_size + 1:
            rem_sheets[sheets] = sheet_size - cut_list[i]
            cuts_per_sheet.append([cut_list[i]])
            sheets += 1
        # Assign the cut to best sheet
        else:
            rem_sheets[best_index] -= cut_list[i]
            cuts_per_sheet[best_index].append(cut_list[i])

    return (sheets, cuts_per_sheet, rem_sheets[:sheets])


def print_patterns(final):
    fin = []
    di = {}
    for i in final:
        fin.append(dict(Counter(i)))

    counter = Counter(map(lambda d: frozenset(d.items()), fin))

    for k, v in counter.items():
        st.write(str(dict(k)) + " X " + str(v))

    return fin


def usable(waste, cts):
    if 0 in list(waste.keys()):
        waste.pop(0)
    usable_w = dict()
    unusable_w = dict()
    for k in waste.keys():
        if k >= min(cts):
            usable_w[k] = waste[k]
        else:
            unusable_w[k] = waste[k]
    return [usable_w, unusable_w]


def outPrint(final):
    for i in final:
        st.write(Counter(i))
    return


def outComp(final1, final2):
    for i in final1:
        if i not in final2:
            st.write(i)
    for x in final2:
        if x not in final1:
            st.write(x)
    return


def dictComp(dict1, dict2):
    for key in list(dict1.keys()):
        try:
            if dict1[key] < dict2.get(key, 0):
                return -1
        except:
            return -1
    return 1


def dictSub(dict1, dict2):
    dict3 = {key: dict1[key] - dict2.get(key, 0) for key in dict1.keys()}
    return dict3


def mod_key(key, res):
    key_c = []
    for dict_res in res:
        if key in dict_res.keys():
            key_c.append(dict_res)
    return key_c


def list_to_dict(final, target):
    fin = []
    for i in final:
        if sum(i) == target:
            if dict(Counter(i)) not in fin:
                fin.append(dict(Counter(i)))
    return fin


# define your streamlit app


def main():
    st.title("Wood-cutting Patterns")
    start_time = time.time()
    input_dict = st.text_area(
        "Enter a dictionary of the required unique board sizes and their respective quantities: ",
        "",
    )
    sheet_size = st.text_input("Enter the Preprocessed Wood Size: ")

    if input_dict and sheet_size:
        sheet_size = int(sheet_size)
        input_dict = eval(input_dict)
        cuts_dict = input_dict
        cuts = list(cuts_dict.keys())
        des_dict = cuts_dict
        des1 = getDesired(des_dict, Bo="Yes")
        start_time = time.time()
        st.write(f"Quantity of needed boards {des1}")

        if sheet_size <= 1100:
            res = []
            res_c = []
            des2 = deepcopy(des1)
            res_c = modulize(des1, sheet_size, deepcopy(sheet_size), res, res_c)
            res_com = list_to_dict(res_c, sheet_size)

            desired = Counter(des2)
            loop_cnt = 0
            key_l = list(desired.keys())
            rem = []
            used = []
            st.write("Started Cleaning")
            for k in key_l:
                key_vals = mod_key(k, res_com)
                key_vals = sorted(key_vals, key=lambda y: y[k], reverse=True)
                if not key_vals:
                    continue
                while des2[k] > 0 and key_vals:
                    for i in key_vals:
                        if dictComp(des2, i) == -1:
                            rem.append(i)
                        else:
                            des2 = dictSub(des2, i)
                            used.append(i)
                    for i in rem:
                        key_vals.remove(i)
                    rem = []

            key_vals = mod_key(k, res_com)
            st.write(len(used))
            des2 = {x: y for x, y in des2.items() if y != 0}
            st.write(des2)

            improper_cuts = generate_cut_list(des2)
            overall_list = generate_cut_list(des1)
            sum1 = sum(overall_list) / sheet_size
            st.write(f"Sheet Size: {sheet_size}")
            st.write(f"Minimum number of boards possible: {ceil(sum1)}")

            # max number of sheets
            max_sheets = len(overall_list)
            result = wood_cutting(improper_cuts, sheet_size, len(improper_cuts))
            st.write(f"The number of boards utilized: {result[0] + len(used)}")
            st.write(f"The number of boards with perfect cuts: {len(used)}")
            st.write(f"The number of boards with wasteful cuts: {result[0]}")
            st.write("Below are the Cutting Patterns")
            st.write("Cutting patters to get inventory: {size, quantity}")
            st.write("Perfect cuts (no waste)")
            print_patterns(used)
            st.write("Imperfect cuts (some waste)")
            print_patterns(result[1])
            st.write("---------- End of cutting patterns ----------")
            [usable_waste, unsuable_waste] = usable(dict(Counter(result[2])), cuts)
            # st.write(f"Unsuable waste produced: {unsuable_waste}")
            st.write(f"Usable waste produced: {usable_waste}")

            # st.write("--- Execution time %s seconds ---" % (time.time() - start_time))

        elif sheet_size > 1100:
            improper_cuts = generate_cut_list(des1)
            overall_list = generate_cut_list(des1)
            sum1 = sum(overall_list) / sheet_size

            st.write(f"Sheet Size: {sheet_size}")
            st.write(f"Minimum number of boards possible: {ceil(sum1)}")
            # max number of sheets
            max_sheets = len(overall_list)
            result = wood_cutting(improper_cuts, sheet_size, len(improper_cuts))
            st.write(f"The number of boards utilized: {result[0]}")

            st.write("Below are the Cutting Patterns")
            st.write("Cutting patters to get inventory: {size, quantity}")
            print_patterns(result[1])
            st.write("Unknown cuts (potential waste)")
            print_patterns(result[1])
            st.write("---------- End of cutting patterns ----------")
            [usable_waste, unsuable_waste] = usable(dict(Counter(result[2])))
            # st.write(f"Unsuable waste produced: {unsuable_waste}")
            st.write(f"Usable waste produced: {usable_waste}")

            # st.write("--- Execution time %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
