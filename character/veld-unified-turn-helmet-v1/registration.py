"""Master-relative collar anchors; do not normalize individual head heights."""
MASTER_GASKET_BOTTOM={'north':104,'east':107,'south':108,'west':107}
CLEAR_BOX=(96,65,169,105)
PROTECTED_BOX=(96,65,169,109)
def bottom(start,end,slot):
    return round(MASTER_GASKET_BOTTOM[start]+(MASTER_GASKET_BOTTOM[end]-MASTER_GASKET_BOTTOM[start])*slot/5)
