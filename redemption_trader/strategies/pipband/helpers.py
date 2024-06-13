import math
def get_R(entry, target, stoploss):
    return (target - stoploss)/(entry - stoploss)

def position_size(dir, entry,SL_px, risk_GBP):
    GBP_per_pt = dir*risk_GBP/(entry - SL_px)
    return GBP_per_pt

def gen_targets():
    pass

def entry_signal(open_px, close_px,band ):
    Lo, Hi = nearest_00levels(open_px,band)
    if Hi == Lo:
        dir = 0
    else:

        if close_px > Hi and open_px < Hi:
            dir = 1
        elif close_px < Lo and open_px > Lo:
            dir = -1
        else:
            dir = 0
    return dir

def new_candle(timestamp, time):
    if timestamp != time:
        return True
    else:
        return False

def midmarket(bid,ask):
    return 0.5*(bid+ask)
#------------------------------------------------
#   Strategy Specific
#------------------------------------------------
def nearest_00levels(px,band):
    HiLevel = band*( math.floor(px/band)+math.ceil((px - math.floor(px))/band) )
    LoLevel = band *( math.floor(px/band)+math.floor((px - math.floor(px))/band))
    return LoLevel, HiLevel



def gen00_levels(px,band):
    HiLevel = band*( math.floor(px/band)+math.ceil((px - math.floor(px))/band) )
    LoLevel = band *( math.floor(px/band)+math.floor((px - math.floor(px))/band)) - band
    return LoLevel, HiLevel

def gen_targets(dir,px,band):
    Lo,Hi = gen00_levels(px,band)

    if dir ==1:
        T_px = Hi
        SL_px = Lo
    elif dir ==-1:
        T_px = Lo
        SL_px = Hi
    return T_px, SL_px

    


    

