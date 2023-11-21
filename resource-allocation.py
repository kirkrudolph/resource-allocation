import osqp
import numpy as np
import scipy as sp
from scipy import sparse

# Generate problem data
np.random.seed(1)
m = 4
n = 4
Ad = sparse.random(m, n, density=0.7, format='csc')
b = np.random.randn(m)

# =====================================================================
# Constrained Least-Squared Problem (one or two sided resource allocation from requests): 
#
#                       min 0.5*|| Ax - b ||
#                       st.       1'x = 1       <- Must add up to 1 (All resources must be allocated)
#                              | x | <= | b |   <- Must move towards zero (systems can use less but they can't be forced to take more)
#
#                       min 0.5*|| A[x_l x_u] - [b b] ||
#                       st.       1'[x_l x_u] = [ll up]
# =====================================================================
# Constrained Least-Squared Equivalent Form: 
#
#                       min  0.5*y'y  
#                       st.  y = Ax - b
#                            1'x = 1
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
#               [ 1 ] <=  [ 1  0 ][ y ] <= [ 1 ]       1 <= 1'x    <= 1                            
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
        sparse.hstack([np.ones([1,n]), sparse.csc_matrix((1, m))])], format='csc')
print(A)
l = np.hstack([b, 1])
u = np.hstack([b, 1])

# Create an OSQP object
prob = osqp.OSQP()

# Setup workspace
prob.setup(P, q, A, l, u)

# Solve problem
res = prob.solve()

print(res.x[0:n])
print(sum(res.x[0:n]))