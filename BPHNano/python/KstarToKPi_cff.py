import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

KstarToPiK = cms.EDProducer(
    'DiTrackBuilder',
    tracks = cms.InputTag('tracksBPH', 'SelectedTracks'),
    transientTracks = cms.InputTag('tracksBPH', 'SelectedTransientTracks'),
    trk1Selection   = cms.string(''),
    trk2Selection   = cms.string(''),
    trk1Mass = cms.double(0.139),
    trk2Mass = cms.double(0.494),
    preVtxSelection = cms.string('abs(userCand("l1").vz - userCand("l2").vz) <= 0.5 '
                                 '&& mass() > 0.889 && mass() < 0.895'
                                 '&& charge() == 0'),
    postVtxSelection =  cms.string('userFloat("fitted_mass") > 0.889 && userFloat("fitted_mass") < 0.895'
                                   '&& userFloat("sv_prob") > 0.01')
)

CountKstarPiK = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
    src       = cms.InputTag("KstarToPiK")
)  

KstarToPiKTable = cms.EDProducer("SimpleCompositeCandidateFlatTableProducer",
    src  = cms.InputTag("KstarToPiK"),
    cut  = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("KstarToPiK"),
    doc  = cms.string("slimmedMuons for BPark after basic selection"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the muons
    variables = cms.PSet(
        CandVars,
        fitted_mass = Var("userFloat('fitted_mass')", float, doc=""),
        fitted_pt   = Var("userFloat('fitted_pt')", float, doc=""),
        fitted_eta  = Var("userFloat('fitted_eta')", float, doc=""),
        fitted_phi  = Var("userFloat('fitted_phi')", float, doc=""),
        svprob      = Var("userFloat('sv_prob')", float, doc=""),
        trk1_mass   = Var("userFloat('trk1_mass')", float, doc=""),
        trk2_mass   = Var("userFloat('trk2_mass')", float, doc=""),
        trk1_idx    = Var("userInt('trk1_idx')", int, doc=""),
        trk2_idx    = Var("userInt('trk2_idx')", int, doc=""),
        second_mass_hypothesis = Var("userInt('second_mass_hypothesis')", int, doc=""),
        vtx_x       = Var("userFloat('vtx_x')", float, doc=""),
        vtx_y       = Var("userFloat('vtx_y')", float, doc=""),
        vtx_z       = Var("userFloat('vtx_z')", float, doc=""),     
    )
)

KstarPiKSequence = cms.Sequence(KstarToPiK)
KstarPiKTables   = cms.Sequence(KstarToPiKTable)
