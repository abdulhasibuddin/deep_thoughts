N = 80
K = [4]  #,3,4,5] #,2,3,4,5] #,4] #,3] #,4,5,6,7,8] #,9,10]
H = [1,2,3,4,5,6,7,8]  #,32,128,512] 1,2,3,4,5,6,7,
max_l = 20
max_d = 10
max_r = 80

import itertools
import numpy
import random
from sklearn.neural_network import MLPClassifier

results = []

print("max_l: "+str(max_l)+", max_d: "+str(max_d)+", max_r: "+str(max_r)+", N: ",str(N))

print

print("n","k","h","successful classifications", "rate")
for k in K:
    numpy.random.seed(0)
    # print data
    for h in H:
        max_iter = 1
        numpy.random.seed(0)
        for n in range(N):
            n += 1
            if n < h*(k) and k>1:
              continue
            data_results = []
            l_len = min(n-1,max_l-1)
            for r_data in range(max_d):
                numpy.random.seed(r_data)
                data = numpy.random.normal(size=[N,k])
                numpy.random.seed(0)
                true_results = 0
                for label_int in range(2**l_len):
                    if max_l < n:
                      label_int = random.randint(0, 2**(n-1))
                    labels = [int(i) for i in bin(label_int * 2 + 2**(N+2))[-n:]]
                    d = data[:n]
                    converged = False
                    for r_mlp in range(max_r):  #lbfgs
                        clf = MLPClassifier(
                            hidden_layer_sizes=(h,), random_state=r_mlp, 
                            #activation='relu', solver="lbfgs",
                            activation='relu', solver="lbfgs",
                            alpha=0)
                        clf.fit(d, labels)
                        if (clf.predict(d) == labels).all():
                            true_results += 1
                            converged = True
                            if r_mlp > max_iter:
                              max_iter = r_mlp
                              print "new iteration record: " + str(max_iter)
                            break
                    if not converged:
                      break
                if data_results and true_results > max(data_results):
                    print(n, k, h, true_results, true_results*1.0/2**l_len, "intermediate", r_data, max(data_results)*1.0/2**l_len)
                data_results.append(true_results)
                if true_results == 2**l_len:
                    if len(data_results) > 1:
                      print(n, k, h, true_results, true_results*1.0/2**l_len, "intermediate", r_data, max(data_results)*1.0/2**l_len)
                    break
            true_results = max(data_results)
            print(n, k, h, true_results, true_results*1.0/2**l_len)
            results.append((n, k, h, true_results, true_results*1.0/2**l_len))
            if true_results*1.0/2**l_len < 0.95:
                print "KVC(0.95): "+str((n-1,k, h))
                print
                break
    print "done"