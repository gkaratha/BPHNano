import FWCore.ParameterSet.Config as cms
from PhysicsTools.NanoAOD.common_cff import *

########################### Selections ###########################

JpsiToMuMu = cms.EDProducer(
    'DiMuonBuilder',
    src = cms.InputTag('muonBPH', 'SelectedMuons'),
    transientTracksSrc = cms.InputTag('muonBPH', 'SelectedTransientMuons'),
    lep1Selection = cms.string('pt > 4.0 && abs(eta) < 2.4 && isLooseMuon && isGlobalMuon'),
    lep2Selection = cms.string('pt > 3.0 && abs(eta) < 2.4 && isLooseMuon && isGlobalMuon'),
    preVtxSelection  = cms.string('abs(userCand("l1").vz - userCand("l2").vz) <= 1.'
                                  '&& 2.8 < mass() && mass() < 3.4 '
                                  '&& charge() == 0'
                                  '&& userFloat("lep_deltaR") > 0.03'),
    postVtxSelection = cms.string('2.9 < userFloat("fitted_mass") && userFloat("fitted_mass") < 3.3'
                                  '&& userFloat("sv_prob") > 0.001')
)

CountDiMuonBPH = cms.EDFilter("PATCandViewCountFilter",
    minNumber = cms.uint32(1),
    maxNumber = cms.uint32(999999),
    src = cms.InputTag("JpsiToMuMu:SelectedDiLeptons")
)  

########################### Tables ###########################

JpsiToMuMuTable = cms.EDProducer("SimpleCandidateFlatTableProducer",
    src = cms.InputTag("JpsiToMuMu:SelectedDiLeptons"),
    cut = cms.string(""), #we should not filter on cross linked collections
    name = cms.string("JpsiToMuMu"),
    doc  = cms.string("Dilepton collections"),
    singleton = cms.bool(False), # the number of entries is variable
    extension = cms.bool(False), # this is the main table for the muons
    variables = cms.PSet(CandVars,
          fitted_mass = Var("userFloat('fitted_mass')", float, doc="Fitted dilepton mass", precision=10),
          svprob = Var("userFloat('sv_prob')", float, doc="Vtx fit probability", precision=10),
          vtx_x =Var("userFloat('vtx_x')", float, doc="Vtx position in x", precision=10),
          vtx_y = Var("userFloat('vtx_y')", float, doc="Vtx position in y", precision=10),
          vtx_z = Var("userFloat('vtx_z')", float, doc="Vtx position in y", precision=10),

    )
)

JpsiToMuMuSequence = cms.Sequence(JpsiToMuMu)
JpsiToMuMuTables = cms.Sequence(JpsiToMuMuTable)
