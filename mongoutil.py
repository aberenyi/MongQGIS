"""
/***************************************************************************
 MongoDB Layer - A QGIS plugin that allows to add a MongoDB collection 
                  as new map layers.

    begin                : 2011-15-04
    copyright            : (C) 2011 by Markus Wuersch
    email                : markus at wuersch.net
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

class MongoUtil:
    """Helper Class"""
    def get_var(self, input_dict, accessor_string):
        """
            Gets data from a dictionary using a dot notation
            source: http://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
        """
        current_data = input_dict
        for chunk in accessor_string.split('.'):
            current_data = current_data.get(chunk, {})
        return current_data

    def get2dField(self, db, coll_name):
        idxs = db[coll_name].index_information()
        fields = [key for key in idxs]
        for field in fields:
            idx = idxs[field]['key'][0]
            if idx[1] == '2d': 
                return idx[0]
        return None

    def getGeoCollectionNames(self, db):
        coll_names = []
        colls = db.collection_names()
        for coll in colls:
            doc = db[coll].find_one()
            if doc is not None and self.get2dField(db, coll) is not None:
                coll_names.append(coll)
        return coll_names

    def getSampleGeoValues(self, db, coll_name):
        doc = db[coll_name].find_one()
        if doc is None:
            return None
        else:
            return self.get_var(doc, self.get2dField(db, coll_name))

    """uff"""

    def analyze2dField(self, db, coll_name):
        doc = db[coll_name].find_one()
        loc = doc['loc']
        print loc
        print self.getType(loc)


