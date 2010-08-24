#!/usr/bin/env python
"""
_Exists_

Oracle implementation of Subscription.Exists

TABLE wmbs_subscription
    id      INT(11) NOT NULL AUTO_INCREMENT,
    fileset INT(11) NOT NULL,
    workflow INT(11) NOT NULL,
    type    ENUM("merge", "processing")
    last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP
"""

__all__ = []
__revision__ = "$Id: Exists.py,v 1.4 2009/01/12 19:26:05 sfoulkes Exp $"
__version__ = "$Revision: 1.4 $"

from WMCore.WMBS.MySQL.Subscriptions.Exists import Exists as ExistsMySQL

class Exists(ExistsMySQL):    
    sql =  """select id from wmbs_subscription
             where fileset = :fileset and workflow = :workflow 
                  and subtype = (SELECT id FROM wmbs_subs_type 
                                 WHERE name = :type)"""
