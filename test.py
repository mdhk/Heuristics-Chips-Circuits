import numpy as np

y_data = [ 
     [[a,0],[b,1],[c,None],[d,6],[e,7]],
     [[a,5],[b,2],[c,1],[d,None],[e,1]],
     [[a,3],[b,None],[c,4],[d,9],[e,None]],
     ]

x_data = [0, 1, 2, 3, 4]

for i in range(5):
    xv = []
    yv = []
    for j, v in enumerate(row[i][1] for row in y_data):
        if v is not None:
            xv.append(j)
            yv.append(v)
    ax.plot(xv, yv, label=y_data[0][i][0])