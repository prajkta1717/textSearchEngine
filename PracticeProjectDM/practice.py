from urllib.request import urlopen
import pandas as pd
data = pd.read_csv("CAvideos.csv")

column1 =['thumbnail_link']
df2 = pd.DataFrame(data, columns=column1)
a = df2.values.tolist()
temp = 2;
print(len(a))
top = []
for i in range(0, len(a)):
    top = a[0:]
#print(top)
for i in top:
    try:
        split_arr = str(i).split('/')
        split_arr2 = split_arr[len(split_arr) - 2]
        f = open('images' + '/' + split_arr2, 'wb')
        f.write(urlopen(i[0]).read())
        f.close()
    except:
        continue