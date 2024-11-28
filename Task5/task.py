import pandas as pd
import json 
import numpy as np

def create_pair_matrix(mas):
    elems = []
    for el in mas:
        if type(el) != list:
            elems.append(el)
        else:
            for mel in el:
                elems.append(mel)
    ids = {}
    for i, el in enumerate(elems):
        ids[el] = i
    mat = pd.DataFrame(index=np.arange(1, len(elems) + 1), columns=np.arange(1, len(elems) + 1))
    mat.loc[:, :] = 0
    for el in mas:
        if type(el) != list:
            mat.loc[el, elems[ids[el]:]] = 1
        else:
            for mel in el:
                mat.loc[mel, elems[ids[mel]:]] = 1
                mat.loc[mel, el] = 1
    
    return mat

def find_contr(ab_mat):
    ans = []
    for i, el in enumerate(ab_mat.columns):
        if ab_mat[el].sum() == el:
            ans.append(el)
        else:
            prot = []
            prot.append(el)
            for si, s in enumerate(ab_mat[el]):
                sid = si + 1
                if sid < el:
                    if s == 0:
                        prot.append(sid)
                        if sid in ans:
                            ans.remove(sid)
            ans.append(sorted(prot))
    return ans

def get_kernels_contr(ans):
    kernels = []
    for el in ans:
        if type(el) == list:
            kernels.append(el)
    return kernels

def main():
    # with open('Ранжировка  A.json', 'r') as file:
    a = [1,[2,3],4,[5,6,7],8,9,10]

   # with open('Ранжировка  B.json', 'r') as file:
    b = [[1,2],[3,4,5],6,7,9,[8,10]]

    #with open('Согласованная кластерная ранжировка AB.json', 'r') as file:
    ab = [3,[1,4],2,6,[5,7,8],[9,10]]

    #with open('Ядро противоречий AB.json', 'r') as file:
    pab = [[8,9]]

    a_mat = create_pair_matrix(a)
    b_mat = create_pair_matrix(b)
    ab_mat = np.multiply(a_mat, b_mat)
    ans = find_contr(ab_mat)
    kernel = get_kernels_contr(ans)
    kernel_json = json.dumps(kernel)
    # print(kernel_json)
    return kernel_json
    # print()
    # print(f"Согласованная кластерная ранжировка {ans}")
    # print(f"Ядро противоречий {kernel}")
    # assert ans == ab, "Согласованная ранжировка неверная"
    # assert kernel == pab, "Ядро противоречий неверное"

# if __name__ == '__main__':
#     main()