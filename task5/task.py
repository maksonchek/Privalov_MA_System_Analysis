import json
import numpy as np
import pandas as pd

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
    
    return np.array(mat)


def get_kernels_contr(matrix_a, matrix_b):
    matrix_a, matrix_b = np.array(matrix_a), np.array(matrix_b)
    combined_matrix = matrix_a * matrix_b
    combined_transpose = matrix_a.T * matrix_b.T
    result_matrix = np.logical_or(combined_matrix, combined_transpose)
    return result_matrix
    #print(result_matrix)


def main():
    # with open('Ранжировка  A.json', 'r') as file:
    a = [1,[2,3],4,[5,6,7],8,9,10]

   # with open('Ранжировка  B.json', 'r') as file:
    b = [[1,2],[3,4,5],6,7,9,[8,10]]
    #b = [1,[2,3],4,[5,6,7],8,9,10]

    #with open('Согласованная кластерная ранжировка AB.json', 'r') as file:
    ab = [3,[1,4],2,6,[5,7,8],[9,10]]

    #with open('Ядро противоречий AB.json', 'r') as file:
    pab = [[8,9]]

    a_mat = create_pair_matrix(a)
    b_mat = create_pair_matrix(b)
    ab_mat = np.multiply(a_mat, b_mat)
    ans = get_kernels_contr(a_mat, b_mat)
    for r in range(len(ans)):
        for c in range(len(ans[r])):
            if ans[r,c] == 0:
                print(f"{r+1}, {c+1}")

    # kernel = get_kernels_contr(ans)
    # kernel_json = json.dumps(kernel)
    # # print(kernel_json)
    return ans

if __name__ == '__main__':
    kernel = main()
    print(kernel)