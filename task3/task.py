import pandas as pd
import numpy as np

t = {
    "1": {
        "2": {
            "3": {
                "5": {},
                "6": {}
            },
            "4": {
                "7": {},
                "8": {}

            }
        }
    }
}

descr =  lambda: print('''\n
r1 - непосредственное управление\n
r2 - непосредственное подчинение\n
r3 - опосредованное управление\n
r4 - опосредованное подчинение\n
r5 - соподчинение\n
''')

def dict_2_df(d):
    tree = []
    first = list(d.keys())[0]
    def rec(k, sub_tree):
        if sub_tree == {}:
            return
        else:
            elems = sub_tree[k]
            for elem in elems:
                tree.append((k, elem))
                rec(elem, elems)
    rec(first, d)
    df = pd.DataFrame(tree, columns=['out', 'in'])
    return df

def r1(val, tree, ans):
    cnt = tree[tree['out'] == val].shape[0]
    ans.loc[val, 'r1'] = cnt
    
def r2(val, tree, ans):
    cnt = tree[tree['in'] == val].shape[0]
    ans.loc[val, 'r2'] = cnt

def r3(val, tree, ans):
    cnt = []
    i = 0
    def rec(val, i):
        if tree[tree['out'] == val].shape[0] == 0:
            return
        else:
            if i != 0:
                cnt.append(tree[tree['out'] == val].shape[0])
            i += 1
            for elem in tree[tree['out'] == val]['in'].values:
                rec(elem, i)

    rec(val, i)

    ans.loc[val, 'r3'] = sum(cnt)

def r4(val, tree, ans):
    cnt = []
    i = 0
    def rec(val, i):
        if tree[tree['in'] == val].shape[0] == 0:
            return
        else:
            if i != 0:
                cnt.append(tree[tree['in'] == val].shape[0])
            i += 1
            for elem in tree[tree['in'] == val]['out'].values:
                rec(elem, i)

    rec(val, i)

    ans.loc[val, 'r4'] = sum(cnt)

def r5(val, tree, ans):
    cnt = 0
    try:
        pred = tree[tree['in'] == val]['out'].values[0]
    except:
        ans.loc[val, 'r5'] = 0
    else:
        for v in tree['in'].values:
            if v != val:
                pred_2 = tree[tree['in'] == v]['out'].values[0]
                if pred_2 == pred:
                    cnt += 1
    ans.loc[val, 'r5'] = cnt

def entropy(df):
    p = df/(df.shape[1]-1)
    ent = 0
    for v in p.columns:
        ids = np.where(p[v] > 0)
        vals = p[v].iloc[ids[0]].values.copy()
        vals = [i*np.log2(i) for i in vals]
        ent += (-np.sum(vals))
    return ent

def main():
    t = {
        "1": {
            "2": {
                "3": {
                    "5": {},
                    "6": {}
                },
                "4": {
                    "7": {},
                    "8": {}

                }
            }
        }
    }
    tree = dict_2_df(t)
    tree['in'] = tree['in'].astype(int)
    tree['out'] = tree['out'].astype(int)
    verts = list(set(list(tree['out'].unique()) + list(tree['in'].unique())))
    ans = pd.DataFrame(index=verts, columns=['r1', 'r2', 'r3', 'r4', 'r5'])

    for val in verts:
        r1(val, tree, ans)
        r2(val, tree, ans)
        r3(val, tree, ans)
        r4(val, tree, ans)
        r5(val, tree, ans)
    
    df = ans.transpose()
    entr = entropy(df)
    return [df, entr]

output = main()
descr()
print()
print(f"Матрица отношений:")
print(output[0])
print()
print("Энтропия:")
print(output[1])