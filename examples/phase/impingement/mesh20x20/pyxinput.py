#!/usr/bin/env python

## 
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "input.py"
 #                                    created: 06/29/04 {2:24:00 PM} 
 #                                last update: 11/1/04 {11:01:36 AM}
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
 #  Author: Alexander Mont <alexander.mont@nist.gov>
 #    mail: NIST
 #     www: http://www.ctcms.nist.gov/fipy/
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
 #  2004-6-24 ADM 1.0 original
 # ###################################################################
 ##

"""

In this example we solve the same set of equations as in
`examples/phase/impingemnet/mesh40x1/input.py` with different initial
conditions and mesh size. The initial conditions are given by

.. raw:: latex

    $$ \\phi = 1 \;\; \\text{and} \;\; \\theta = \\frac{2 \\pi}{3} \;\; \\text{for} \;\; x^2 - y^2 < L / 2 $$
    $$ \\phi = 1 \;\; \\text{and} \;\; \\theta = \\frac{-2 \\pi}{3} \;\; \\text{for} \;\; (x-L)^2 - y^2 < L / 2 $$
    $$ \\phi = 1 \;\; \\text{and} \;\; \\theta = \\frac{-2 \\pi}{3}+0.3 \;\; \\text{for} \;\; x^2 - (y-L)^2 < L / 2 $$
    $$ \\phi = 1 \;\; \\text{and} \;\; \\theta = \\frac{2 \\pi}{3} \;\; \\text{for} \;\; (x-L)^2 - (y-L)^2 < L / 2 $$

This defines four solid regions with different
orientations. Solidification occurs and then boundary wetting occurs
where the orientation varies.

   >>> for i in range(steps):        
   ...     it.timestep()

The solution is compared with test data. The test data was created
with a FORTRAN code written by Ryo Kobayashi for phase field
modeling. The following code opens the file `test.gz` extracts the
data and compares it with the `theta` variable.

   >>> import os
   >>> testFile = 'test.gz'
   >>> import examples.phase.impingement.mesh20x20
   >>> filestream=os.popen('gunzip --fast -c < %s/%s'%(examples.phase.impingement.mesh20x20.__path__[0], testFile),'r')
   >>> import cPickle
   >>> testData = cPickle.load(filestream)
   >>> filestream.close()
   >>> import Numeric
   >>> theta =  Numeric.array(theta)
   >>> testData = Numeric.reshape(testData, theta.shape)
   >>> Numeric.allclose(theta, testData, rtol = 1e-10, atol = 1e-10)
   1


"""
__docformat__ = 'restructuredtext'

##from __future__ import nested_scopes

import Numeric

from fipy.meshes.grid2D import Grid2D
from fipy.models.phase.phase.type1MPhiVariable import Type1MPhiVariable
from fipy.models.phase.phase.phaseEquation import PhaseEquation
from fipy.solvers.linearPCGSolver import LinearPCGSolver
from fipy.boundaryConditions.fixedValue import FixedValue
from fipy.boundaryConditions.fixedFlux import FixedFlux
from fipy.iterators.iterator import Iterator
from fipy.viewers.pyxviewer import PyxViewer
from fipy.viewers.pyxviewer import Grid2DPyxViewer
from fipy.variables.cellVariable import CellVariable
from fipy.models.phase.theta.modularVariable import ModularVariable
from fipy.models.phase.theta.thetaEquation import ThetaEquation

nx = 20
ny = 20
steps = 10
temperature = 10.

timeStepDuration = 0.02

sharedPhaseThetaParameters = {
    'epsilon'               : 0.008,
    's'                     : 0.01,
    'anisotropy'            : 0.0,
    'alpha'                 : 0.015,
    'symmetry'              : 4.
    }

phaseParameters = {
    'tau'                   : 0.1,
    'time step duration'    : timeStepDuration
    }

thetaParameters = {
    'time step duration'    : timeStepDuration,
    'small value'           : 1e-6,
    'beta'                  : 1e5,
    'mu'                    : 1e3,
    'tau'                   : 0.01,
    'gamma'                 : 1e3 
    }

for key in sharedPhaseThetaParameters.keys():
    phaseParameters[key] = sharedPhaseThetaParameters[key]
    thetaParameters[key] = sharedPhaseThetaParameters[key]
            
Lx = 2.5 * nx / 100.
Ly = 2.5 * ny / 100.            
dx = Lx / nx
dy = Ly / ny

mesh = Grid2D(dx,dy,nx,ny)

pi = Numeric.pi
        
phase = CellVariable(
    name = 'PhaseField',
    mesh = mesh,
    value = 0.
    )

theta = ModularVariable(
    name = 'Theta',
    mesh = mesh,
    value = -pi + 0.0001
    )

circleCenters = ((0., 0.), (Lx, 0.), (0., Ly), (Lx, Ly))
thetaValues = (2. * pi / 3., -2. * pi / 3., -2. * pi / 3. + 0.3, 2. * pi / 3.)

for i in range(len(thetaValues)):

    (a, b) = circleCenters[i]
    
    def circle(cell):
        x = cell.getCenter()[0]
        y = cell.getCenter()[1]
        if ((x - a)**2 + (y - b)**2) < (Lx / 2.)**2:
            return 1
        else:
            return 0

    cells = mesh.getCells(filter = circle)

    phase.setValue(1., cells)
    theta.setValue(thetaValues[i], cells)
        


thetaProd = -pi + phase * (theta + pi)
        
phaseViewer = Grid2DPyxViewer(phase)
thetaProductViewer = Grid2DPyxViewer(thetaProd)
        
phaseFields = {
    'theta' : theta,
    'temperature' : temperature
    }
        
thetaFields = {
    'phase' : phase
    }

thetaEq = ThetaEquation(
    var = theta,
    solver = LinearPCGSolver(
    tolerance = 1.e-15, 
    steps = 2000
    ),
    boundaryConditions = (
    FixedFlux(mesh.getExteriorFaces(), 0.),
    ),
    parameters = thetaParameters,
    fields = thetaFields
    )
        
phaseEq = PhaseEquation(
    var = phase,
    mPhi = Type1MPhiVariable,
    solver = LinearPCGSolver(
    tolerance = 1.e-15, 
    steps = 1000
    ),
    boundaryConditions = (
    FixedFlux(mesh.getExteriorFaces(), 0.),
    ),
    parameters = phaseParameters,
    fields = phaseFields
    )
        
it = Iterator((thetaEq, phaseEq))

if __name__ == '__main__':

    for i in range(steps):
        it.timestep()

    phaseViewer.plot(minval = 0.0, maxval = 1.0, maxx = 0.5, maxy = 0.5, viewcmd = "gv", resolution = 0.005, scalefile = "scaletestp", valuelabel = "Phase Variable")
    thetaProductViewer.plot(minval = -pi, maxval = pi, maxx = 0.5, maxy = 0.5, viewcmd = "gv", resolution = 0.005, scalefile = "scaletestt", valuelabel = "Theta Product")

    raw_input('finished')