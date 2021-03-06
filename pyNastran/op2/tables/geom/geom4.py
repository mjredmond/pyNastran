"""
defines readers for BDF objects in the OP2 GEOM4/GEOM4S table
"""
#pylint: disable=C0111,C0103
from __future__ import print_function
from struct import unpack, Struct
from six import b
from six.moves import range
import numpy as np

from pyNastran.bdf.cards.elements.rigid import RBAR, RBE2, RBE3, RROD
from pyNastran.bdf.cards.bdf_sets import (
    ASET, ASET1, BSET, BSET1, CSET, CSET1, QSET, QSET1, USET, USET1, SEQSET1 # SEQSET
)
from pyNastran.bdf.cards.loads.loads import SPCD
from pyNastran.op2.tables.geom.geom_common import GeomCommon
from pyNastran.bdf.cards.constraints import (
    SUPORT1, SUPORT,
    SPC, SPC1, SPCADD, SPCOFF, SPCOFF1,
    MPC, MPCADD, #SPCAX, SESUP, GMSPC
)

class GEOM4(GeomCommon):
    """defines methods for reading op2 constraints"""

    def _read_geom4_4(self, data, ndata):
        """reads the GEOM4/GEOM4OLD table"""
        return self._read_geom_4(self._geom4_map, data, ndata)

    def __init__(self):
        GeomCommon.__init__(self)
        self._geom4_map = {
            (5561, 76, 215): ['ASET', self._read_aset],          # record 1
            (5571, 77, 216): ['ASET1', self._read_aset1],        # record 2
            (10200, 102, 473): ['BNDGRID', self._read_bndgrid],  # record 3  - not done

            (110, 1, 311): ['BSET', self._read_bset],            # record 5  - not done
            (410, 4, 314): ['BSET1', self._read_bset1],          # record 6  - not done
            (310, 3, 313): ['CSET', self._read_cset],            # record 7  - not done
            (210, 2, 312): ['CSET1', self._read_cset1],          # record 8  - not done

            (1510, 15, 328): ['CYAX', self._read_cyax],          # record 9  - not done
            (5210, 52, 257): ['CYJOIN', self._read_cyjoin],      # record 10 - not done
            (1610, 16, 329) : ['CYSUP', self._read_cysup],       # record 11 - not done
            (1710, 17, 330): ['CYSYM', self._read_cysym],        # record 12 - not done
            (8801, 88, 9022) : ['EGENDT', self._read_egendt],    # record 13 - not done (NX)
            (9001, 90, 9024): ['FCENDT', self._read_fcendt],     # record 14 - not done (NX)
            (8001, 80, 395): ['GMBC', self._read_gmbc],          # record 15 - not done
            (7801, 78, 393): ['GMSPC', self._read_gmspc],        # record 16 - not done
            #: ['', self._read_fake],


            (4901, 49, 17) : ['MPC', self._read_mpc],             # record 17
            (4891, 60, 83) : ['MPCADD', self._read_mpcadd],       # record 18
            (5001, 50, 15) : ['OMIT', self._read_omit],           # record 19 - not done
            (4951, 63, 92) : ['OMIT1', self._read_omit1],         # record 20 - not done
            (510, 5, 315) : ['QSET', self._read_qset],            # record 21
            (610, 6, 316) : ['QSET1', self._read_qset1],          # record 22

            (6601, 66, 292) : ['RBAR', self._read_rbar],          # record 23 - not done
            (6801, 68, 294) : ['RBE1', self._read_rbe1],          # record 24 - not done
            (6901, 69, 295) : ['RBE2', self._read_rbe2],          # record 25 - buggy
            (7101, 71, 187) : ['RBE3', self._read_rbe3],          # record 26 - not done
            (14201, 142, 652) : ['RBJOINT', self._read_rbjoint],  # record 27 - not done
            (14301, 143, 653) : ['RBJSTIF', self._read_rbjstif],  # record 28 - not done
            (1310, 13, 247) : ['RELEASE', self._read_release],    # record 29 - not done
            (14101, 141, 640): ['RPNOM', self._read_rpnom],       # record 30 - not done
            (6501, 65, 291): ['RROD', self._read_rrod],           # record 31 - not done
            (7001, 70, 186): ['RSPLINE', self._read_rspline],     # record 32 - not done
            (7201, 72, 398): ['RSSCON', self._read_rsscon],       # record 33 - not done
            #: ['', self._read_fake],
            #: ['', self._read_fake],
            #: ['', self._read_fake],
            (1110, 11, 321): ['SEQSET', self._read_seqset],      # record 40
            (1210, 12, 322): ['SEQSET1', self._read_seqset1],    # record 41
            (5110, 51, 256): ['SPCD', self._read_spcd],          # record 48 - buggy

            # these ones are not fully marked...
            (5501, 55, 16): ['SPC', self._read_spc],             # record 44 - buggy
            (5481, 58, 12): ['SPC1', self._read_spc1],           # record 45 - not done
            (5491, 59, 13): ['SPCADD', self._read_spcadd],       # record 46 - not done
            (5601, 56, 14): ['SUPORT', self._read_suport],       # record 59 - not done
            (10100, 101, 472): ['SUPORT1', self._read_suport1],  # record 60 - not done
            (2010, 20, 193) : ['USET', self._read_uset],         # Record 62

            (6210, 62, 344): ['SPCOFF1', self._read_spcoff1],    # record
            (2110, 21, 194) : ['USET1', self._read_uset1],  # record
            (1010, 10, 320): ['SECSET1', self._read_secset1],  # record

            (4901, 49, 420017): ['', self._read_fake],    # record
            (5561, 76, 0): ['PLOTEL/SESET?', self._read_fake],         # record
            (610, 6, 0): ['', self._read_fake],           # record
            (5110, 51, 620256): ['', self._read_fake],    # record
            (5501, 55, 620016): ['', self._read_fake],    # record
            (410, 4, 0): ['', self._read_fake],    # record
            (6701, 67, 293): ['RTRPLT', self._read_rtrplt],    # record 34
            (9801, 98, 79): ['', self._read_fake],  # record
            (9901, 99, 80): ['', self._read_fake],  # record
            (12001, 120, 601) : ['BLTMPC', self._read_bltmpc],  # record (NX)

            # GEOM4705 - pre MSC 2001
            (110, 1, 584): ['BNDFIX', self._read_bndfix],    # record 3 (NX)
            (210, 2, 585): ['BNDFIX1', self._read_bndfix1],    # record 4 (NX)
            (310, 3, 586) : ['BNDFREE', self._read_bndfree],  # record 5 (NX)

            (9801, 98, 609) : ['RVDOF', self._read_fake],
            (9901, 99, 610) : ['RVDOF1', self._read_fake],
            (11901, 119, 561) : ['RWELD', self._read_fake],
            (5571, 77, 0) : ['', self._read_fake],

            # F:\work\pyNastran\pyNastran\master2\pyNastran\bdf\test\nx_spike\out_sdr_s111se.op2
            (210, 2, 0) : ['', self._read_fake],
            (810, 8, 318) : ['SESET?', self._read_fake],
        }

    def _read_aset(self, data, n):
        """ASET(5561,76,215) - Record 1"""
        return self._read_xset(data, n, 'ASET', ASET, self._add_aset_object)

    def _read_qset(self, data, n):
        """QSET(610, 6, 316) - Record 21"""
        return self._read_xset(data, n, 'QSET', QSET, self._add_qset_object)

    def _read_aset1(self, data, n):
        """
        ASET1(5571,77,216) - Record 22

        ASET1=(5, 0, 4, 10, -1,
               12345, 0, 1, 2, 3, -1,
               12345, 0, 8, 9)
        """
        return self._read_xset1(data, n, 'ASET1', ASET1, self._add_aset_object)

    def _read_xset(self, data, n, card_name, cls, add_method):
        """common method for ASET, QSET; not USET"""
        s = Struct(b(self._endian + '2i'))
        #self.show_data(data, types='ifs')
        ntotal = 8
        nelements = (len(data) - n) // ntotal
        for i in range(nelements):
            edata = data[n:n + ntotal]
            out = s.unpack(edata)
            if self.is_debug_file:
                self.binary_debug.write('  %s=%s\n' % (card_name, str(out)))
            #(id, component) = out
            set_obj = cls.add_op2_data(out)
            add_method(set_obj)
            n += ntotal
            self.increase_card_count(card_name, 1)
        return n

    def _read_xset1(self, data, n, card_name, cls, add_method, debug=False):
        r"""
        common method for ASET1, QSET1; not USET1

        F:\work\pyNastran\pyNastran\master2\pyNastran\bdf\test\nx_spike\out_cntlmtlboltld02.op2
        [123   0   6  10  -1]
        """
        ndata = len(data)
        #nfields = (ndata - n) // 4
        #fmt = '%ii' % nfields
        out = np.fromstring(data[n:], self.idtype)
        #print(out)
        izero = np.where(out == -1)[0]
        if len(izero) == 0:
            card = cls.add_op2_data(out)
            add_method(card)
            self.increase_card_count(card_name, 1)
        else:
            i = np.hstack([[0], izero[:-1]+1])
            j = np.hstack([izero[:-1], -1])
            #print(i, j)
            for ii, jj in zip(i, j):
                outi = out[ii:jj]
                #print(outi)
                assert -1 not in outi, outi
                if self.is_debug_file:
                    self.binary_debug.write('  %s=%s\n' % (card_name, str(out)))
                card = cls.add_op2_data(outi)
                add_method(card)
            self.increase_card_count(card_name, len(i))
        return ndata

    def _add_superset_card(self, cls, card_name, add_method, out):
        """helper method for ``_read_superxset1``"""
        #print('out =', out)
        seid = out[0]
        components = out[1]
        thru_flag = out[2]
        if thru_flag == 0:
            nids = out[3:]
            thru_check = False
        else:
            nids = list(range(out[3], out[4]+1))
            thru_check = True

        in_data = [seid, components, nids]
        card = cls.add_op2_data(in_data)
        add_method(card)
        self.increase_card_count(card_name, 1)
        if thru_check and len(out) > 5:
            card = out[5:]
            #print('out[5:] =', out[5:])
            self._add_superset_card(cls, card_name, add_method, out[5:])

    def _read_superxset1(self, data, n, card_name, cls, add_method, debug=False):
        r"""
        common method for ASET1, QSET1; not USET1

        F:\work\pyNastran\pyNastran\master2\pyNastran\bdf\test\nx_spike\out_cntlmtlboltld02.op2
        [123   0   6  10  -1]
        [  1   0   1 101 112
           2   0   1 113 124]
        """
        ndata = len(data)
        #nfields = (ndata - n) // 4
        #fmt = '%ii' % nfields
        out = np.fromstring(data[n:], self.idtype)
        #print(out)
        iminus1 = np.where(out == -1)[0]
        if len(iminus1) == 0:
            self._add_superset_card(cls, card_name, add_method, out)
        else:
            i = np.hstack([[0], iminus1[:-1]+1])
            j = np.hstack([iminus1[:-1], -1])
            #print(i, j)
            for ii, jj in zip(i, j):
                outi = out[ii:jj]
                #print(outi)
                assert -1 not in outi, outi
                if self.is_debug_file:
                    self.binary_debug.write('  %s=%s\n' % (card_name, str(out)))

                self._add_superset_card(cls, card_name, add_method, out)

                #seid = data[0]
                #components = data[1]
                #thru_flag = outi[2]
                #if thru_flag == 0:
                    #nids = outi[3:]
                #else:
                    #assert len(outi) == 5, outi
                    #nids = list(range(outi[3], outi[4]+1))

                #in_data = [seid, components, nids]

                #card = cls.add_op2_data(in_data)
                #add_method(card)
            #self.increase_card_count(card_name, len(i))
        return ndata

    def _read_bndgrid(self, data, n):
        """BNDGRID(10200,102,473) - Record 3 """
        self.log.info('skipping BNDGRID in GEOM4\n')
        return len(data)

    def _read_bset(self, data, n):
        return self._read_xset(data, n, 'BSET', BSET, self._add_bset_object)

    def _read_bset1(self, data, n):
        return self._read_xset1(data, n, 'BSET1', BSET1, self._add_bset_object)

    def _read_cset(self, data, n):
        return self._read_xset(data, n, 'CSET', CSET, self._add_cset_object)

    def _read_cset1(self, data, n):
        return self._read_xset1(data, n, 'CSET1', CSET1, self._add_cset_object)

    def _read_cyax(self, data, n):
        """CYAX(1510,15,328) - Record 8 """
        self.log.info('skipping CYAX in GEOM4\n')
        return len(data)

    def _read_cyjoin(self, data, n):
        """CYJOIN(5210,52,257) - Record 9 """
        self.log.info('skipping CYJOIN in GEOM4\n')
        return len(data)

    def _read_cysup(self, data, n):
        self.log.info('skipping CYSUP in GEOM4\n')
        return len(data)

    def _read_cysym(self, data, n):
        """CYSYM(1710,17,330) - Record 11"""
        self.log.info('skipping CYSYM in GEOM4\n')
        return len(data)

    def _read_egendt(self, data, n):
        self.log.info('skipping EGENDT in GEOM4\n')
        return len(data)

    def _read_fcendt(self, data, n):
        self.log.info('skipping FCENDT in GEOM4\n')
        return len(data)

    def _read_gmbc(self, data, n):
        self.log.info('skipping GMBC in GEOM4\n')
        return len(data)

    def _read_gmspc(self, data, n):
        self.log.info('skipping GMSPC in GEOM4\n')
        return len(data)

    def _read_mpc(self, data, n):
        """MPC(4901,49,17) - Record 16"""
        ndata = len(data)
        nfields = (ndata - n) // 4
        datan = data[n:]
        ints = unpack(b(self._endian + '%ii' % nfields), datan)
        floats = unpack(b(self._endian + '%if' % nfields), datan)

        i = 0
        nentries = 0
        while i < nfields:
            sid, grid, comp = ints[i:i+3]
            coeff = floats[i+3]
            mpc_data = [sid, grid, comp, coeff]
            nodes = [grid]
            components = [comp]
            coefficients = [coeff]

            intsi = ints[i+4:i+7]
            assert len(intsi) == 3, intsi
            while intsi != (-1, -1, -1):
                gridi, compi, coeffi = ints[i+4], ints[i+5], floats[i+6]
                mpc_data.extend([gridi, compi, coeffi])
                nodes.append(gridi)
                components.append(compi)
                coefficients.append(coeffi)
                i += 3
                intsi = ints[i+4:i+7]
            mpc_data.extend([-1, -1, -1])
            i += 7 # 3 + 4 from (-1,-1,-1) and (sid,grid,comp,coeff)
            if self.is_debug_file:
                self.binary_debug.write('  MPC=%s\n' % str(mpc_data))
            mpci = MPC.add_op2_data((sid, nodes, components, coefficients))
            self._add_constraint_mpc_object(mpci)
            nentries += 1
        self.increase_card_count('MPC', nentries)
        return len(data)

    def _read_mpcadd(self, data, n):
        """
        MPCADD(4891,60,83) - Record 17
        """
        nentries = (len(data) - n) // 4
        datai = np.fromstring(data[n:], self.idtype)
        _read_spcadd_mpcadd(self, 'MPCADD', datai)
        return len(data)

    def _read_omit1(self, data, n):
        """OMIT1(4951,63,92) - Record 19"""
        self.log.info('skipping OMIT1 in GEOM4\n')
        return len(data)

    def _read_qset1(self, data, n):
        """QSET1(610,6,316) - Record 22"""
        #self.log.info('skipping QSET1 in GEOM4\n')
        #return len(data)
        return self._read_xset1(data, n, 'QSET1', QSET1, self._add_qset_object)

    def _read_rbar(self, data, n):
        """RBAR(6601,66,292) - Record 22"""
        n = self._read_dual_card(data, n, self._read_rbar_nx, self._read_rbar_msc,
                                 'RBAR', self._add_rigid_element_object)
        return n

    def _read_rbar_nx(self, data, n):
        """
        RBAR(6601,66,292) - Record 22 - NX version

        1 EID I Element identification number
        2 GA  I Grid point A identification number
        3 GB  I Grid point B identification number
        4 CNA I Component numbers of independent degrees-of-freedom at end A
        5 CNB I Component numbers of independent degrees-of-freedom at end B
        6 CMA I Component numbers of dependent degrees-of-freedom at end A
        7 CMB I Component numbers of dependent degrees-of-freedom at end B
        """
        s = Struct(b(self._endian + '7i'))
        ntotal = 28
        nelements = (len(data) - n) // ntotal
        assert (len(data) - n) % ntotal == 0
        elems = []
        for i in range(nelements):
            edata = data[n:n + ntotal]  # 8*4
            out = s.unpack(edata)
            if self.is_debug_file:
                self.binary_debug.write('  RBAR NX=%s\n' % str(out))
            (eid, ga, gb, cna, cnb, cma, cmb) = out
            out = list(out)
            out.append(0.)
            elem = RBAR.add_op2_data(out)
            elems.append(elem)
            #if self.is_debug_file:
                #self.binary_debug.write('	eid	ga	gb	cna	cnb	cma	cmb	alpha\n')
                #self.binary_debug.write(str(elem))
            n += ntotal
        return n, elems

    def _read_rbar_msc(self, data, n):
        """RBAR(6601,66,292) - Record 22 - MSC version"""
        s = Struct(b(self._endian + '7if'))
        ntotal = 32
        nelements = (len(data) - n) // ntotal
        assert (len(data) - n) % ntotal == 0
        elems = []
        for i in range(nelements):
            edata = data[n:n + ntotal]  # 8*4
            out = s.unpack(edata)
            if self.is_debug_file:
                self.binary_debug.write('  RBAR MSC=%s\n' % str(out))
            #(eid, ga, gb, cna, cnb, cma, cmb, alpha) = out
            elem = RBAR.add_op2_data(out)
            elems.append(elem)
            n += ntotal
        return n, elems

    def _read_rbe1(self, data, n):
        """
        RBE1(6801,68,294) - Record 23

        MSC/NX
        Word Name Type Description
        1 EID I Element identification number
        2 GN  I Grid point identification number for independent degrees-of-freedom
        3 CN  I Component numbers of independent degrees-of-freedom
        Words 2 through 3 repeat until (-2,-2) occurs

        4 GM  I Grid point identification number for dependent degrees-of-freedom
        5 CM  I Component numbers of dependent degreesof-freedom
        Words 4 through 5 repeat until (-1,-1) occurs

        6 ALPHA RS Thermal expansion coefficient
        7 UNDEF none Not used
        """
        idata = np.fromstring(data[n:], self.idtype)
        #fdata = np.fromstring(data[n:], self.fdtype)

        i = 0
        nelements = 0
        nfields = len(idata)
        while i < nfields:
            eid, gn, cn = idata[i:i+3]
            gni, cni = idata[i+3:i+5]
            Gni = [gn]
            Cni = [cn]
            while (gni, cni) != (-2, -2):
                print(eid, gn, cn, (gni, cni))
                Gni.append(gni)
                Cni.append(cni)
                i += 2
                gni, cni = idata[i+3:i+5]
                #print((gni, cni))
                #print('----')
            i += 2

            gmi, cmi = idata[i+3:i+5]
            #print("gmi,cmi=", gmi, cmi)
            Gmi = []
            Cmi = []
            while (gmi, cmi) != (-1, -1):
                Gmi.append(gmi)
                Cmi.append(cmi)
                i += 2
                gmi, cmi = idata[i+3:i+5]
            i += 5
            #print(idata[i+3:])
            #idata
            #print(idata[i:])
            rbe1 = self.add_rbe1(eid, Gni, Cni, Gmi, Cmi, alpha=0.)
            #print(rbe1)

            nelements += 1
        self.card_count['RBE1'] = nelements
        return len(data)

    def _read_rbe2(self, data, n):
        """
        RBE2(6901,69,295) - Record 24

        ::

          data = (1, 1, 123456, 10000, -1, 0.0,
                  2, 2, 123456, 20000, -1, 0.0,
                  3, 3, 12345,  30000, 30001, 30002, 30003, 30004, 30005, -1, 0.0,
                  4, 4, 123,    40000, 40001, 40010, 40011, 40020, 40021, 40030, 40031, 40040, 40041, 40050, 40051, -1, 0.0,
                  5, 5, 123,    50000, 50001, 50010, 50011, 50020, 50021, 50030, 50031, 50040, 50041, 50050, 50051, -1, 0.0)
        """
        idata = np.fromstring(data[n:], self.idtype)
        iminus1 = np.where(idata == -1)[0]
        if idata[-1] == -1:
            is_alpha = False
            i = np.hstack([[0], iminus1[:-1]+1])
            j = np.hstack([iminus1[:-1], len(idata)])
        else:
            is_alpha = True
            i = np.hstack([[0], iminus1[:-1]+1])
            fdata = np.fromstring(data[n:], self.fdtype)
            j = np.hstack([iminus1[:-1], len(idata)-2])

        #print('i=%s' % i)
        #print('j=%s' % j)
        #print('idata=%s' % idata)
        #print(fdata, len(fdata))
        nelements = len(j)
        if is_alpha:
            for ii, jj in zip(i, j):
                eid, gn, cm = idata[ii:ii + 3]
                gm = idata[ii+3:jj-1].tolist()
                #print('eid=%s gn=%s cm=%s gm=%s' % (eid, gn, cm, gm))
                #alpha = fdata[jj]
                alpha = fdata[jj+1]
                #print('eid=%s gn=%s cm=%s gm=%s alpha=%s' % (eid, gn, cm, gm, alpha))

                out = (eid, gn, cm, gm, alpha)
                if self.is_debug_file:
                    self.binary_debug.write('  RBE2=%s\n' % str(out))
                #print('  RBE2=%s\n' % str(out))
                elem = RBE2.add_op2_data(out)
                self._add_rigid_element_object(elem)
        else:
            alpha = 0.0
            for ii, jj in zip(i, j):
                #eid, gn, cm, gm1, gm2 = idata[ii:ii + 5]
                eid, gn, cm = idata[ii:ii + 3]
                gm = idata[ii+3:jj-1].tolist()

                out = (eid, gn, cm, gm, alpha)
                if self.is_debug_file:
                    self.binary_debug.write('  RBE2=%s\n' % str(out))
                #print('  RBE2=%s\n' % str(out))
                elem = RBE2.add_op2_data(out)
                self._add_rigid_element_object(elem)
        self.card_count['RBE2'] = nelements
        return n

        #while n < len(data):
            ## (eid, gn, cm, gm, ..., alpha)
            #out = s_msc.unpack(data[n:n+20])
            #eid, gn, cm, gm1, gm2 = out
            #n += 20

            #Gmi = [gm1, gm2]
            #while gm2 != -1:
                #gm2, = struct_i.unpack(data[n:n+4])
                #Gmi.append(gm2)
                #n += 4
            #Gmi = [gmi for gmi in Gmi if gmi != -1]

            ### TODO: according to the MSC/NX manual, alpha should be here,
            ###       but it's not...
            #alpha = 0.

            #if self.is_debug_file:
                #self.binary_debug.write('  RBE2=%s\n' % str(out))
            #print('  RBE2=%s\n' % str(out))
            #out = (eid, gn, cm, Gmi, alpha)
            #elem = RBE2.add_op2_data(out)
            #self._add_rigid_element_object(elem)
            #nelements += 1
        #self.card_count['RBE2'] = nelements
        #return n

    def _read_rbe3(self, data, n):
        """RBE3(7101,71,187) - Record 25"""
        idata = np.fromstring(data[n:], self.idtype)
        fdata = np.fromstring(data[n:], self.fdtype)
        read_rbe3s_from_idata_fdata(self, idata, fdata)
        return n

    def _read_rbjoint(self, data, n):
        self.log.info('skipping RBJOINT in GEOM4\n')
        return len(data)

    def _read_rbjstif(self, data, n):
        self.log.info('skipping RBJSTIF in GEOM4\n')
        return len(data)

    def _read_release(self, data, n):
        self.log.info('skipping RELEASE in GEOM4\n')
        return len(data)

    def _read_rpnom(self, data, n):
        self.log.info('skipping RPNOM in GEOM4\n')
        return len(data)

    def _read_rrod(self, data, n):
        """common method for reading RROD"""
        n = self._read_dual_card(data, n, self._read_rrod_nx, self._read_rrod_msc,
                                 'RROD', self._add_rigid_element_object)
        return n

    def _read_rrod_nx(self, data, n):
        """RROD(6501,65,291) - Record 30"""
        s = Struct(b(self._endian + '5i'))
        ntotal = 20
        nelements = (len(data) - n) // ntotal
        elements = []
        for i in range(nelements):
            edata = data[n:n + ntotal]
            out = s.unpack(edata)
            if self.is_debug_file:
                self.binary_debug.write('  RROD=%s\n' % str(out))
            (eid, ga, gb, cma, cmb) = out
            out = (eid, ga, gb, cma, cmb, 0.0) # alpha
            elem = RROD.add_op2_data(out)
            elements.append(elem)
            n += ntotal
        return n, elements

    def _read_rrod_msc(self, data, n):
        """RROD(6501,65,291) - Record 30"""
        s = Struct(b(self._endian + '5if'))
        ntotal = 24
        nelements = (len(data) - n) // ntotal
        elements = []
        for i in range(nelements):
            edata = data[n:n + ntotal]
            out = s.unpack(edata)
            if self.is_debug_file:
                self.binary_debug.write('  RROD=%s\n' % str(out))
            #(eid, ga, gb, cma, cmb, alpha) = out
            elem = RROD.add_op2_data(out)
            elements.append(elem)
            n += ntotal
        return n, elements

    def _read_rspline(self, data, n):
        """RSPLINE(7001,70,186) - Record 31"""
        self.log.info('skipping RSPLINE in GEOM4\n')
        return len(data)

    def _read_rsscon(self, data, n):
        """RSSCON(7201,72,398) - Record 32"""
        self.log.info('skipping RSSCON in GEOM4\n')
        return len(data)

    def _read_rweld(self, data, n):
        self.log.info('skipping RWELD in GEOM4\n')
        return len(data)

    def _read_sebset(self, data, n):
        self.log.info('skipping SEBSET in GEOM4\n')
        return len(data)

    def _read_sebset1(self, data, n):
        self.log.info('skipping SEBSET1 in GEOM4\n')
        return len(data)

    def _read_secset(self, data, n):
        self.log.info('skipping SECSET in GEOM4\n')
        return len(data)

    def _read_secset1(self, data, n):
        self.log.info('skipping SECSET1 in GEOM4\n')
        return len(data)

    def _read_seqset(self, data, n):
        """SEQSET(1110,11,321) - Record 40"""
        self.log.info('skipping SEQSET in GEOM4\n')
        return len(data)
        #return self._read_xset(data, n, 'SEQSET', SEQSET, self.add_SEQSET)

    def _read_seqset1(self, data, n):
        """
        SEQSET1(1210,12,322) - Record 41

        SEQSET1=(1, 0, 0, 700, -1,
                 2, 0, 0, 200, -1,
                 3, 0, 0, 300, -1,
                 4, 0, 0, 400, -1,
                 5, 0, 0, 500, -1,
                 6, 0, 0, 600)
        SEQSET1=[1   0   1 101 112
                 2   0   1 113 124]
        """
        return self._read_superxset1(data, n, 'SEQSET1', SEQSET1, self._add_seqset_object,
                                     debug=True)

    def _read_sesup(self, data, n):
        self.log.info('skipping SESUP in GEOM4\n')
        return len(data)

    def _read_seuset(self, data, n):
        self.log.info('skipping SEUSET in GEOM4\n')
        return len(data)

    def _read_seuset1(self, data, n):
        self.log.info('skipping SEUSET1 in GEOM4\n')
        return len(data)

    def _read_spcoff(self, data, n):
        """SPCOFF(5501,55,16) - Record 44"""
        ntotal = 16
        nentries = (len(data) - n) // ntotal
        for i in range(nentries):
            edata = data[n:n + 16]
            (sid, ID, c, dx) = unpack(b(self._endian + 'iiif'), edata)
            if self.is_debug_file:
                self.binary_debug.write('SPCOFF sid=%s id=%s c=%s dx=%s\n' % (sid, ID, c, dx))
            constraint = SPCOFF.add_op2_data([sid, ID, c, dx])
            self._add_constraint_spcoff_object(constraint)
            n += 16
        return n

    def _read_spc(self, data, n):
        """common method for reading SPCs"""
        n = self._read_dual_card(data, n, self._read_spc_nx, self._read_spc_msc,
                                 'SPC', self._add_constraint_spc_object)
        return n

    def _read_spc_msc(self, data, n):
        """SPC(5501,55,16) - Record 44

        1 SID   I    Set identification number
        2 ID    I    Grid or scalar point identification number
        3 C     I    Component numbers
        4 UNDEF none Not used
        5 D     RX   Enforced displacement
        """
        ntotal = 20
        nentries = (len(data) - n) // ntotal
        assert nentries > 0, nentries
        assert (len(data) - n) % ntotal == 0
        #self.show_data(data, types='if')

        constraints = []
        struc = Struct(b(self._endian + 'iiiif'))
        for i in range(nentries):
            edata = data[n:n + 20]
            (sid, nid, comp, xxx, dx) = struc.unpack(edata)
            assert xxx == 0, xxx
            if self.is_debug_file:
                self.binary_debug.write('SPC-MSC sid=%s id=%s comp=%s dx=%s\n' % (
                    sid, nid, comp, dx))
            assert comp != 7, 'SPC-MSC sid=%s id=%s comp=%s dx=%s\n' % (sid, nid, comp, dx)
            constraint = SPC.add_op2_data([sid, nid, comp, dx])
            constraints.append(constraint)
            n += 20
        return n, constraints

    def _read_spc_nx(self, data, n):
        """SPC(5501,55,16) - Record 44

        1 SID I  Set identification number
        2 ID  I  Grid or scalar point identification number
        3 C   I  Component numbers
        4 D   RS Enforced displacement
        """
        msg = ''
        ntotal = 16
        nentries = (len(data) - n) // ntotal
        assert nentries > 0, nentries
        assert (len(data) - n) % ntotal == 0
        #self.show_data(data, types='if')

        struc = Struct(b(self._endian + 'iiif'))
        constraints = []
        for i in range(nentries):
            edata = data[n:n + 16]
            (sid, nid, comp, dx) = struc.unpack(edata)
            if self.is_debug_file:
                self.binary_debug.write('SPC-NX sid=%s nid=%s comp=%s dx=%s\n' % (
                    sid, nid, comp, dx))

            assert comp != 7, 'SPC-NX sid=%s nid=%s comp=%s dx=%s\n' % (sid, nid, comp, dx)
            if nid < 100000000:
                constraint = SPC.add_op2_data([sid, nid, comp, dx])
                constraints.append(constraint)
                #msg += '  SPC-NX sid=%s nid=%s comp=%s dx=%s\n' % (sid, nid, comp, dx)
            else:
                msg += '  SPC-NX sid=%s nid=%s comp=%s dx=%s\n' % (sid, nid, comp, dx)
            n += 16
        if msg:
            self.log.warning('Invalid Node IDs; skipping\n' + msg)
        return n, constraints

    def _read_spcoff1(self, data, n):
        """
        SPCOFF1(6210, 62, 344) - Record
        see SPC1

        Record - SPC1(5481,58,12)
        Word Name Type Description
        1 SID I Set identification number  <------ removing...
        2 C I Component numbers
        3 THRUFLAG I Thru range flag
        THRUFLAG=0 No
        4 ID I Grid or scalar point identification number
        Word 4 repeats until End of Record
        THRUFLAG=1 Yes
        4 ID1 I First grid or scalar point identification number
        5 ID2 I Second grid or scalar point identification number
        End THRUFLAG

        Word Name Type Description
        1 C I Component numbers
        2 THRUFLAG I Thru range flag
        THRUFLAG=0 No
        3 ID I Grid or scalar point identification number
        Word 3 repeats until End of Record
        THRUFLAG=1 Yes
        3 ID1 I First grid or scalar point identification number
        4 ID2 I Second grid or scalar point identification number
        End THRUFLAG
        """
        #nentries = 0
        #nints = (len(data) - n) // 4
        idata = np.fromstring(data[n:], self.idtype)
        if not idata[-1] == -1:
            idata = np.hstack([idata, -1])
        iminus1 = np.where(idata == -1)[0]
        assert len(iminus1) > 0, idata

        i = np.hstack([[0], iminus1[:-1]+1])
        j = np.hstack([iminus1[:-1], -1])
        for ii, jj in zip(i, j):
            outi = idata[ii:jj]
            self._add_spcoff1_card(outi)
        return len(data)

    def _add_spcoff1_card(self, out):
        """helper method for ``_read_spcoff1``"""
        components, thru_flag = out[:2]
        if thru_flag == 0:  # repeat 4 to end
            nids = out[2:].tolist()
            thru_check = False
        elif thru_flag == 1:
            n1 = out[2]
            n2 = out[3]
            nids = list(range(n1, n2+1))
            thru_check = True
        else:
            raise NotImplementedError('SPCOFF1; thru_flag=%s' % thru_flag)

        assert -1 not in out, out.tolist()
        if self.is_debug_file:
            self.binary_debug.write('SPCOFF1: components=%s thru_flag=%s' % (
                components, thru_flag))
            self.binary_debug.write('   nids=%s\n' % str(nids))
        if len(nids) == 0:
            #self.log.warning('skipping SPC1 because its empty...%s' % out)
            return
        in_data = [components, nids]
        constraint = SPCOFF1.add_op2_data(in_data)
        self._add_constraint_spcoff_object(constraint)
        self.increase_card_count('SPCOFF1', 1)
        if thru_check and len(out) > 5:
            #card = out[5:]
            self._add_spcoff1_card(out[5:])

    def _read_spc1(self, data, n):
        r"""
        SPC1(5481,58,12) - Record 45

        odd case = (
            # sid, comp, thru_flag
            12, 12345, 0, 110039, 110040, 110041, 110042, 110043, 110044, 110045,
                          110046, 110047, 110048, 110049, -1,
            # sid, comp, thru_flag, ???
            12, 12345, 0, -1)

        F:\work\pyNastran\pyNastran\master2\pyNastran\bdf\test\nx_spike\out_acmsnnns.op2

        [1, 123456, 0, 31, 35, 39, 43, 47, 48, 53, 63, 64, 69, 70, 71, 72, -1,
         3, 456, 1, 1]
        TestOP2.test_op2_solid_bending_02_geom

        [123456, 456, 1, 5, 13,
         123456, 123456, 0, 22, 23, 24, 25, -1]
        TestOP2.test_op2_solid_shell_bar_01_geom
        """
        #nentries = 0
        #nints = (len(data) - n) // 4
        idata = np.fromstring(data[n:], self.idtype)
        if not idata[-1] == -1:
            idata = np.hstack([idata, -1])
        iminus1 = np.where(idata == -1)[0]
        assert len(iminus1) > 0, idata

        i = np.hstack([[0], iminus1[:-1]+1])
        j = np.hstack([iminus1[:-1], -1])
        for ii, jj in zip(i, j):
            outi = idata[ii:jj]
            self._add_spc1_card(outi)
        return len(data)

    def _add_spc1_card(self, out):
        """helper method for ``_read_spc1``"""
        sid, components = out[:2]
        thru_flag = out[2]
        if thru_flag == 0:  # repeat 4 to end
            nids = out[3:].tolist()
            thru_check = False
        elif thru_flag == 1:
            n1 = out[3]
            n2 = out[4]
            nids = list(range(n1, n2+1))
            thru_check = True
        else:
            raise NotImplementedError('SPC1; thru_flag=%s' % thru_flag)

        assert -1 not in out, out.tolist()
        if self.is_debug_file:
            self.binary_debug.write('SPC1: sid=%s components=%s thru_flag=%s' % (
                sid, components, thru_flag))
            self.binary_debug.write('   nids=%s\n' % str(nids))
        if len(nids) == 0:
            #self.log.warning('skipping SPC1 because its empty...%s' % out)
            return
        in_data = [sid, components, nids]
        constraint = SPC1.add_op2_data(in_data)
        self._add_constraint_spc_object(constraint)
        self.increase_card_count('SPC1', 1)
        if thru_check and len(out) > 5:
            #card = out[5:]
            self._add_spc1_card(out[5:])

    def _read_spcadd(self, data, n):
        """SPCADD(5491,59,13) - Record 46"""
        nentries = (len(data) - n) // 4
        datai = np.fromstring(data[n:], self.idtype)
        _read_spcadd_mpcadd(self, 'SPCADD', datai)
        return len(data)

    def _read_spcd(self, data, n):
        """common method for reading SPCDs"""
        n = self._read_dual_card(data, n, self._read_spcd_nx, self._read_spcd_msc,
                                 'SPCD', self._add_load_object)
        return n

    def _read_spcd_nx(self, data, n):
        """SPCD(5110,51,256) - NX specific"""
        s = Struct(b(self._endian + '3if'))
        ntotal = 16 # 4*4
        nentries = (len(data) - n) // ntotal
        assert nentries > 0, nentries
        assert (len(data) - n) % ntotal == 0
        constraints = []
        for i in range(nentries):
            edata = data[n:n + ntotal]
            #self.show_data(edata)
            out = s.unpack(edata)
            (sid, ID, c, dx) = out
            #print(out)
            if self.is_debug_file:
                self.binary_debug.write('  SPCD-NX=%s\n' % str(out))
            constraint = SPCD.add_op2_data([sid, ID, c, dx])
            constraints.append(constraint)
            n += ntotal
        return n, constraints

    def _read_spcd_msc(self, data, n):
        """
        SPCD(5110,51,256) - MSC specific - Record 47

        Word Name Type Description
        1 SID   I    Superelement identification number
        2 ID    I    Grid or scalar point identification number
        3 C     I    Component numbers
        4 UNDEF none Not used
        5 D     RX   Enforced displacement
        """
        s = Struct(b(self._endian + '4if'))
        ntotal = 20 # 5*4
        nentries = (len(data) - n) // ntotal
        assert nentries > 0, nentries
        assert (len(data) - n) % ntotal == 0
        constraints = []
        for i in range(nentries):
            edata = data[n:n + ntotal]
            out = s.unpack(edata)
            (sid, ID, c, xxx, dx) = out
            assert xxx == 0, xxx

            if self.is_debug_file:
                self.binary_debug.write('  SPCD-MSC=%s\n' % str(out))
            constraint = SPCD.add_op2_data([sid, ID, c, dx])
            constraints.append(constraint)
            n += ntotal
        return n, constraints

    def _read_spcde(self, data, n):
        self.log.info('skipping SPCDE in GEOM4\n')
        return len(data)

    def _read_spcf(self, data, n):
        self.log.info('skipping SPCDF in GEOM4\n')
        return len(data)

    def _read_spcdg(self, data, n):
        self.log.info('skipping SPCDG in GEOM4\n')
        return len(data)

    def _read_spce(self, data, n):
        self.log.info('skipping SPCE in GEOM4\n')
        return len(data)

    def _read_spceb(self, data, n):
        self.log.info('skipping SPCEB in GEOM4\n')
        return len(data)

    def _read_spcfb(self, data, n):
        self.log.info('skipping SPCFB in GEOM4\n')
        return len(data)

    def _read_spcgb(self, data, n):
        self.log.info('skipping SPCGB in GEOM4\n')
        return len(data)

    def _read_spcgrid(self, data, n):
        self.log.info('skipping SPCGRID in GEOM4\n')
        return len(data)

    def _read_suport(self, data, n):
        """SUPORT(5601,56, 14) - Record 59"""
        nentries = (len(data) - n) // 8 # 2*4
        s = Struct(b(self._endian + '2i'))
        for i in range(nentries):
            out = list(s.unpack(data[n:n + 8]))
            if self.is_debug_file:
                self.binary_debug.write('  SUPORT=%s\n' % str(out))
                #self.log.info(out)
            suport = SUPORT.add_op2_data(out)
            self._add_suport_object(suport) # extracts [sid, c]
            n += 8
        return n

    def _read_suport1(self, data, n):
        """SUPORT1(10100,101,472) - Record 60"""
        nfields = (len(data) - n) // 4 - 2
        out = unpack(b(self._endian + '%ii' % nfields), data[n:n+nfields*4])

        i = 0
        nsuports = 0
        suport = []
        while i < len(out):
            if out[i] == -1:
                assert out[i+1] == -1, out
                suporti = SUPORT1.add_op2_data(suport)
                #self.log.info(suporti)
                self._add_suport_object(suporti) # extracts [sid, nid, c]
                nsuports += 1
                if self.is_debug_file:
                    self.binary_debug.write('  SUPORT1=%s\n' % str(suport))
                suport = []
                i += 2
                continue
            suport.append(out[i])
            i += 1
            assert -1 not in suport, suport

        if self.is_debug_file:
            self.binary_debug.write('  SUPORT1=%s\n' % str(suport))

        suporti = SUPORT1.add_op2_data(suport)
        self._add_suport_object(suporti) # extracts [sid, nid, c]
        nsuports += 1
        self.card_count['SUPOT1'] = nsuports
        assert n+nfields*4+8 == len(data), 'a=%s b=%s' % (n+nfields*4+8, len(data))
        return len(data)

    def _read_tempbc(self, data, n):
        self.log.info('skipping TEMPBC in GEOM4\n')
        return len(data)

    def _read_uset(self, data, n):
        """
        USET(2010,20,193) - Record 63
        (sid, nid, comp), ...
        """
        s = Struct(b(self._endian + '3i'))
        ntotal = 12
        #self.show_data(data, types='is')
        nelements = (len(data) - n) // ntotal
        for i in range(nelements):
            edata = data[n:n + ntotal]
            out = s.unpack(edata)
            if self.is_debug_file:
                self.binary_debug.write('  USET=%s\n' % str(out))
            #(sid, id, component) = out
            set_obj = USET.add_op2_data(out)
            self._add_uset_object(set_obj)
            n += ntotal
        self.increase_card_count('USET', len(self.usets))
        return n

    def _read_uset1(self, data, n):
        """USET1(2110,21,194) - Record 65

        odd case = (
            # sid, comp, thru_flag
            12, 12345, 0, 110039, 110040, 110041, 110042, 110043, 110044, 110045,
                          110046, 110047, 110048, 110049, -1,
            # sid, comp, thru_flag, ???
            12, 12345, 0, -1)
        """
        nentries = 0
        nints = (len(data) - n) // 4
        idata = unpack('%s%ii' % (self._endian, nints), data[n:])
        i = 0
        #print('idata = %s' % idata)
        nidata = len(idata)
        while i < nidata:
            sname = data[n+i*(4) : n+(i+1)*4]
            sname_str = unpack('4s', sname)
            #print('sname_str = %r' % sname_str)
            comp, thru_flag = idata[i+1:i+3]
            i += 3
            if thru_flag == 0:  # repeat 4 to end
                nid = idata[i]
                nids = [nid]
                i += 1
                if i == nidata:
                    break
                while idata[i] != -1:
                    nid = idata[i]
                    nids.append(nid)
                    i += 1
                i += 1
            elif thru_flag == 1:
                n1, n2 = idata[i:i+2]
                nids = list(range(n1, n2+1))
                i += 2
            else:
                raise NotImplementedError('USET1; thru_flag=%s' % thru_flag)

            if self.is_debug_file:
                self.binary_debug.write('USET1: sname=%s comp=%s thru_flag=%s' % (
                    sname_str, comp, thru_flag))
                self.binary_debug.write('   nids=%s\n' % str(nids))
            #print('SPC1: sid=%s comp=%s thru_flag=%s' % (
            #    sid, comp, thru_flag))
            #print('   nids=%s\n' % str(nids))
            in_data = [sname_str, comp, nids]

            constraint = USET1.add_op2_data(in_data)
            self._add_uset_object(constraint)
        self.card_count['USET1'] = nentries
        return len(data)


    def _read_omit(self, data, n):
        self.log.info('skipping OMIT in GEOM4\n')
        return len(data)

    def _read_rtrplt(self, data, n):
        self.log.info('skipping RTRPLT in GEOM4\n')
        return len(data)

    def _read_bndfix(self, data, n):
        self.log.info('skipping BNDFIX in GEOM4\n')
        return len(data)

    def _read_bndfix1(self, data, n):
        self.log.info('skipping BNDFIX1 in GEOM4\n')
        return len(data)

    def _read_bndfree(self, data, n):
        self.log.info('skipping BNDFREE in GEOM4\n')
        return len(data)

    def _read_bltmpc(self, data, n):
        self.log.info('skipping BLTMPC in GEOM4\n')
        return len(data)

def read_rbe3s_from_idata_fdata(self, idata, fdata):
    """
    1 EID   I Element identification number
    2 REFG  I Reference grid point identification number
    3 REFC  I Component numbers at the reference grid point

    4 WT1  RS Weighting factor for components of motion at G
    5 C     I Component numbers
    6 G     I Grid point identification number
    Word 6 repeats until -1 occurs

    Words 4 through 6 repeat until -2 occurs

    7 GM    I Grid point identification number for dependent degrees-of-freedom
    8 CM    I Component numbers of dependent degrees-of-freedom

    Words 7 through 8 repeat until -3 occurs

    data = [99           99 123456 1.0    123    44    45  48  49  -1    -3]
    data = [61           71 123456 1.0    123    70    75  77      -1    -3
            62           71 123456 1.0    123    58    59  72      -1    -3]
    data = [1001100 1001100 123456 1.0 123456 10011 10002          -1 -2 -3
            1002500 1002500 123456 1.0 123456 10025 10020          -1 -2 -3]
            eid     refg    refc   wt  c      g     ...
    data = [107, 1, 123456, 1.0, 1234, 10600, 10601, -1, -2, -3, 0/0.0,
            207, 2, 123456, 1.0, 1234, 20600, 20601, -1, -2, -3, 0/0.0,
            307, 3, 123456, 1.0, 1234, 30600, 30601, -1, -2, -3, 0/0.0]]
    """
    rbe3s = []

    #iminus1 = np.where(idata == -1)[0]
    #iminus2 = np.where(idata == -2)[0]
    #assert len(iminus1) == 1, idata
    #assert len(iminus2) == 1, idata
    #assert len(iminus3) == 1, idata

    iminus3 = np.where(idata == -3)[0]
    if idata[-1] == -3:
        is_alpha = False
        i = np.hstack([[0], iminus3[:-1]+1])
    else:
        is_alpha = True
        i = np.hstack([[0], iminus3[:-1]+2])
    j = np.hstack([iminus3[:-1], len(idata)])

    #print('idata = %s' % idata.tolist())
    #print('fdata = %s' % fdata.tolist())
    #print('i = %s' % i.tolist())
    #print('j = %s' % j.tolist())
    #print('is_alpha = %s' % is_alpha)
    assert len(i) == len(j)
    for ii, jj in zip(i, j):

        idatai = idata[ii:jj]
        eid, refg, refc, dummy, comp, grid = idatai[:6]
        weight = fdata[ii+3]
        weights = [weight]
        comps = [comp]
        gijs = [grid]
        #print('eid=%s refg=%s refc=%s weight=%s comp=%s grid=%s' % (
            #eid, refg, refc, weight, comp, grid))

        while 1:
            weight = fdata[ii + 3]
            comp = idata[ii + 4]
            grid = idata[ii + 5]
            #print('weight=%s comp=%s grid=%s' % (
                #weight, comp, grid))
            #if idata[ii + 6] in [-2, -3]:
                #break
            while idata[ii + 6] > 0:
                grid = idata[ii+6]
                #print('  gridi =', grid)
                #print('  ii+6=%s gridi=%s extra=%s' % (ii+6, grid, idata[ii+6:jj+1].tolist()))
                gijs.append(grid)
                ii += 1
            #print('ii = ', ii)
            #print('idata[ii+6:] =', idata[ii+6:].tolist())
            if idata[ii+6] == -3:
                break
            assert idata[ii+6] == -1, idata[ii+6:]
            ii += 1 # -1
            if idata[ii+6] == -2:
                ii += 1 # -2
                break

        gmi = []
        cmi = []
        if idata[ii+6] != -3:
            # gm/cm
            #print('idata[ii+6]*', idata[ii+6])
            #print('idata[ii+7]*', idata[ii+7])
            #print('end = ', idata[ii+6:jj+1].tolist())

            while idata[ii+6] != -3:
                gm = idata[ii+6]
                cm = idata[ii+7]
                #print('  gm=%s cm=%s' % (gm, cm))
                gmi.append(gm)
                cmi.append(cm)
                ii += 2

        if is_alpha:
            alpha = fdata[ii]
            ii += 1
        else:
            alpha = 0.0
        #print('alpha = %s' % alpha)
        in_data = [eid, refg, refc, weights, comps, gijs,
                   gmi, cmi, alpha]
        if self.is_debug_file:
            self.binary_debug.write('  RBE3=%s\n' % str(in_data))
        #print('rbe3 =', in_data)
        rbe3 = RBE3.add_op2_data(in_data)

        self._add_rigid_element_object(rbe3)
        rbe3s.append(rbe3)
        #print('--------------------------------------')
    return rbe3s

def _read_spcadd_mpcadd(model, card_name, datai):
    """
    reads a SPCADD/MPCADD card

    Word Name Type Description
    1 SID I Set identification number
    2 S   I Set identification number
    Word 2 repeats until End of Record
    """
    if model.is_debug_file:
        model.binary_debug.write('  %s - %s' % (card_name, str(datai)))
    iend = np.where(datai == -1)[0]
    i0 = 0
    count_num = len(iend)
    for iendi in iend:
        dataii = datai[i0:iendi]
        #print('dataii = ', dataii)
        i0 = iendi + 1

        assert -1 not in dataii, dataii

        #print('%r %s' % (card_name, dataii))
        if card_name == 'MPCADD':
            constraint = MPCADD.add_op2_data(dataii)
            model._add_constraint_mpcadd_object(constraint)
        else:
            constraint = SPCADD.add_op2_data(dataii)
            model._add_constraint_spcadd_object(constraint)
    model.increase_card_count(card_name, count_num=count_num)
