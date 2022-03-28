from pydm import Display
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import math

class GradPf(Display):
    def __init__(self, parent=None, args=None):
        super(GradPf, self).__init__(parent=parent, args=args)


        # Functions related to user choice
        self.ui.compute_button.clicked.connect(self.buttonToggled)
        self.ui.compute_group.buttonClicked.connect(self.computeSwitch)

        #initialize radio button selected to Eacc and 1.3 GHz
        self.ui.eacc_radio.setChecked(True)
        self.ui.onepthree_radio.setChecked(True)

        # Initialize text fields
        self.ui.qext_edit.setText("4.1e7")
        self.ui.q0_edit.setText("2.7e10")
        self.ui.pf_edit.setText("1000")

        EpkOverSqrtU, EpkOverEacc, ROverQ, freq, L = self.getFreqParams()
        self.computeEacc(EpkOverSqrtU, EpkOverEacc)
        self.computePdiss(ROverQ, L)
        

        # initialize which fields you can edit
        self.ui.eacc_edit.setReadOnly(True)
        self.ui.pf_edit.setReadOnly(False)



        
    
    def ui_filename(self):
        return 'GradPf.ui'

    def buttonToggled(self):
        EpkOverSqrtU, EpkOverEacc, ROverQ, freq, L  = self.getFreqParams()
        meas = self.getMeasurement()
        if meas == "Eacc":
            self.computeEacc(EpkOverSqrtU, EpkOverEacc)
            self.computePdiss(ROverQ, L)
        else:
            self.computePf(EpkOverSqrtU, EpkOverEacc)
            self.computePdiss(ROverQ, L)


    def computeSwitch(self):
        if self.ui.eacc_radio.isChecked():
            self.ui.eacc_edit.setReadOnly(True)
            self.ui.pf_edit.setReadOnly(False)
        elif self.ui.pf_radio.isChecked():
            self.ui.pf_edit.setReadOnly(True)
            self.ui.eacc_edit.setReadOnly(False)
        else:
            self.ui.pf_edit.setReadOnly(True)
            self.ui.eacc_edit.setReadOnly(False)

    def getFreqParams(self):
        if self.ui.onepthree_radio.isChecked():
            freq = 1.3e9
            EpkOverSqrtU = 5.53
            EpkOverEacc = 2
            ROverQ = 1012
            L = 1.038
        else:
            freq = 3.9e9
            ROverQ = 750
            EpkOverSqrtU = 28
            EpkOverEacc = 2.26
            L = .346
        return EpkOverSqrtU, EpkOverEacc, ROverQ, freq, L

    def getMeasurement(self):
        if self.ui.eacc_radio.isChecked():
            meas = "Eacc"
        else:
            meas = "Pf"
        return meas

    def computeEacc(self,EpkOverSqrtU,EpkOverEacc):
        # user input
        Q0 = float(self.ui.q0_edit.text())

        Qext = float(self.ui.qext_edit.text())

        Pf = float(self.ui.pf_edit.text())

        if self.ui.onepthree_radio.isChecked():
            freq = 1.3e9
        else:
            freq = 3.9e9

        beta = Q0/Qext
        omega = 2*math.pi*freq
        U = 4*beta*Pf*Q0/(1+math.pow(beta,2))/omega
        Epk = EpkOverSqrtU*math.sqrt(U)
        E = Epk/EpkOverEacc

        self.ui.eacc_edit.setText(str(round(E,2)))

    def computePf(self,EpkOverSqrtU,EpkOverEacc):
        # user input
        Q0 = float(self.ui.q0_edit.text())
        Qext = float(self.ui.qext_edit.text())
        Eacc = float(self.ui.eacc_edit.text())

        if self.ui.onepthree_radio.isChecked():
            freq = 1.3e9
        else:
            freq = 3.9e9

        beta = Q0/Qext
        omega = 2*math.pi*freq
        Epk = Eacc*EpkOverEacc
        U = math.pow(Epk/EpkOverSqrtU,2)
        Pf = U*omega*(1+math.pow(beta,2))/4/beta/Q0

        self.ui.pf_edit.setText(str(round(Pf,2)))

    def computePdiss(self,ROverQ,L):
        # user input
        Q0 = float(self.ui.q0_edit.text())
        Eacc = float(self.ui.eacc_edit.text())

        Pdiss = math.pow(Eacc,2)*math.pow(L,2)*math.pow(1e6,2)/ROverQ/Q0

        self.ui.pdiss_edit.setText(str(round(Pdiss,2)))
        

    


        
        
