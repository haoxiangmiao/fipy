#!/usr/bin/env python

## 
 # -*-Pyth-*-
 # ###################################################################
 #  FiPy - Python-based finite volume PDE solver
 # 
 #  FILE: "phaseEquation.py"
 #                                    created: 11/12/03 {10:39:23 AM} 
 #                                last update: 9/3/04 {10:35:49 PM} 
 #  Author: Jonathan Guyer <guyer@nist.gov>
 #  Author: Daniel Wheeler <daniel.wheeler@nist.gov>
 #  Author: James Warren   <jwarren@nist.gov>
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
 #  2003-11-12 JEG 1.0 original
 # ###################################################################
 ##

import Numeric

from fipy.equations.matrixEquation import MatrixEquation
from fipy.terms.transientTerm import TransientTerm
from fipy.terms.explicitDiffusionTerm import ExplicitDiffusionTerm
from fipy.terms.scSourceTerm import ScSourceTerm
from fipy.terms.spSourceTerm import SpSourceTerm


from phaseDiffusionVariable import PhaseDiffusionVariable
from anisotropyVariable import AnisotropyVariable
from spSourceVariable import SpSourceVariable
from phaseHalfAngleVariable import PhaseHalfAngleVariable
from scSourceVariable import ScSourceVariable

class PhaseEquation(MatrixEquation):

    def __init__(self,
                 var,
                 solver = 'default_solver',
                 boundaryConditions = (),
                 fields = {},
                 parameters = {},
                 mPhi = 0.):
        
        mesh = var.getMesh()
	
	self.parameters = parameters

	self.var = var
	self.temp = fields['temperature']
##        self.thetaOld = fields['theta']
        self.thetaOld = fields['theta'].getOld()
        	
	self.mPhi = mPhi(phase = self.var, temperature = self.temp, parameters = parameters)

        self.halfAngle = PhaseHalfAngleVariable(
            parameters = self.parameters,
            phase = self.var,
            theta = self.thetaOld
            )

        self.diffTerm = ExplicitDiffusionTerm(
	    diffCoeff = PhaseDiffusionVariable(
            parameters = self.parameters,
            halfAngle = self.halfAngle
            ),
	    mesh = mesh,
	    boundaryConditions = boundaryConditions
            )
	
        self.spTerm = SpSourceTerm(
            sourceCoeff = SpSourceVariable(
            theta = self.thetaOld,
            mPhi = self.mPhi,
            phase = self.var,
            parameters = self.parameters),
	    mesh = mesh)

        anisotropy = AnisotropyVariable(parameters = parameters, phase = self.var, halfAngle = self.halfAngle)

        self.scTerm = ScSourceTerm(
            sourceCoeff = ScSourceVariable(mPhi = self.mPhi, phase = self.var, anisotropy = anisotropy),
	    mesh = mesh)
	
	transientCoeff = parameters['tau']
        
	terms = (
	    TransientTerm(transientCoeff, mesh),
	    self.diffTerm,
            self.scTerm,
            self.spTerm
	)

	MatrixEquation.__init__(
            self,
            var,
            terms,
            solver)