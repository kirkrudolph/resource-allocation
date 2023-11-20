import osqp
import numpy as np
import scipy as sp
from scipy import sparse

# Generate problem data
np.random.seed(1)
m = 6
n = 4
Ad = sparse.random(m, n, density=0.7, format='csc')
b = np.random.randn(m)

# =====================================================================
# Constrained Least-Squared Problem (one sided resource allocation): 
#
#                       min 0.5*|| Ax - b ||
#                       st.      1'x = Limit
# =====================================================================
# Constrained Least-Squared Equivalent Form: 
#
#                       min  0.5*y'y  
#                       st.  y = Ax - b
#                            0 <= x <= 1
# Proof:
#
# y'y = (Ax-b)'(Ax-b)
#     = ...
#     = || Ax-b ||
#
# =====================================================================
# OSQP Form: 
#                       min 0.5*x'Px+q'x
#                       st. l <= Ax <= u
# =====================================================================
# Block Form:
#                         [ 0  0 ][ x ]                
#          min 0.5*[ x y ][ 0  I ][ y ]                    0.5 * y'y
#          st.  [ b ]     [ A -I ][ x ]    [ b ]       b <= Ax - y <= b
#               [ 0 ] <=  [ I  0 ][ y ] <= [ 1 ]       0 <= x      <= 1                            
# =====================================================================
# Example:
#
# =====================================================================
# So... 
#       1. I just care about the first few values of the solution.
#       2. P never changes, q never changes
#       3. u and l definetly change
#       4. If A contains weights, A will change. 
#          - Likely there are some smart "default" hardcodable choices.
#          - A = I (normalize / all equal)
#          - A = pre-set large to small (ordered priority)
#

# OSQP data
P = sparse.block_diag([sparse.csc_matrix((n, n)), sparse.eye(m)], format='csc')
q = np.zeros(n+m)
A = sparse.vstack([
        sparse.hstack([Ad, -sparse.eye(m)]),
        sparse.hstack([sparse.eye(n), sparse.csc_matrix((n, m))])], format='csc')
l = np.hstack([b, np.zeros(n)])
u = np.hstack([b, np.ones(n)])

# Create an OSQP object
prob = osqp.OSQP()

# Setup workspace
prob.setup(P, q, A, l, u)

# Solve problem
res = prob.solve()

print(res.x[0:n])