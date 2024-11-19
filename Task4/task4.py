import pandas as pd
import numpy as np
#A - значение суммы чисел на гранях игральных костей
# B - произведение числе на гранях игральных костей
# a.	H(AB) - энтропия двух связанных (совместных) событий;
# b.	H(A) - энтропия события А;
# c.	H(B) - энтропия события B;
# d.	Ha(B) - условная энтропия события B связанного с событием A;
# e.	I(A,B) - информация в событии A о событии B.
def generate_data():
    data = {}
    sums = set()
    prods = set()
    for i in range(1, 7):
        for j in range(1, 7):
            sum = i + j
            prod = i*j
            if sum not in data.keys():
                data[sum] = []
            
            data[sum].append(prod)
            sums.add(sum)
            prods.add(prod)
    df = pd.DataFrame(index=list(sums), columns=list(prods))
    df = df.fillna(0)
    for i in range(1, 7):
        for j in range(1, 7):
            sum = i + j
            prod = i*j
            df.loc[sum, prod] += 1
    return df

#Вероятность совместного события
def pxy(df):
    pdf = df.copy()
    #print(pdf)
    summ = np.sum([pdf[col].sum() for col in pdf.columns])
    for col in pdf.columns:

        pdf[col] = (df[col]/summ).astype(float)
    return pdf
#Совместная энтропия
def hxy(pdf):
    hdf = pdf.copy()
    hdf = hdf.apply(lambda x: -x*np.log2(x))
    entr = hdf.sum().sum()
    return entr
#Энтропия X
def hx(pdf):
    sdf = pdf.sum(axis = 0)
    return sdf.apply(lambda x: -x*np.log2(x)).sum()
#Энтропия Y
def hy(pdf):
    sdf = pdf.sum(axis = 1)
    return sdf.apply(lambda x: -x*np.log2(x)).sum()
#Условная вероятноть 
def px_y(pdf):
    sdf = pdf.sum(axis = 1)
    sdf.reset_index(inplace = True, drop = True)
    pdf2 = pdf.copy()
    for i, col in enumerate(pdf2.columns):
        for j, row in enumerate(pdf2.index):
            pdf2.loc[row, col] = pdf2.loc[row, col]/sdf.iloc[j]
    return pdf2
#Условная энтропия
def hx_y(pdf, px_y_df):
    return (pdf.sum(axis = 1)*px_y_df.apply(lambda x: -x*np.log2(x)).sum(axis=1)).sum()
#Информация
def inf_gain(entr_x, h_x_y):
    return entr_x - h_x_y


def execute():
    df = generate_data()
    pdf = pxy(df)
    hxay = hxy(pdf)
    entr_x = hx(pdf)
    entr_y = hy(pdf)
    px_y_df = px_y(pdf)
    h_x_y = hx_y(pdf, px_y_df)
    inf = inf_gain(entr_x, h_x_y)
    return [hxay, entr_y, entr_x, h_x_y, inf]


print(execute())
