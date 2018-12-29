#  -*- coding: utf-8 -*-
__author__ = "radek.augustyn@email.cz"


from pygeotoolbox.dataconnectors import connection as database
from pygeotoolbox.dataconnectors.postgis import FieldDefinition
from pygeotoolbox.sharedtools import listToSqlStr, setParameters, normalizePath
import pygeotoolbox.sharedtools.log as log
from operations import Operations


listSymbolNamesSQL = """
with symbol_names as (
	select map_symbol from m3_persistent_representations.context_features
			where representation_id = 1234
			group by map_symbol
)

select array_agg(map_symbol) from symbol_names"""


searchForEquivalentRealFeatureSQL = """
with stored_feature as (
	select geom, st_buffer(geom, 0.5) as geom_buffer from m3_persistent_representations.context_features where id = 1234
),

context_mbr as (
	select * from m3_persistent_representations.representations  where representation_id = 5678
),

real_features_in_view as (
	select elm_id as id, source_geom as geom, st_buffer(source_geom, 0.5) as geom_buffer  from data.elements as elements, context_mbr
		where source_elt_id = 'P4203000' and context_mbr.geom && source_geom
),

real_feature as (

	select * from real_features_in_view, stored_feature
		where st_contains(real_features_in_view.geom_buffer, stored_feature.geom) and st_contains(stored_feature.geom_buffer, real_features_in_view.geom)
)


select id from real_feature"""


searchForEquivalentContextFeatureSQL = """
with real_feature as (
	select source_geom as geom, st_buffer(source_geom, 0.5) as geom_buffer from data.elements where elm_id = 1234
),

context_features_in_representation as (
	select geom as geom, st_buffer(geom, 0.5) as geom_buffer  from m3_persistent_representations.context_features
		where representation_id = 5678 and map_symbol = 'B1260000'
),

context_feature as (
	select * from context_features_in_representation, real_feature
		where st_contains(context_features_in_representation.geom_buffer, real_feature.geom) and st_contains(real_feature.geom_buffer, context_features_in_representation.geom)
)

select count(*) from context_feature"""

selectContextRealFeatures = """
with context_mbr as (
	select * from m3_persistent_representations.representations  where representation_id = 1234
)


select elm_id, source_elt_id from data.elements as elements, context_mbr
		where source_elt_id in ('L3020100') and context_mbr.geom && source_geom and (st_contains(context_mbr.geom, source_geom) or ST_Overlaps(context_mbr.geom, source_geom))
"""


cleanStatusSQL = """
update m3_persistent_representations.context_features set status=null;
update m3_persistent_representations.cartographic_features set status=null;
update m3_persistent_representations.representations set status=null;
"""

selectCartographicFeatures = """
select feature_id, st_astext(geom), cartographic_operation from m3_persistent_representations.cartographic_features where representation_id = 1234 and geom is not null
union ALL
select feature_id, ''::text as geom, cartographic_operation from m3_persistent_representations.cartographic_features where representation_id = 1234 and geom is null
"""

selectRepresentationsInCurrentMap = """
with envelope as (
	select st_astext(st_buffer(st_envelope(ST_Collect (source_geom)), 0.1)) as geom from data.elements
)

select representation_id, caption
	from  m3_persistent_representations.representations, envelope
	where envelope.geom && representations.geom
"""


class StatusCodes:
    STATUS_OK = 0
    STATUS_NOT_APPLIED = 1
    STATUS_APPLIED = 2
    STATUS_NOEQUIVALENTFOUND = 3
    STATUS_MORETHANNONEEQUIVALENTFOUND = 4
    STATUS_EQUIVALENT_FOUND = 5
    STATUS_NOCONTEXTELEMENT_FOUND = 6
    STATUS_MORETHANONECONTEXTELEMENT_FOUND = 8


class PersistentRepresentationsProcessor:
    DATA_UPDATED = False

    def __init__(self):
        self.representationId = None
        self.representationCaption = None
        self.contextMBR = None
        self.changed = False
        self.executeBuffer = []
        self.idLinks = {}


    def logError(self, msg):
        log.error(msg)
        self.changed = True


    def checkRealElementsOverContext(self):
        for row in database.executeSelectSQL("select id, feature_id, map_symbol from m3_persistent_representations.context_features where representation_id = 1", { "1": self.representationId}):
            id, featureId, mapSymbol = row
            equivalentRows = database.executeSelectSQL(searchForEquivalentRealFeatureSQL, { "P4203000": mapSymbol, "1234": id, "5678": self.representationId })
            if equivalentRows:
                equivalentRows = equivalentRows.fetchall()
                if equivalentRows == []:
                    status = StatusCodes.STATUS_NOEQUIVALENTFOUND
                elif len(equivalentRows) > 1:
                    status = StatusCodes.STATUS_MORETHANNONEEQUIVALENTFOUND
                else:
                    status = StatusCodes.STATUS_EQUIVALENT_FOUND
                    dataId = equivalentRows[0][0]
                    self.idLinks[featureId] = dataId
            else:
                status = StatusCodes.STATUS_NOEQUIVALENTFOUND

            if status != StatusCodes.STATUS_EQUIVALENT_FOUND:
                self.changed = True

            self.executeSQL("update m3_persistent_representations.context_features set status=1234 where id=5678", {"1234" : status, "5678" : id } )


    def checkContextElementsOverReal(self):
        mapSymbols = database.firstRowFromSelect(listSymbolNamesSQL, { "1234": self.representationId} )[0]

        for row in database.executeSelectSQL(selectContextRealFeatures, { "1234": self.representationId, "('L3020100')": listToSqlStr(mapSymbols) }):
            elementId, mapSymbol = row
            equivalentCount = database.firstRowFromSelect(searchForEquivalentContextFeatureSQL, { "B1260000": mapSymbol, "1234": elementId, "5678": self.representationId })[0]
            if equivalentCount == 0:
                status = StatusCodes.STATUS_NOCONTEXTELEMENT_FOUND
            elif equivalentCount > 1:
                status = StatusCodes.STATUS_MORETHANNONEEQUIVALENTFOUND
            else:
                status = StatusCodes.STATUS_EQUIVALENT_FOUND

            if status <> StatusCodes.STATUS_EQUIVALENT_FOUND:
                self.changed = True

            self.executeSQL("update data.elements set pcr_status=1234 where elm_id=5678",  {"1234": status, "5678": elementId})


    def executeSQL(self, sql, params = {}):
        sql = setParameters(sql, params)
        self.executeBuffer = database.executeBuffer(sql, self.executeBuffer)


    def cleanStatusFields(self):
        database.execute(cleanStatusSQL)
        fieldDefinitions, addedFields = database.addFieldsIfNotExists("data", "elements", [FieldDefinition("pcr_status", "integer", None)])
        if not addedFields:
            database.execute("update data.elements set pcr_status=null;")


    def execute(self):
        log.logger.openSection("Analysing context for permanent cartographic representations")
        if not PersistentRepresentationsProcessor.DATA_UPDATED:
            import loader

            loader.databaseNeeded()
            PersistentRepresentationsProcessor.DATA_UPDATED = True

        self.idLinks = {}
        self.cleanStatusFields()
        self.executeBuffer = []
        appliedCount = 0
        changedCount = 0
        representations = database.executeSelectSQL(selectRepresentationsInCurrentMap)
        for row in representations:
            self.representationId = row[0]
            self.representationCaption = "#%s:%s" % (str(self.representationId), row[1])

            log.logger.info("Processing representation %s" % self.representationCaption)

            self.changed = False
            self.checkRealElementsOverContext()
            self.checkContextElementsOverReal()
            self.executeSQL("update m3_persistent_representations.representations set status=1234 where representation_id=5678", {"1234" : int(self.changed), "5678" : self.representationId } )

            if self.changed:
                log.logger.info("Situation has changed")
                changedCount += 1
            else:
                self.applyChanges()
                appliedCount += 1

        database.flushBuffer(self.executeBuffer)
        log.logger.closeSection("Done - %d applied, %d changed." % (appliedCount, changedCount))


    def applyChanges(self):
        log.logger.openSection("Applying context...")
        result = True
        for row in database.executeSelectSQL(selectCartographicFeatures, { "1234": self.representationId }):
            featureId = row[0]
            if featureId in self.idLinks:
                elementId = self.idLinks[featureId]
                self.executeSQL("update data.elements set state=1 where elm_id=5678".replace("state=1", Operations.captionToSQLSetStatement(row[2])), {
                    "$geom$": "st_geometryfromtext('%s', 5514)" % row[1],
                    "5678": elementId
                })
            else:
                log.logger.error("No match [%s] %s PersistentRepresentationsProcessor.applyChanges()"  % (str(featureId), __file__))
                result = False

        log.logger.closeSection()
        return result



from workflow import WorkflowItem

def process():
    procesor = PersistentRepresentationsProcessor()
    procesor.execute()
    return True


def getWorkflow():
    return WorkflowItem("Persistent Cartographic Representations", "", process, True, True)

if __name__ == "__main__":
    log.createLoggerForModule(__file__)

    process()