#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input2D.py"
 #                                    created: 12/29/03 {3:23:47 PM}
 #                                last update: 9/3/04 {10:41:38 PM}
 # Stolen from:
 #  Author: Jonathan Guyer
 #  E-mail: guyer@nist.gov
 #  Author: Daniel Wheeler
 #  E-mail: daniel.wheeler@nist.gov
 #    mail: NIST
 #     www: http://ctcms.nist.gov
 #  
 # ========================================================================
 # This software was developed at the National Institute of Standards
 # and Technology by employees of the Federal Government in the course
 # of their official duties.  Pursuant to title 17 Section 105 of the
 # United States Code this software is not subject to copyright
 # protection and is in the public domain.  FiPy is an experimental
 # system.  NIST assumes no responsibility whatsoever for its use by
 # other parties, and makes no guarantees, expressed or implied, about
 # its quality, reliability, or any other characteristic.  We would
 # appreciate acknowledgement if the software is used.
 # 
 # This software can be redistributed and/or modified freely
 # provided that any derivative works bear some notice that they are
 # derived from it, and any modified versions bear some notice that
 # they have been modified.
 # ========================================================================
 #  
 #  Description: 
 # 
 #  History
 # 
 #  modified   by  rev reason
 #  ---------- --- --- -----------
 #  2003-11-10 JEG 1.0 original
 # ###################################################################
 ##

"""

This example solves the Cahn-Hilliard equation given by:

.. raw:: latex

    $$ \\frac{\\partial \\phi}{\\partial t} = \\nabla \\cdot D \\nabla
    \\left( \\frac{\\partial f}{\\partial \\phi} - \\epsilon^2
    \\nabla^2 \\phi \\right) $$

where the free energy functional is given by,

.. raw:: latex

    $$ f = \\frac{a^2}{2} \\phi^2 (1 - \\phi)^2 $$

"""
__docformat__ = 'restructuredtext'

import Numeric

import optparse

import sys
args = [sys.argv[0]]
for arg in sys.argv[1:]:
    if '--numberOfElements' in arg or '--numberOfSteps' in arg:
        args.append(arg)

parser = optparse.OptionParser(option_list = [
    optparse.make_option('-e', '--numberOfElements', action = 'store', type = 'int', dest = 'numberOfElements', default = 400),
    optparse.make_option('-n', '--numberOfSteps', action = 'store', type = 'int', dest = 'steps', default = 100)])

(options, args) = parser.parse_args(args)

nx = int(Numeric.sqrt(options.numberOfElements))
ny = int(Numeric.sqrt(options.numberOfElements))

steps = options.steps

dx = 2.
dy = 2.

L = dx * nx

asq = 1.0
epsilon = 1
diffusionCoeff = 1

from fipy.meshes.grid2D import Grid2D
mesh = Grid2D(dx, dy, nx, ny)

import random
from fipy.variables.cellVariable import CellVariable
var = CellVariable(name = "phase field",
                   mesh = mesh,
                   value = [random.random() for x in range(nx * ny)])

##var.setValue(1, cells = mesh.getCells(lambda cell: cell.getCenter()[0] > L / 2))

faceVar = var.getArithmeticFaceValue()
doubleWellDerivative = asq * ( 1 - 6 * faceVar * (1 - faceVar))

from fipy.terms.nthOrderDiffusionTerm import NthOrderDiffusionTerm
from fipy.terms.transientTerm import TransientTerm
diffTerm2 = NthOrderDiffusionTerm(coeffs = (diffusionCoeff * doubleWellDerivative,))
diffTerm4 = NthOrderDiffusionTerm(coeffs = (diffusionCoeff, -epsilon**2))
eqch = TransientTerm() - diffTerm2 - diffTerm4

from fipy.solvers.linearPCGSolver import LinearPCGSolver
from fipy.solvers.linearLUSolver import LinearLUSolver
##solver = LinearLUSolver(tolerance = 1e-15,steps = 1000)
solver = LinearPCGSolver(tolerance = 1e-15,steps = 1000)

from fipy.boundaryConditions.fixedValue import FixedValue
from fipy.boundaryConditions.fixedFlux import FixedFlux
from fipy.boundaryConditions.nthOrderBoundaryCondition import NthOrderBoundaryCondition
BCs = (FixedFlux(mesh.getFacesRight(), 0),
       FixedFlux(mesh.getFacesLeft(), 0),
       NthOrderBoundaryCondition(mesh.getFacesLeft(), 0, 3),
       NthOrderBoundaryCondition(mesh.getFacesRight(), 0, 3),
       NthOrderBoundaryCondition(mesh.getFacesTop(), 0, 3),
       NthOrderBoundaryCondition(mesh.getFacesBottom(), 0, 3))

if __name__ == '__main__':

    from fipy.viewers.grid2DGistViewer import Grid2DGistViewer
    viewer = Grid2DGistViewer(var, minVal=0., maxVal=1.0, palette = 'rainbow.gp')
    viewer.plot()
    
dexp=-5

import time

runTime = time.clock()

for step in range(steps):
    dt = Numeric.exp(dexp)
    dt = min(100, dt)
    dexp += 0.01
    var.updateOld()
    eqch.solve(var, boundaryConditions = BCs, solver = solver, dt = dt)

    if __name__ == '__main__':
        viewer.plot()
        print 'step',step,'dt',dt

runTime = time.clock() - runTime
            
def getRunTime():
    return runTime
