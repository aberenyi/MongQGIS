# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MongQGISDialog
                                 A QGIS plugin
 TBD
                             -------------------
        begin                : 2015-06-03
        git sha              : $Format:%H$
        copyright            : (C) 2015 by GISLab Consulting Ltd.
        email                : aberenyi@gislab.hu
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

import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'mongqgis_dialog_base.ui'))

from mongoutil import MongoUtil
import types

class MongQGISDialog(QtGui.QDialog, FORM_CLASS):
    db = None
    collection = None
    x = None
    y = None

    def __init__(self, parent=None):
        """Constructor."""
        self.connection = None
        self.comboBoxDBIdx = -10
        self.comboBoxCollectionIdx = -10
        self.mongoUtil = MongoUtil()
        super(MongQGISDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def on_btnConnect_released(self):
        try:
            _host = str(self.host.displayText())
            _port = int(self.port.displayText())
            self.setStatusText('Connecting to %s:%d...' % (_host, _port))
            from pymongo import MongoClient
            self.connection = MongoClient(_host, _port)

            self.comboBoxDBs.clear()
            self.comboBoxDBs.setEnabled(True)
            self.comboBoxDBs.addItem('<select a database>')

            self.setStatusText('Fetching database names...')
            dbs = self.connection.database_names()
            for db in dbs:
                self.comboBoxDBs.addItem(db)
            self.setStatusText('Please select a database...')

            #self.comboBoxColls.addItem('<select collection>')
            #self.labelLongitudeField.setEnabled(False)
            #self.comboBoxLongField.setEnabled(False)
            #self.comboBoxDBs.clear()

        except:
            self.setStatusText('Connection failure.')

    def on_comboBoxDBs_currentIndexChanged(self):
        if self.comboBoxDBs.currentIndex() == 0:
            self.comboBoxCollections.setEnabled(False)
            return
        if str(self.comboBoxDBs.itemText(self.comboBoxDBs.currentIndex())) == '':
            return
        if str(self.comboBoxDBs.itemText(self.comboBoxDBs.currentIndex())) == '<select a database>':
            return
        if self.comboBoxDBIdx == self.comboBoxDBs.currentIndex():
            return
        self.comboBoxDBIdx = self.comboBoxDBs.currentIndex()

        self.setStatusText('Fetching collection names...')
        self.comboBoxCollections.clear()
        self.comboBoxCollections.addItem('<select a collection>')

        self.db = str(self.comboBoxDBs.itemText(self.comboBoxDBs.currentIndex()))
        _colls = self.mongoUtil.getGeoCollectionNames(self.connection[self.db])
        for coll in _colls:
            self.comboBoxCollections.addItem(coll)
        self.comboBoxCollections.setEnabled(True)
        #self.labelLongitudeField.setEnabled(False)
        #self.comboBoxLongField.setEnabled(False)
        self.setStatusText('Please select a collection...')

    def on_comboBoxCollections_currentIndexChanged(self):
        if self.comboBoxCollectionIdx == self.comboBoxCollections.currentIndex():
            return
        #self.labelLongitudeField.setEnabled(False)
        #self.comboBoxLongField.setEnabled(False)
        self.comboBoxCollectionIdx = self.comboBoxCollections.currentIndex()
        #self.btnOk.setEnabled(self.comboBoxColls.currentIndex()>0)

        if self.comboBoxCollections.currentIndex() > 0 and self.comboBoxDBs.currentIndex() > 0:
            #_dbName = str(self.comboBoxDBs.itemText(self.comboBoxDBs.currentIndex()))
            self.collection = str(self.comboBoxCollections.itemText(self.comboBoxCollections.currentIndex()))
            property = self.mongoUtil.get2dField(self.connection[self.db], self.collection)
            geo = self.mongoUtil.getSampleGeoValues(self.connection[self.db], self.collection)
            if type(geo) == types.ListType:
                self.comboBoxX.setEnabled(True)
                self.comboBoxY.setEnabled(True)
                self.comboBoxX.clear()
                self.comboBoxY.clear()
                self.x = '%s[0]' % property
                self.y = '%s[0]' % property
                self.comboBoxX.addItem(self.x)
                self.comboBoxY.addItem(self.y)

            else:
                self.setStatusText('TBD')
                """fields = [key for key in geo]
                self.labelLongitudeField.setEnabled(True)
                self.comboBoxLongField.setEnabled(True)
                self.comboBoxLongField.clear()
                self.comboBoxLongField.addItem(fields[0])
                self.comboBoxLongField.addItem(fields[1])
                if str(fields[0]).lower().startswith('lat'):
                    self.comboBoxLongField.setCurrentIndex(1)
                    self.labelLatitudeFieldName.setText(str(fields[0]))
                else:
                    self.comboBoxLongField.setCurrentIndex(0)
                    self.labelLatitudeFieldName.setText(str(fields[1]))"""

    def setStatusText(self, text):
       self.labelStatus.setText(text)
