from workflowitem import WorkflowItem
import sharedtools.log as log

class WorkflowSequence(WorkflowItem):
    def __init__(self, caption, description, items, enabled, required):
        """Initialise workfwlow sequence with items if provided.

        :param caption:Sequence human readable caption.
        :param description:Sequence description.
        :param items:

        >>> sequence = WorkflowSequence("My Sequence")
        >>> sequence.caption
        'My Sequence'


        >>> sequence = WorkflowSequence("My Sequence", items = [WorkflowItem("ItemA"), WorkflowItem("ItemB")])
        >>> len(sequence.items)
        2
        """
        WorkflowItem.__init__(self, caption, description=description, onExecute = None, enabled=enabled, required=required)
        self.items = items

    def harvestParamNames(self, skippedParamNames = []):
        result = WorkflowItem.harvestParamNames(self, skippedParamNames)

        allParamNames = []
        for item in self.items:
            for paramName in item.paramNames:
                if not paramName in allParamNames and not paramName in skippedParamNames:
                    allParamNames.append(paramName)

        for paramName in allParamNames:
            if not paramName in result:
                isSharedParam = True
                for item in self.items:
                    if not paramName in item.paramNames:
                        isSharedParam = False
                        break

                if isSharedParam:
                    groupName = "SharedParam"
                else:
                    groupName = "ChildParam"
                result.append((paramName, groupName))

        return result

    def isBlind(self):
        if self.items:
            for item in self.items:
                if not item.isBlind():
                    return False

        return WorkflowItem.isBlind(self)

    def getJSON(self):
        result = WorkflowItem.getJSON(self)
        itemIds = []
        for item in self.items:
            itemIds.append(item.id)
        result["itemIds"] = itemIds

        itemSubIds = []
        for item in self.getAllItems():
            itemSubIds.append(item.id)
        result["itemSubIds"] = itemSubIds

        return result

    def getAllItemsJSON(self):
        result = {}
        for item in self.getAllItems():
            result[item.id] = item.getJSON()

        return result

    def getAllItems(self):
        result = []

        for item in self.items:
            result.append(item)
            result.extend(item.getAllItems())

        return result

    def execute(self):
        """This method executes all processes in self.items list. Returns True if all of them suceeeded.

        :param result: Returns True in case of sucess.

        >>> def executeProcA():print "Executed procedure A called";return True
        >>> def executeProcB():print "Executed procedure B called";return True
        >>> itemA = WorkflowItem("TestItem", onExecute=executeProcA)
        >>> itemB = WorkflowItem("TestItem", onExecute=executeProcB)
        >>> sequence = WorkflowSequence("Sequence", items = [itemA, itemB])
        >>> sequence.execute()
        Executed procedure A called
        Executed procedure B called
        True
        """
        log.logger.openSection("Processing sequence '%s' items..." % self.caption)
        for item in self.items:
            log.logger.openSection(item.caption)
            if not item.execute():
                log.logger.warning("Item %s didn't return with True. Skipping sequence..." % item.caption)
                return False
            log.logger.closeSection()

        log.logger.closeSection()
        return True

    def getItemByCaption(self, caption):
        for item in self.items:
            if item.caption == caption:
                return WorkflowItem

        return None

    def __repr__(self):
        """

        :return: string representing the instance

        >>> item = WorkflowItem("Ahoj")
        >>> print item
        WorkflowItem('Ahoj', False, True)
        """
        s = "%s('%s'" % (self.__class__.__name__, self.caption)
        if self.description:
            s += ", '%s'" % self.description

        if self.items:
            s += ", " + str(self.items)
        else:
            s += ", Empty"
        s += ')'
        return s

