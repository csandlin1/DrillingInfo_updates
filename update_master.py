# this module uses arcpy to read through the file geodatabase deliveries from Drilling info and create a new file
# geodatabase from the states listed in the dictionary below that contain features for that state,
# this example uses TX and OK.
import os
import datetime
import arcpy
import config
import logging
log = logging.getLogger(__name__)

arcpy.env.overwriteOutput = True
state_dict = config.state_dict

def updatenow(inPath, outPath):
    log.info(str(datetime.datetime.now()))

    # check if output database(s) exists and if not, make it
    for fn in state_dict:
        log.info(state_dict[fn]['filename'])
        if arcpy.Exists(os.path.join(outPath, state_dict[fn]['filename'])):
            log.info((state_dict[fn]['filename'] + " is here"))
        else:
            log.info("Making the databases")
            arcpy.CreateFileGDB_management(outPath, state_dict[fn]['filename'])

    # walk through each database to copy features from Oklahoma and Texas into master DBs
    for root, dirs, datasets in arcpy.da.Walk(inPath):
        print 'root', root
        print 'directories:', dirs
        print 'datasets:', datasets
        print '======'
        if len(datasets) > 0:
            for data in datasets:
                inFeature = os.path.join(root, data)
                desc = arcpy.Describe(inFeature)
                if desc.dataType == "FeatureClass":                
                    if data in ("TX_Pipelines", "DI_TX_producing_units"):  # only for Texas dataaset
                        if "Texas" in state_dict:
                            log.info("Processing " + str(desc.dataType) + " " + str(data) + "Texas")
                            arcpy.FeatureClassToFeatureClass_conversion(inFeature, os.path.join(outPath,
                                                                        state_dict["Texas"]['filename']), data)
                    elif data == "di_Rigs":  # different field names, doesn't use the abbreviation for states
                        log.info("Processing " + str(desc.dataType) + " " + str(data))
                        for state_name, state_info in state_dict.iteritems():
                            arcpy.MakeFeatureLayer_management(inFeature, "tempclass", ("state_name = '" +
                                                                        state_name + "'"))
                            feature_count = int(arcpy.GetCount_management("tempclass").getOutput(0))
                            log.info(str(state_name) + " feature count is " + str(feature_count))
                            if feature_count > 0:
                                log.info(("Adding " + str(feature_count) + " features to " + state_name))
                                arcpy.FeatureClassToFeatureClass_conversion(inFeature, os.path.join(outPath,
                                                state_info['filename']), data, ("state_name = '" + state_name + "'"))
                    else:  # this processes most of the feature classes
                        log.info("Processing " + str(desc.dataType) + " " + str(data))
                        for state_name, state_info in state_dict.iteritems():
                            arcpy.MakeFeatureLayer_management(inFeature, "tempclass", ("state = '" +
                                                                                       state_info['abbrev'] + "'"))
                            feature_count = int(arcpy.GetCount_management("tempclass").getOutput(0))
                            log.info(str(state_name) + " feature count is " + str(feature_count))
                            if feature_count > 0:
                                log.info("Adding " + str(feature_count) + " features to " + str(state_name))
                                arcpy.FeatureClassToFeatureClass_conversion(inFeature, os.path.join(outPath,
                                            state_info['filename']), data, ("state = '" + state_info['abbrev'] + "'"))
                else:  # processing table features
                    log.info("Processing " + str(desc.dataType) + " " + str(data))
                    for state_name, state_info in state_dict.iteritems():
                        arcpy.MakeTableView_management(inFeature, "out_table", ("state = '" +
                                                                                state_info['abbrev'] + "'"))
                        feature_count = int(arcpy.GetCount_management("out_table").getOutput(0))
                        log.info(str(state_name) + " feature count is " + str(feature_count))
                        if feature_count > 0:
                            log.info(("Adding " + str(feature_count) + " rows to " + str(state_name)))
                            arcpy.CopyRows_management("out_table", os.path.join(outPath, state_info['filename'], data))

    log.info(str(datetime.datetime.now()))  # to see how long the processing took
    return
