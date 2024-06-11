from __future__ import absolute_import
import rules
import datetime

@rules.predicate
def is_first_day_in_month():
    return datetime.date.today().day == 1

rules.add_perm("ecp.add_esign", rules.is_authenticated | is_first_day_in_month)
