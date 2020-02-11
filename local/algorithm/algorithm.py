from ROOT import *
from sys import argv
from objects import *
from config import config

#----Algorithm----#
def ClusterCalorimeter(jetlist,towers):
    DrawGrid(towers,'calo')
    for iphi in irange(1,72,24):
        center = getKey(iphi,1)
        gct = getGCTTowers(center,towers)
        if config.debug: print "Clustering GCT %s" % center
        ClusterGCT(jetlist,gct)
def ClusterGCT(jetlist,towers):
    for ieta in irange(2,34,4):
        for iphi in irange(6,26,4):
            center = getKey(iphi,ieta)
            jet = Jet()
            t22 = get22x22Towers(center,towers)
            if config.debug: print "-Clustering 22x22 Jet %s" % center
            DrawGrid(towers,'gct',box=(iphi+0.5,ieta-0.5,3.0,3.0))
            Cluster22x22(jet,t22)
            if jet.et > 0:
                jetlist.append(jet)
def Cluster22x22(jet,towers):
    max_tower = getMaxTowerIn4x4('1112',towers)
    if max_tower['key'] == -1: return
    seed = towers[max_tower['key']]
    if config.debug: print "--Max Tower %s" % str(seed)
    DrawGrid(towers,"t22",pause=True)
    if max_tower['et'] < 2.5: return
    t19 = get19x19Towers(max_tower['key'],towers)

    check = getMaxTowerIn7x7('1010',t19)
    check_seed = t19[check['key']]
    if (check_seed != seed): return
    if config.debug: print "--Found Jet Seed %s" % str(seed)
    Cluster19x19(jet,t19)
def Cluster19x19(jet,towers):
    #--Overlap Handling needs to be done here--#
    DrawGrid(towers,"t19",pause=True)
    t7 = get7x7Towers('1010',towers)
    Cluster7x7(jet,t7)
def Cluster7x7(jet,towers):
    seed = towers['404']
    jet.seed(seed)
    for key,tower in towers.iteritems():
        if key == '404': continue
        jet.add(tower)
    if config.debug: print '---Clustered Jet %s\n' % str(jet)
   
#----Helper Methods----# 
def getGCTTowers(center_key,towers):
    subset = {}
    cphi,ceta = getPhiEta(center_key)
    dphi,deta = cphi - 6,ceta - 2
    for ieta in irange(1,34):
        for iphi in irange(1,32):
            rphi,reta = (iphi + dphi)%72+1,(ieta + deta)%34+1
            rkey = getKey(rphi,reta)
            nkey = getKey(iphi,ieta)
            if rkey not in towers: continue
            subset[nkey] = towers[rkey]
    return subset
def get22x22Towers(center_key,towers):
    subset = {}
    cphi,ceta = getPhiEta(center_key)
    dphi,deta = cphi - 11,ceta - 12
    for ieta in irange(1,22):
        for iphi in irange(1,22):
            rphi,reta = (iphi + dphi),(ieta + deta)
            rkey = getKey(rphi,reta)
            nkey = getKey(iphi,ieta)
            if rkey not in towers: continue
            subset[nkey] = towers[rkey]
    return subset
def get19x19Towers(center_key,towers):
    subset = {}
    cphi,ceta = getPhiEta(center_key)
    dphi,deta = cphi - 10,ceta - 10
    for ieta in irange(1,19):
        for iphi in irange(1,19):
            rphi,reta = (iphi + dphi),(ieta + deta)
            rkey = getKey(rphi,reta)
            nkey = getKey(iphi,ieta)
            if rkey not in towers: continue
            subset[nkey] = towers[rkey]
    return subset
def get7x7Towers(center_key,towers):
    subset = {}
    cphi,ceta = getPhiEta(center_key)
    dphi,deta = cphi - 4,ceta - 4
    for ieta in irange(1,7):
        for iphi in irange(1,7):
            rphi,reta = (iphi + dphi),(ieta + deta)
            rkey = getKey(rphi,reta)
            nkey = getKey(iphi,ieta)
            if rkey not in towers: continue
            subset[nkey] = towers[rkey]
    return subset
def getMaxTowerIn4x4(center,towers):
    cphi,ceta = getPhiEta(center)
    dphi,deta = cphi - 2,ceta - 3
    max_tower = {'key':-1,'et':-1}
    for iphi in irange(1,4):
        for ieta in irange(1,4):
            rphi,reta = iphi + dphi,ieta + deta
            key = getKey(rphi,reta)
            if key not in towers: continue
            if max_tower['et'] < towers[key].et:
                max_tower['key'] = key
                max_tower['et'] = towers[key].et
    return max_tower
def getMaxTowerIn7x7(center,towers):
    cphi,ceta = getPhiEta(center)
    dphi,deta = cphi - 4,ceta - 4
    max_tower = {'key':-1,'et':-1}
    for iphi in irange(1,7):
        for ieta in irange(1,7):
            rphi,reta = iphi + dphi,ieta + deta
            key = getKey(rphi,reta)
            if key not in towers: continue
            if max_tower['et'] < towers[key].et:
                max_tower['key'] = key
                max_tower['et'] = towers[key].et
    return max_tower
