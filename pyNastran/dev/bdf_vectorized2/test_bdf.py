"""tests the vectorized BDF class before being used by the GUI"""
from __future__ import print_function
import os
import unittest
import numpy as np
import pyNastran
from pyNastran.bdf.bdf import read_bdf
from pyNastran.dev.bdf_vectorized2.bdf_vectorized import read_bdf as read_bdfv

PKG_PATH = pyNastran.__path__[0]
MODEL_PATH = os.path.join(PKG_PATH, '../', 'models')


class TestVectorized(unittest.TestCase):
    def test_solid_bending(self):
        """tests solid_bending"""
        bdf_filename = os.path.join(MODEL_PATH, 'solid_bending', 'solid_bending.bdf')
        model = read_bdfv(bdf_filename, validate=True, xref=False, punch=False,
                          skip_cards=None, encoding=None, log=None, debug=True,
                          mode='msc')
        #print(model.get_bdf_stats())

        #model.grids[10] = GRID(10, [0., 0., 0.])
        print(model.grid)
        print(model.grid[10]) # nid or index?
        print(model.grid.get_by_nid(10))
        out_filename = 'spike.bdf'
        model.write_bdf(out_filename, encoding=None, size=8, is_double=False,
                        interspersed=False, enddata=None,
                        close=True)

    def test_bwb(self):
        """tests bwb"""
        bdf_filename = os.path.join(MODEL_PATH, 'bwb', 'BWB_saero.bdf')
        model = read_bdfv(bdf_filename, validate=True, xref=False, punch=False,
                          skip_cards=None, encoding=None, log=None, debug=True,
                          mode='msc')
        #print(model.get_bdf_stats())

        out_filename = 'spike.bdf'
        model.write_bdf(out_filename, encoding=None, size=8, is_double=False,
                        interspersed=False, enddata=None,
                        close=True)

    def test_isat(self):
        """tests isat"""
        bdf_filename = os.path.join(MODEL_PATH, 'iSat', 'ISat_Dploy_Sm.dat')
        out_filename_v = 'spike_v.bdf'
        out_filename_nv = 'spike_nv.bdf'
        modelv = read_bdfv(bdf_filename, validate=True, xref=False, punch=False,
                           skip_cards=None, encoding=None, log=None, debug=True,
                           mode='msc')
        #print(model.get_bdf_stats())
        modelv.write_bdf(out_filename_v, encoding=None, size=8, is_double=False,
                         interspersed=False, enddata=None,
                         close=True)
        print(modelv.cbush)
        print(modelv.get_bdf_stats())
        print(modelv.elements)
        print(modelv.elements2)

        model_nv = read_bdf(bdf_filename, validate=True, xref=True, punch=False,
                            skip_cards=None, encoding=None, log=None, debug=True,
                            mode='msc')
        model_nv.write_bdf(out_filename_nv, encoding=None, size=8, is_double=False,
                           interspersed=False, enddata=None,
                           close=True)

        model1 = read_bdf(out_filename_v, validate=True, xref=True, punch=False,
                          skip_cards=None, encoding=None, log=None, debug=True,
                          mode='msc')
        model2 = read_bdf(out_filename_nv, validate=True, xref=True, punch=False,
                          skip_cards=None, encoding=None, log=None, debug=True,
                          mode='msc')

        #xyz_cid1, nid_cp_cd1 = model1.get_xyz_in_coord(cid=0, fdtype='float32')
        #xyz_cid2, nid_cp_cd2 = model2.get_xyz_in_coord(cid=0, fdtype='float32')

        out1 = model1.get_displacement_index_xyz_cp_cd(
            fdtype='float64', idtype='int32', sort_ids=True)
        icd_transform1, icp_transform1, xyz_cp1, nid_cp_cd1 = out1
        xyz_cid1 = model1.transform_xyzcp_to_xyz_cid(
            xyz_cp1, nid_cp_cd1[:, 0], icp_transform1, cid=0,
            in_place=False)

        out2 = model2.get_displacement_index_xyz_cp_cd(
            fdtype='float64', idtype='int32', sort_ids=True)
        icd_transform2, icp_transform2, xyz_cp2, nid_cp_cd2 = out2
        xyz_cid2 = model2.transform_xyzcp_to_xyz_cid(
            xyz_cp2, nid_cp_cd2[:, 0], icp_transform2, cid=0,
            in_place=False)

        assert np.array_equal(nid_cp_cd1, nid_cp_cd2)
        assert len(icp_transform1) == len(icp_transform2)
        assert len(icd_transform1) == len(icd_transform2)
        for icp1, icp2 in zip(icp_transform1, icp_transform2):
            assert np.array_equal(icp_transform1[icp1], icp_transform2[icp2])
        #assert np.array_equal(icp_transform1, icp_transform2)
        for icd1, icd2 in zip(icd_transform1, icd_transform2):
            assert np.array_equal(icd_transform1[icd1], icd_transform2[icd2])
        assert len(model1.nodes) == len(model2.nodes)
        for nid in model1.nodes:

            if not np.allclose(model1.nodes[nid].xyz, model2.nodes[nid].xyz):
                msg = 'nid=%s xyz1=%s xyz2=%s' % (nid, model1.nodes[nid].xyz, model2.nodes[nid].xyz)
                print(msg)
                #raise RuntimeError(msg)
        #assert np.array_equal(xyz_cp1, xyz_cp2)
        #assert np.array_equal(xyz_cid1, xyz_cid2)
        for nid, xyz1, xyz2 in zip(nid_cp_cd1[:, 0], xyz_cid1, xyz_cid2):
            if not np.allclose(xyz1, xyz2):
                print('xyz_cid0: nid=%s xyz1=%s xyz2=%s' % (nid, xyz1, xyz2))


    def test_static_elements(self):
        """tests static_elements"""
        bdf_filename = os.path.join(MODEL_PATH, 'elements', 'static_elements.bdf')
        model = read_bdfv(bdf_filename, validate=True, xref=False, punch=False,
                          skip_cards=None, encoding=None, log=None, debug=True,
                          mode='msc')

        print(model.cquad4)
        print(model.ctria3)
        print(model.shells)
        print(model.solids)
        print(model.elements)

        print(model.ctetra4)
        print(model.cpenta6)
        print(model.chexa8)
        print(model.cpyram5)
        print(model.ctetra10)
        print(model.cpenta15)
        print(model.chexa20)
        print(model.cpyram13)

        print(model.celas1)
        print(model.celas2)
        print(model.celas3)
        print(model.celas4)

        print(model.cdamp1)
        print(model.cdamp2)
        print(model.cdamp3)
        print(model.cdamp4)

        print(model.conrod)
        print(model.crod)
        print(model.ctube)

        print(model.elements2)
        len(model.elements2)
        #print(model.load_combinations)
        print(model.loads)
        print(model.get_bdf_stats())

        out_filename = 'spike.bdf'
        model.write_bdf(out_filename, encoding=None, size=8, is_double=False,
                        interspersed=False, enddata=None,
                        close=True)
        model.write_bdf(out_filename, encoding=None, size=16, is_double=False,
                        interspersed=False, enddata=None,
                        close=True)

if __name__ == '__main__':  # pragma: no cover
    unittest.main()
