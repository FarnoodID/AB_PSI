
from pypbc import *
import time
import hashlib
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


# FY1 -	Foundation year one junior doctor
# FY2 -	Foundation year two junior doctor
# ST -	Specialty trainee in a hospital specialty - includes StR (specialty registrar) or have a number signifying the amount of years spent in training, eg ST4 psychiatry
# SpR -	Specialty registrar in a hospital specialty
# GPST - Specialty registrar in general practice
# SHO -	Senior house officer # CodeBy FarnoodID
# ACF – academic clinical fellow
# CL – clinical lecturer
# CRF – clinical research fellow
# CSL – senior clinical lecturer reader / associate professor
# prof – professor
#Credentials: Doctors require specific credentials such as medical degrees, licenses, and certifications to practice medicine. An ABAC system can use these credentials to ensure that only authorized doctors have access to sensitive information.
universal_attribute_set = ['is_medical_student', 'is_FY1', 'is_FY2',
                           'is_ST', 'is_SpR', 'is_GPST', 'is_SHO',
                           'is_consultant', 'is_specialist', 'is_associate_specialist',
                           'is_specialty', 'is_GP', 'is_ACF', 'is_CL',
                           'is_CFR', 'is_CSL', 'is_associate_professor', 'is_professor',
                           'is_anaesthetist', 'is_forensic_physician', 'is_gynaecologist',
                           'is_occupational_physician', 'is_physician', 'is_cardiologists',
                           'is_dermatologists', 'is_endocrinologists', 'is_gastroenterologists',
                           'is_geriatricians', 'is_haematologists', 'is_neurologists', 'is_oncologists',
                           'is_renal_physicians', 'is_respiratory_physicians', 'is_rheumatologists',
                           'has_credentials', 'is_resident', 'is_fellows', 'is_attending_physician', 'is_geneticist']

class AB_PSI:
    def __init__(self, universal_att_set):
        self.universal_attribute_set = universal_att_set
        self.Access_Tree = ['is_specialist', 'is_geneticist', 'is_professor', 'is_CFR']
        # Initialize a pairing group
        self.params = Parameters(qbits=512, rbits=160)
        self.pairing = Pairing(self.params)
        self.e = self.pairing.apply
    def data(self):
        #preparing data for computation # CodeBy FarnoodID
        dataset_X = []
        dataset_Y = []
        dir = "/home/farnood/Downloads/AB-PSI Data/"
        with open(dir + "sequenced_Hashed.txt", "r") as openfileobject:
            for line in openfileobject:
                dataset_X.append(Element.from_hash(self.pairing, Zr, line[:-1]))
        with open(dir + "sequenced_Hashed2.txt", "r") as openfileobject:
            for line in openfileobject:
                dataset_Y.append(Element.from_hash(self.pairing, Zr, line[:-1]))
        # print(dataset_X)
        # print(dataset_Y)
        return dataset_X, dataset_Y
    def Access_Policy(self, Att):
        #checking Access Policy satisfaction
        for v in self.Access_Tree:
            if v not in Att:
                return False
        return True
    def Share(self, secret_r):
        #sharing secret r
        qv = {}
        sum = Element.zero(self.pairing, Zr)
        att = self.Access_Tree.copy()
        last_att = att.pop()
        for v in att:
            qv[v] = Element.random(self.pairing, Zr)
            sum += qv[v]
        qv[last_att] = secret_r - sum
        return qv
    def Combine(self, value_set):
        #recovering secret r
        result = Element.one(self.pairing, GT)
        for value in value_set.values():
            result *= value
        return result
    def Setup(self):

        # Selecting random elements from G1 group
        g0 = Element.random(self.pairing, G1)
        g1 = Element.random(self.pairing, G1)
        g2 = Element.random(self.pairing, G1)
        g3 = Element.random(self.pairing, G1)

        # Selecting random elements from Zr
        x0 = Element.random(self.pairing, Zr)
        x1 = Element.random(self.pairing, Zr)

        #computing h variables
        h0 = pow(g0, x0)
        h1 = pow(g0, x1)
        h2 = g3 * pow(h1, x0)
        h3 = self.e(h0, g1)
        one1 = Element.one(self.pairing, G1)
        h4 = self.e(one1.__ifloordiv__(h0), h1)
        h5 = self.e(g0, g2)

        #selecting ska <- Zr and computing pka # CodeBy FarnoodID
        ska = {}
        pka = {}
        for a in self.universal_attribute_set:
            sk = Element.random(self.pairing, Zr)
            ska[a] = sk
            pka[a] = pow(g0, sk)

        PK = {  'g0' : g0,
                'g1' : g1,
                'g2' : g2,
                'h0' : h0,
                'h1' : h1,
                'h2' : h2,
                'h3' : h3,
                'h4' : h4,
                'h5' : h5,
                'pka': pka}

        MSK = {'x0' : x0,
               'x1' : x1,
               'g3' : g3,
               'ska': ska}

        return (PK, MSK)
    def Keygen(self, PK, MSK, Att, id):
        #generating secret-key of a data user
        g1 = PK['g1']
        g3 = MSK['g3']
        x0 = MSK['x0']
        ska = MSK['ska']
        idu = Element.from_hash(self.pairing, G1, id)

        Sk_u_Att = {}
        for a in Att:
            Sk_u_Att[a] = (pow(g1, x0) * g3 * pow(idu, ska[a]))

        return (Sk_u_Att)
    def Blind(self, PK, dataset_X):
        #providing data confidentiality
        r = Element.random(self.pairing, Zr)
        qv = self.Share(r)
        g0 = PK['g0']
        g2 = PK['g2']
        h3 = PK['h3']
        h4 = PK['h4']
        # CodeBy FarnoodID


        C1 = pow(g2, r)
        C2 = pow(h4, r)
        Cv1 = {} #Cva
        Cv2 = {} #C'va
        for v in self.Access_Tree:
            Cv1[v] = pow(g0, qv[v])
        one1 = Element.one(self.pairing, G1)
        for v in self.Access_Tree:
            Cv2[v] = pow(PK['pka'][v].__ifloordiv__(g2), qv[v])

        Cx = []
        for x in dataset_X:
            H = hashlib.sha256()
            H.update(bytes(str(pow(h3, r*x)).encode()))
            hash_v = H.digest()
            hash_v = Element.from_hash(self.pairing, Zr, hash_v)
            Cx.append(hash_v)

        BD_x = {'C1': C1, 'C2': C2, 'Cv1': Cv1, 'Cv2': Cv2, 'Cx' : Cx}
        return BD_x
    #ok
    def TokenGen1(self, PK, id, Sk_u_Att):
        g0 = PK['g0']
        g2 = PK['g2']
        h1 = PK['h1']
        h5 = PK['h5']
        idu = Element.from_hash(self.pairing, G1, id)

        s = Element.random(self.pairing, Zr)
        d = Element.random(self.pairing, Zr)

        tk1 = pow(g0, d)
        tk2 = pow(h1, d)
        tk3 = pow(idu, d)
        tk4 = pow(g0, s)
        tk5 = pow(h5, s*d)

        tk_u = {}
        for a, ska_u in Sk_u_Att.items():
            tk_u[a] = ska_u * pow(g2, s)

        TK_u_Att = {'tk1': tk1, 'tk2': tk2, 'tk3': tk3, 'tk4': tk4, 'tk5': tk5, 'tk_u' : tk_u, 'd' : d}

        return TK_u_Att
    #problem
    def TokenGen2(self, PK, TK_u_Att, BD_x, id):
        if not self.Access_Policy(list(TK_u_Att['tk_u'].keys())):
            raise TypeError("Error!") # CodeBy FarnoodID

        idu = Element.from_hash(self.pairing, G1, id)
        g2  = PK['g2']
        h0  = PK['h0']
        h2  = PK['h2']
        pka = PK['pka']

        C1  = BD_x['C1']
        C2  = BD_x['C2']
        Cv1 = BD_x['Cv1']
        Cv2 = BD_x['Cv2']
        Cx  = BD_x['Cx']

        tk1  = TK_u_Att['tk1']
        tk2  = TK_u_Att['tk2']
        tk3  = TK_u_Att['tk3']
        tk4  = TK_u_Att['tk4']
        tk5  = TK_u_Att['tk5']
        tk_u = TK_u_Att['tk_u']

        one = Element.one(self.pairing, Zr)
        n0 = one * len(self.Access_Tree)
        n0_inverse = one.__ifloordiv__(n0)

        one = Element.one(self.pairing, G1)
        TK_a_u_d = {}
        for a in self.Access_Tree:
            numerator = self.e(Cv1[a] * tk1 ** n0_inverse, tk_u[a])
            denominator = (self.e(Cv1[a] * tk1 ** n0_inverse, h2)
                           * self.e( tk3 ** n0_inverse, (pka[a]).__ifloordiv__(g2))
                           * self.e( idu, Cv2[a])
                           * tk5 ** n0_inverse)
            TK_a_u_d[a] = numerator.__ifloordiv__(denominator)

        TK_r_u_d = self.Combine(TK_a_u_d)

        TK_r_d = TK_r_u_d.__ifloordiv__(C2 * self.e(tk2 , one.__ifloordiv__(h0)) * self.e(tk4*idu, C1) * self.e(tk3, g2))
        TK_u_x = {'TK_r_d': TK_r_d, 'Cx': Cx}

        return TK_u_x
    def PSI(self, PK, TK_u_x, dataset_Y, d):
        TK_r_d = TK_u_x['TK_r_d']
        h3 = PK['h3']
        Cx = TK_u_x['Cx']

        one = Element.one(self.pairing, GT)
        data = []
        for index, y in enumerate(dataset_Y):
            H = hashlib.sha256()
            H.update(bytes(str(pow(TK_r_d * one.__ifloordiv__(pow(h3, d)), y)).encode()))
            hash_v = H.digest()
            hash_v = Element.from_hash(self.pairing, Zr, hash_v)
            data.append((hash_v, index))

        intersect = []
        for value in data:
            if value[0] in Cx:
                intersect.append(value)

        return intersect

if __name__ == '__main__':

    start = time.time()
    id = 'FarnoodWTB'
    Att = ['is_specialist', 'is_geneticist', 'is_professor', 'is_CFR']

    ab_psi = AB_PSI(universal_attribute_set)
    dataset_X, dataset_Y = ab_psi.data()
    PK, MSK = ab_psi.Setup()
    Sk_u_Att= ab_psi.Keygen(PK, MSK, Att, id)
    BD_x = ab_psi.Blind(PK, dataset_X)
    TK_u_Att = ab_psi.TokenGen1(PK, id, Sk_u_Att)
    TK_u_x = ab_psi.TokenGen2(PK, TK_u_Att, BD_x, id)
    d = TK_u_Att['d']
    intersection = ab_psi.PSI(PK, TK_u_x, dataset_Y, d)
    print(intersection)
    end = time.time() # CodeBy FarnoodID
    print("Spent time is:","{0:.2f}".format(end-start), "s")