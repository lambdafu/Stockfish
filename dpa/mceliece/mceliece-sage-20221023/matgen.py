

# This file was *autogenerated* from the file matgen.sage
from sage.all_cmdline import *   # import sage library

_sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_2 = Integer(2)
import echelon
import parameters

def matgen(Gamma,params,check00=True):
  r'''
  Return the output of the Classic McEliece MatGen function
  on input Gamma for the specified parameters.

  The output is either False or (T,...),
  where T is an mt x k matrix over F_2.

  In the case (mu,nu) = (0,0),
  a non-False output (T,...) is (T,Gamma).
  For general (mu,nu),
  a non-False output (T,...) is (T,c[m*t-mu],...,c[m*t-1],Gammaprime),
  where c[...] are integers
  with m*t-mu <= c[m*t-mu] < c[m*t-mu+1] < ... < c[m*t-1] < m*t-mu+nu,
  Gammaprime = (g,alphaprime[0],...,alphaprime[n-1]),
  and alphaprime[0],...,alphaprime[n-1] are distinct elements of F_q.

  INPUT:

  "Gamma" - a tuple (g,alpha[0],...,alpha[n-1])
  where g is a monic irreducible polynomial in F_q[x] of degree t
  and alpha[0],...,alpha[n-1] are distinct elements of F_q

  "params" - a Classic McEliece parameter set

  "check00" (optional, default True) -
  if True, use simpler algorithm in the case (mu,nu) = (0,0);
  this has no effect for other (mu,nu)
  '''
  assert isinstance(params,parameters.parameters)
  m = params.m
  n = params.n
  t = params.t
  k = params.k
  Fq = params.Fq
  mu = params.mu
  nu = params.nu

  Gamma = tuple(Gamma)
  assert len(Gamma) == n+_sage_const_1 
  g,alpha = Gamma[_sage_const_0 ],Gamma[_sage_const_1 :]
  assert all(alphaj in Fq for alphaj in alpha)
  assert len(set(alpha)) == n
  assert g.base_ring() == Fq
  assert g.is_monic()
  assert g.is_irreducible()
  assert g.degree() == t

  # "Compute the t x n matrix Htilde = {h_{i,j}} over F_q,
  #  where h_{i,j} = alpha_j^i/g(alpha_j)
  #  for i = 0,...,t-1 and j = 0,...,n-1."
  # (same for the (0,0) case and the general case)
  overgalpha = [_sage_const_1 /g(alpha[j]) for j in range(n)]
  Htilde = matrix(Fq,[[alpha[j]**i*overgalpha[j] for j in range(n)] for i in range(t)])

  # "Form an mt x n matrix Hhat over F_2
  #  by replacing each entry u_0 + u_1 z + ... + u_{m-1} z^{m-1} of Htilde
  #  with a column of m bits u_0,u_1,...,u_{m-1}."
  # (same for the (0,0) case and the general case)
  F2 = GF(_sage_const_2 )
  Hintegers = [[Htildeij.integer_representation() for Htildeij in Htildei] for Htildei in Htilde]
  Hhat = matrix(F2,[[_sage_const_1 &(Hintegers[i//m][j]>>(i%m)) for j in range(n)] for i in range(m*t)])

  if check00 and (mu,nu) == (_sage_const_0 ,_sage_const_0 ):
    # "Reduce Hhat to systematic form (I_{mt} | T),
    #  where I_{mt} is an mt x mt identity matrix.
    #  If this fails, return False."
    H = echelon.echelon(Hhat)
    if not echelon.is_systematic(H): return False

    # "Return (T,Gamma)."
    T = H.matrix_from_columns(list(range(m*t,n)))
    assert T.nrows() == m*t
    assert T.ncols() == k
    
    return T,Gamma

  # "Reduce Hhat to (mu,nu)-semi-systematic form, obtaining a matrix H.
  #  If this fails, return False."
  H = echelon.echelon(Hhat)
  if not echelon.is_semi_systematic(H,mu,nu): return False

  # "Now row i has its leading 1 in column c_i."
  c = echelon.echelon_positions(H)

  # "By definition of semi-systematic form,
  #  c_i = i for 0 <= i < mt-mu;
  #  and mt-mu <= c_{mt-mu} < c_{mt-mu+1} < ... < c_{mt-1} < mt-mu+nu."
  assert all(c[i] == i for i in range(m*t-mu))
  assert all(c[i] <= i-mu+nu for i in range(m*t))

  # "Set (alpha'_0,alpha'_1,...,alpha'_{n-1}) <- (alpha_0,alpha_1,...,alpha_{n-1})."
  alphaprime = list(alpha)

  # "For i = mt-mu, then i = mt-mu+1, and so on through i = mt-1, in this order:
  #  swap column i with column c_i in H, while swapping alpha'_i with alpha'_{c_i}."
  for i in range(m*t-mu,m*t):
    alphaprime[i],alphaprime[c[i]] = alphaprime[c[i]],alphaprime[i]
    for j in range(H.nrows()):
      H[j,i],H[j,c[i]] = H[j,c[i]],H[j,i]
    # "After the swap, row i has its leading 1 in column i."
    assert H[i][:i] == _sage_const_0 
    assert H[i][i] == _sage_const_1 

  # "The matrix H now has systematic form (I_{mt} | T),
  #  where I_{mt} is an mt x mt identity matrix."
  assert echelon.is_systematic(H)
  T = H.matrix_from_columns(list(range(m*t,n)))

  # "Return (T,c_{mt-mu},...,c_{mt-1},Gamma')
  #  where Gamma' = (g,alpha'_0,alpha'_1,...,alpha'_{n-1}). ...
  #  In the special case (mu,nu) = (0,0) ...
  #  Gamma' is guaranteed to be the same as Gamma."
  Gammaprime = (g,)+tuple(alphaprime)
  if (mu,nu) == (_sage_const_0 ,_sage_const_0 ): assert Gammaprime == Gamma
  return (T,)+tuple(c[m*t-mu:m*t])+(Gammaprime,)

def test1():
  for system in parameters.alltests:
    P = parameters.parameters(system,allowtestparams=True)
    Fq = P.Fq
    Fqx = Fq['x']; (x,) = Fqx._first_ngens(1)
    m = P.m
    t = P.t
    n = P.n
    mu = P.mu
    nu = P.nu

    tries = _sage_const_0 
    while True:
      print('matgen %s' % system)
      sys.stdout.flush()
      tries += _sage_const_1 
      while True:
        g = Fqx.random_element(t)
        if g.is_irreducible(): break
      g /= g.leading_coefficient()
      alpha = list(Fq)
      shuffle(alpha)
      alpha = alpha[:n]
      Gamma = tuple([g]+alpha)
      result = matgen(Gamma,P)

      if (mu,nu) == (_sage_const_0 ,_sage_const_0 ):
        assert result == matgen(Gamma,P,check00=False)
        # "The general algorithm definition thus matches the (0,0) algorithm definition."

      if result == False: continue

      T = result[_sage_const_0 ]
      c = result[_sage_const_1 :-_sage_const_1 ]
      Gammaprime = result[-_sage_const_1 ]
      assert T.nrows() == m*t
      assert T.ncols() == n-m*t

      if (mu,nu) == (_sage_const_0 ,_sage_const_0 ):
        assert len(c) == _sage_const_0 
        assert Gammaprime == Gamma

      assert list(c) == sorted(set(c))
      assert all(cj >= m*t-mu for cj in c)
      assert all(cj < m*t-mu+nu for cj in c)
      assert Gammaprime[_sage_const_0 ] == g
      alphaprime = Gammaprime[_sage_const_1 :]
      assert len(alphaprime) == n
      assert sorted(alphaprime) == sorted(alpha)
      break

    print('successful matgen; tries: %d' % tries)
    sys.stdout.flush()

if __name__ == '__main__':
  test1()

