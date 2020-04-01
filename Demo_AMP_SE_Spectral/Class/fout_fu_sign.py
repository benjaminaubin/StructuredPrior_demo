from Library.import_library import *
from Functions.generic_functions import gaussian


class fout_gout_dgout_sign(object):
    def __init__(self, K=1, Delta_2=0, invA_B=0, A=1, omega=0, V=1, inv_A=-1, Nishimori_identity=False):
        self.K = K
        self.Delta_2 = Delta_2
        self.invA_B = invA_B
        if inv_A == -1:
            self.inv_A = inv(A)
        else:
            self.inv_A = inv_A
        # Fix for initialization
        if self.inv_A < 0:
            self.inv_A = - self.inv_A
            #print('negative inv_A')
        self.omega = omega
        self.V = V
        self.inv_V = inv(V)

        self.fout = 0
        self.gout = 0
        self.dgout = 0
        self.Nishimori_identity = Nishimori_identity
        self.threshold_zero = 1e-4

    def compute_fout_gout(self):
        self.gout_()
        return self.fout, self.gout

    def compute_fout_gout_(self):
        return self.fout_gout_()

    def fout_gout_(self):
        omega = self.omega
        V = self.V
        Delta_2 = self.Delta_2
        inv_A = self.inv_A
        invA_B = self.invA_B

        fout = 1/2 * gaussian(invA_B, 1, Delta_2 + inv_A) * (1 + erf(omega/sqrt(2*V))) \
            + 1/2 * gaussian(invA_B, -1, Delta_2 + inv_A) * \
            (1 - erf(omega/sqrt(2*V)))

        dfout = (gaussian(invA_B, 1, Delta_2 + inv_A) - gaussian(invA_B, -1, Delta_2 + inv_A)) * \
            gaussian(omega, 0, V)

        res = 1/fout * dfout**2
        return res

    def compute_gout_dgout(self):
        self.dgout_()
        return self.gout, self.dgout

    def compute_fout_gout_dgout(self):
        self.dgout_()
        return self.fout, self.gout, self.dgout

    def fout_(self):
        omega = self.omega
        V = self.V
        Delta_2 = self.Delta_2
        inv_A = self.inv_A
        invA_B = self.invA_B

        fout = 1/2 * gaussian(invA_B, 1, Delta_2 + inv_A) * (1 + erf(omega/sqrt(2*V))) \
            + 1/2 * gaussian(invA_B, -1, Delta_2 + inv_A) * \
            (1 - erf(omega/sqrt(2*V)))

        if fout < self.threshold_zero:
            fout = 0

        self.fout = fout

    def gout_(self):
        omega = self.omega
        V = self.V
        Delta_2 = self.Delta_2
        inv_A = self.inv_A
        invA_B = self.invA_B

        self.fout_()
        fout = self.fout

        dfout = (gaussian(invA_B, 1, Delta_2 + inv_A) - gaussian(invA_B, -1, Delta_2 + inv_A)) * \
            gaussian(omega, 0, V)

        if fout < self.threshold_zero:
            gout = 0
        else:
            gout = dfout / fout
        self.fout = fout
        self.dfout = dfout
        self.gout = gout

    def dgout_(self):
        omega = self.omega
        V = self.V
        Delta_2 = self.Delta_2
        inv_A = self.inv_A
        invA_B = self.invA_B
        inv_V = inv(V)

        self.gout_()
        fout = self.fout
        gout = self.gout

        if self.Nishimori_identity:
            ddfout = 0
        else:
            ddfout = (gaussian(invA_B, 1, Delta_2 + inv_A) - gaussian(invA_B, -1, Delta_2 + inv_A)) * \
                gaussian(omega, 0, V) * (-omega/V)

        if fout < self.threshold_zero:
            dgout = 0
        else:
            dgout = 1/fout * ddfout - gout**2
        self.ddfout = ddfout
        self.dgout = dgout


class fu_0_1_2_sign(object):
    def __init__(self, K=1, Delta_2=0, invA_B=0, A=1, omega=0, V=1, inv_A=-1):
        self.K = K
        self.Delta_2 = Delta_2
        self.invA_B = invA_B
        if inv_A == -1:
            self.inv_A = inv(A)
        else:
            self.inv_A = inv_A
        # Fix for initialization
        if self.inv_A < 0:
            self.inv_A = - self.inv_A
            #print('negative inv_A')

        self.omega = omega
        self.V = V
        self.inv_V = inv(V)
        self.inv_Delta2_A = inv(self.Delta_2 + self.inv_A)
        self.fu_0 = 0
        self.fu_1 = 0
        self.fu_2 = 0

        self.threshold_zero = 1e-4

    def compute_fu_0_1(self):
        self.fu_1_()
        return self.fu_0, self.fu_1

    def compute_fu_0_1_(self):
        return self.fu_0_1_()

    def compute_fu_1_2(self):
        self.fu_2_()
        return self.fu_1, self.fu_2

    def compute_fu_0_1_2(self):
        self.fu_2_()
        return self.fu_0, self.fu_1, self.fu_2

    def fu_0_1_(self):
        omega = self.omega
        V = self.V
        Delta_2 = self.Delta_2
        inv_A = self.inv_A
        invA_B = self.invA_B
        inv_Delta2_A = self.inv_Delta2_A

        fu_0 = 1/2 * gaussian(invA_B, 1, Delta_2 + inv_A) * (1 + erf(omega/sqrt(2*V))) \
            + 1/2 * gaussian(invA_B, -1, Delta_2 + inv_A) * \
            (1 - erf(omega/sqrt(2*V)))

        term1 = 1/2 * inv_Delta2_A * \
            (1 - invA_B) * gaussian(invA_B, 1, Delta_2 + inv_A) * \
            (1 + erf(omega/sqrt(2*V)))
        term2 = 1/2 * inv_Delta2_A * \
            (-1 - invA_B) * gaussian(invA_B, -1,
                                     Delta_2 + inv_A) * (1 - erf(omega/sqrt(2*V)))
        dfu_0 = term1 + term2
        res = 1 / fu_0 * (dfu_0)**2
        return res

    def fu_0_(self):
        omega = self.omega
        V = self.V
        Delta_2 = self.Delta_2
        inv_A = self.inv_A
        invA_B = self.invA_B

        fu_0 = 1/2 * gaussian(invA_B, 1, Delta_2 + inv_A) * (1 + erf(omega/sqrt(2*V))) \
            + 1/2 * gaussian(invA_B, -1, Delta_2 + inv_A) * \
            (1 - erf(omega/sqrt(2*V)))
        if np.abs(fu_0) < self.threshold_zero:
            fu_0 = 0
        self.fu_0 = fu_0

    def fu_1_(self):
        omega = self.omega
        V = self.V
        Delta_2 = self.Delta_2
        inv_A = self.inv_A
        invA_B = self.invA_B
        inv_Delta2_A = self.inv_Delta2_A

        self.fu_0_()
        fu_0 = self.fu_0

        term1 = 1/2 * inv_Delta2_A * \
            (1 - invA_B) * gaussian(invA_B, 1, Delta_2 + inv_A) * \
            (1 + erf(omega/sqrt(2*V)))
        term2 = 1/2 * inv_Delta2_A * \
            (-1 - invA_B) * gaussian(invA_B, -1,
                                     Delta_2 + inv_A) * (1 - erf(omega/sqrt(2*V)))
        dfu_0 = term1 + term2

        if np.abs(fu_0) < self.threshold_zero:
            fu_1 = 0
        else:
            fu_1 = inv_A * dfu_0 / fu_0 + invA_B
        self.fu_0 = fu_0
        self.dfu_0 = dfu_0
        self.fu_1 = fu_1

    def fu_2_(self):
        omega = self.omega
        V = self.V
        Delta_2 = self.Delta_2
        inv_A = self.inv_A
        invA_B = self.invA_B
        inv_Delta2_A = self.inv_Delta2_A

        self.fu_1_()
        fu_0 = self.fu_0
        fu_1 = self.fu_1

        term1 = - 1/2 * inv_Delta2_A * \
            gaussian(invA_B, 1, Delta_2 + inv_A) * (1 + erf(omega/sqrt(2*V)))
        term2 = 1/2 * (inv_Delta2_A * (1 - invA_B))**2 * gaussian(invA_B, 1, Delta_2 + inv_A) * \
            (1 + erf(omega/sqrt(2*V)))
        term3 = - 1/2 * inv_Delta2_A * \
            gaussian(invA_B, -1, Delta_2 + inv_A) * (1 - erf(omega/sqrt(2*V)))
        term4 = 1/2 * (inv_Delta2_A * (-1 - invA_B))**2 * gaussian(invA_B, -1, Delta_2 + inv_A) * \
            (1 - erf(omega/sqrt(2*V)))
        ddfu_0 = term1 + term2 + term3 + term4

        if fu_0 < self.threshold_zero:
            fu_2 = 0
        else:
            fu_2 = inv_A**2 * 1/fu_0 * ddfu_0 + inv_A - \
                invA_B**2 + 2 * invA_B * fu_1 - fu_1**2

        self.fu_2 = fu_2
