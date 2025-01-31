# generated by 04-find-leak.sage
MISSING=-1
PERIOD_SHIFT=33
PERIOD_ZERO=732
def model_leakpos(r, c):
    if r == c:
        return MISSING
    pos = -315.0*c^2 + 2264764.75*c + 1047823.0
    pos += -5.75*(c%8)
    pos += PERIOD_ZERO*r
    if r > c:
        pos += PERIOD_SHIFT - PERIOD_ZERO
    return int(pos)
