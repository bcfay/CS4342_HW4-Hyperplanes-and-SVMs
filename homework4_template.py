from cvxopt import solvers, matrix
import numpy as np
import sklearn.svm


class SVM4342:
    def __init__ (self):
        pass

    # Expects each *row* to be an m-dimensional row vector. X should
    # contain n rows, where n is the number of examples.
    # y should correspondingly be an n-vector of labels (-1 or +1).
    def fit (self, X, y):
        print(X.shape)
        print(y.shape)

        sample_num, data_len = X.shape

        # ones = np.atleast_2d(np.ones(sample_num)).T
        X = self.data4wewights(X)
        bias_data_len = data_len + 1

        # TODO change these -- they should be np.arrays representing matrices or vectors


        G=np.zeros((sample_num,bias_data_len))
        for i in range(bias_data_len):
            print(X[:,i])
            print(np.multiply(X[:,i],-y))
            G[:,i]=np.multiply(X[:,i],-y)#makeynegativebysubtractingfromG
        # G = G.T


        h = np.ones(sample_num) * -1
        P = np.identity(bias_data_len)
        q = np.zeros(bias_data_len)

        # Solve -- if the variables above are defined correctly, you can call this as-is:
        sol = solvers.qp(matrix(P, tc='d'), matrix(q, tc='d'), matrix(G, tc='d'), matrix(h, tc='d'))

        # Fetch the learned hyperplane and bias parameters out of sol['x']
        # To avoid any annoying errors due to broadcasting issues, I recommend
        # that you flatten() the w you retrieve from the solution vector so that
        # it becomes a 1-D np.array.
        flattened_soln = np.array(sol['x']).flatten()
        
        self.w = flattened_soln[:-1]  # TODO change this
        self.b = flattened_soln[-1]  # TODO change this
        zero = 0

    def data4wewights(self, X):
        sample_num, data_len = X.shape
        X = np.hstack((X, np.atleast_2d(np.ones(sample_num)).T))
        return X

    # Given a 2-D matrix of examples X, output a vector of predicted class labels
    def predict (self, x):
        samplenum, data_len_withbias = x.shape
        weights = np.atleast_2d(np.hstack((self.w, self.b))).T
        x = self.data4wewights(x)
        predictions = np.rint(np.dot(x, weights))
        return predictions  # TODO fix

def test1 ():
    # Set up toy problem
    X = np.array([ [1,1], [2,1], [1,2], [2,3], [1,4], [2,4] ])
    y = np.array([-1,-1,-1,1,1,1])

    # Train your model
    svm4342 = SVM4342()
    svm4342.fit(X, y)
    print(svm4342.w, svm4342.b)

    # Compare with sklearn
    svm = sklearn.svm.SVC(kernel='linear', C=1e15)  # 1e15 -- approximate hard-margin
    svm.fit(X, y)
    print(svm.coef_, svm.intercept_)

    our_pred = svm4342.predict(X).T
    print('our_pred', our_pred)
    lib_pred = svm.predict(X)
    print('lib_pred', lib_pred)

    acc = np.mean(our_pred == lib_pred)
    print("Acc={}".format(acc))

def test2 (seed):
    np.random.seed(seed)

    # Generate random data
    X = np.random.rand(20,3)
    # Generate random labels based on a random "ground-truth" hyperplane
    while True:
        w = np.random.rand(3)
        y = 2*(X.dot(w) > 0.5) - 1
        # Keep generating ground-truth hyperplanes until we find one
        # that results in 2 classes
        if len(np.unique(y)) > 1:
            break

    svm4342 = SVM4342()
    svm4342.fit(X, y)

    # Compare with sklearn
    svm = sklearn.svm.SVC(kernel='linear', C=1e15)  # 1e15 -- approximate hard margin
    svm.fit(X, y)
    print("svm coef shape = "); print(svm.coef_.flatten().shape)
    diff = np.linalg.norm(svm.coef_.flatten() - svm4342.w) + np.abs(svm.intercept_ - svm4342.b)
    print(diff)

    acc = np.mean(svm4342.predict(X) == svm.predict(X))
    print("Acc={}".format(acc))

    if acc == 1 and diff < 1e-1:
        print("Passed")

if __name__ == "__main__": 
    test1()
    #for seed in range(5):
    #    test2(seed)
