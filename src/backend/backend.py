# -*- coding: utf-8 -*-
import axisvm.com.tlb as axtlb
from axisvm.com.tlb import RSurfaceAttr, lnlTensionAndCompression, \
    RResistancesXYZ, schLinear, stPlate, RElasticFoundationXYZ, \
    RNonLinearityXYZ, dofPlateXY, lgtStraightLine, RLineGeomData, \
    RLoadDomainPolyArea, dtGlobal, ldtConst, RResistances, RNonLinearity, \
    RStiffnesses, dsGlobal, ndcEuroCode
import numpy as np


def build(axapp, *args, material, size, 
          thickness, load, support, **kwargs):
    axapp.Models.New()  # cleans everything up
    axmodel = axapp.Models[1]
    
    axmodel.Settings.NationalDesignCode = ndcEuroCode
    matId = axmodel.Materials.AddFromCatalog(ndcEuroCode, material) 
    
    # define coordinates
    # the plate is in the x-y plane
    # the origo is located at the left bottom corner
    Lx, Ly = size
    coords = np.zeros((4, 3))  # we have four points in 3d space
    coords[0, :] = 0., 0., 0.
    coords[1, :] = Lx, 0., 0.
    coords[2, :] = Lx, Ly, 0.
    coords[3, :] = 0., Ly, 0. 
    
    # add nodes
    fnc = axmodel.Nodes.AddWithDOF
    nodeIDs = list(map(lambda c: fnc(*c, dofPlateXY), coords))
    
    # add lines
    nodes_of_lines = [[0, 1], [1, 2], [2, 3], [3, 0]]
    LineGeomType = lgtStraightLine
    lineIDs = []
    for line in nodes_of_lines:
        lineIDs.append(axmodel.Lines.Add(nodeIDs[line[0]], 
                                         nodeIDs[line[1]],
                       LineGeomType, RLineGeomData())[1])
        
    # add domain
    sattr = RSurfaceAttr(
        Thickness=thickness,
        SurfaceType=stPlate,
        RefZId=0,
        RefXId=0,
        MaterialId=matId,
        ElasticFoundation=RElasticFoundationXYZ(0, 0, 0),
        NonLinearity=RNonLinearityXYZ(lnlTensionAndCompression,
                                      lnlTensionAndCompression,
                                      lnlTensionAndCompression),
        Resistance=RResistancesXYZ(0, 0, 0),
        Charactersitics=schLinear
        )
    axmodel.Domains.Add(LineIds=lineIDs, SurfaceAttr=sattr)
    
    # add path load
    # origo is located at the left bottom corner
    xc, yc, w, h, q = load['xc'], load['yc'], load['w'], load['h'], load['q']
    patchlines = axapp.ObjectCreator.NewLines3d()
    patchline1 = axtlb.RLine3d(
        LineType=axtlb.ltStraightLine3d,
        P1=axtlb.RPoint3d(xc-w/2, yc-h/2, 0),
        P2=axtlb.RPoint3d(xc+w/2, yc-h/2, 0)
    )
    patchline2 = axtlb.RLine3d(
        LineType=axtlb.ltStraightLine3d,
        P1=axtlb.RPoint3d(xc+w/2, yc-h/2, 0),
        P2=axtlb.RPoint3d(xc+w/2, yc+h/2, 0)
    )
    patchline3 = axtlb.RLine3d(
        LineType=axtlb.ltStraightLine3d,
        P1=axtlb.RPoint3d(xc+w/2, yc+h/2, 0),
        P2=axtlb.RPoint3d(xc-w/2, yc+h/2, 0)
    )
    patchline4 = axtlb.RLine3d(
        LineType=axtlb.ltStraightLine3d,
        P1=axtlb.RPoint3d(xc-w/2, yc+h/2, 0),
        P2=axtlb.RPoint3d(xc-w/2, yc-h/2, 0)
    )
    patchlines.Add(patchline1)
    patchlines.Add(patchline2)
    patchlines.Add(patchline3)
    patchlines.Add(patchline4)
    RectPatch = RLoadDomainPolyArea(
        LoadCaseId=1,
        DistributionType=dtGlobal,
        LoadDistributionType=ldtConst,
        Component=2,  # z direction
        P1=q,
        WindowLoad=True
    )
    axmodel.Loads.AddDomainPolyArea(patchlines, RectPatch)
    
    # add supports
    NonLinearity = RNonLinearity(
        x=lnlTensionAndCompression,
        y=lnlTensionAndCompression,
        z=lnlTensionAndCompression,
        xx=lnlTensionAndCompression,
        yy=lnlTensionAndCompression,
        zz=lnlTensionAndCompression
    )
    Resistances = RResistances(
        x=0, y=0, z=0,
        xx=0, yy=0, zz=0
    )
    for i, edge in enumerate(['bottom', 'right', 'top', 'left']):
        Stiffnesses = RStiffnesses(**support[edge])
        axmodel.LineSupports.AddEdgeRelative(Stiffnesses, NonLinearity,
                                             Resistances, i+1, 0, 0, 1, 0)


def generate_mesh(axapp, *args, meshsize, **kwargs):
    with axapp.Models[1] as axmodel:
        # mesh
        MeshParams = axtlb.RDomainMeshParameters(
            MeshSize=meshsize,
            MeshType=axtlb.mtUniform,
            MeshGeometryType=axtlb.mgtTriangle,
            IsFitToPointLoad=True,
            FitToPointLoad=0.,  # fit to all loads
            IsFitToSurfaceLoad=True,
            FitToSurfaceLoad=0.,  # fit to all loads
        )
        axmodel.Domains[:].GenerateMesh(MeshParams)
        
    with axapp.Models[1] as axmodel:
        nIDs = [i+1 for i in range(len(axmodel.Nodes))]
        
        # coordinates of the nodes as a numpy array
        coords = axmodel.Nodes.BulkGetCoord(nIDs)[0]
        coords = np.array([[n.x, n.y, n.z] for n in coords])

        # get the topology as a numpy array
        def fnc(i): return axmodel.Surfaces.Item[i].GetContourPoints()[0]
        sIDs = axmodel.Domains[1].MeshSurfaceIds
        topo = np.vstack(list(map(fnc, sIDs))) - 1
    
    return coords, topo


def calculate(axapp, *args, filename, **kwargs):
    with axapp.Models[1] as axmodel:
        # calculate
        axmodel.SaveToFile(filename, False)
        axmodel.Calculation.LinearAnalysis(
            axtlb.cuiNoUserInteractionWithAutoCorrectNoShow)


def get_results(axapp):
    axmodel = axapp.Models[1]
       
    # IDs of all the nodes in the model
    N = axmodel.Nodes.Count
    res2d = np.zeros((3, N))

    # get displacement results
    disps = axmodel.Results.Displacements
    disps.DisplacementSystem = dsGlobal
    disps.LoadCaseId = 1
    disps.LoadLevelOrModeShapeOrTimeStep = 1
    dres = disps.AllNodalDisplacementsByLoadCaseId()[0][:N]
    def fnc_ez(dres): return dres.ez
    def fnc_rotx(dres): return dres.Fx
    def fnc_roty(dres): return dres.Fy
    res2d[0, :] = np.array(list(map(fnc_ez, dres)))
    res2d[1, :] = np.array(list(map(fnc_rotx, dres)))
    res2d[2, :] = np.array(list(map(fnc_roty, dres)))
    del dres