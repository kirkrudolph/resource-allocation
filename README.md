# Quadratic Program - Resource Allocation

This is a library function which solves a Quadratic Programs (QP) in order to
achieve constrained resource allocation. Targetted for real-time and embedded use.

## QP Solver
[OSQP](https://osqp.org/docs/release-0.6.3/index.html) is a solver for problems of the form of:

$$
\begin{array}{ll}
  \mbox{minimize} & \frac{1}{2} x^T P x + q^T x \\
  \mbox{subject to} & l \le A x \le u
\end{array}
$$

## Constrained Least-squares Problem

Consider the following constrained least-squares problem

$$
  \begin{array}{ll}
    \mbox{minimize} & \frac{1}{2} \|Ax - b\|_2^2 \\
    \mbox{subject to} & 0 \leq x \leq 1
  \end{array}
$$

The problem has the following equivalent form

$$
  \begin{array}{ll}
    \mbox{minimize} & \frac{1}{2} y^T y \\
    \mbox{subject to} & y = A x - b \\
                      & 0 \le x \le 1
  \end{array}
$$

## Examples

### Power

$$
P_{lower-limit} < Power < P_{upper-limit}
$$

### Code

