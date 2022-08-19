# BCH(15,7) encode and decode
import numpy as np

G = np.array([[1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0,],
              [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0,],
              [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0,],
              [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1,],
              [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0,],
              [0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1,],
              [0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1,]]).T


H = np.array([[1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1,],
              [0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0,],
              [0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0,],
              [1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 0, 0,],
              [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1,],
              [1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0,],
              [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0,],
              [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0,]])

def bchEncode(M):
    """
        Returns the encoded form of M
    """
    assert G.shape[1] == M.shape[0], f"the format of M is wrong: M.shape is {M.shape}"
    return G @ M % 2

def bchDecode(C_hat):
    """
        check and correct C_hat
            Returns True if the corrected C_hat is correct, otherwise returns False
    """
    assert H.shape[1] == C_hat.shape[0], f"the format of C_hat is wrong: C_hat.shape is {C_hat.shape}"
    # check matrix S: (8, )
    S = H @ C_hat % 2
    # check if S is all 0, meaning C_hat is correct
    arr = [a != 0 for a in S]
    if sum(arr) == 0:
        return True
    # check if C_hat has one bit error, which can be repaired
    for i in range(H.shape[1]):
        tmp = [a ^ b for (a, b) in zip(H[:, i], S)]
        if sum(tmp) == 0:
            C_hat[i] = 1 - C_hat[i]
            return True
    # check if C_hat has two bit error, which can be repaired
    n = H.shape[1]
    for i in range(n):
        for j in range(n):
            if i != j:
                c = [a ^ b for (a, b) in zip(H[:, i], H[:, j])]
                tmp = [a ^ b for (a, b) in zip(c, S)]
                if sum(tmp) == 0:
                    C_hat[i], C_hat[j] = 1 - C_hat[i], 1 - C_hat[j]
                    return True
    # check if C_hat has more than two bit error, which can't be repaired
    return False