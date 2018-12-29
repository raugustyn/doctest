# -*- coding: utf-8 -*-
# WORKFLOW_LICENSE

from json import dumps

from pygeotoolbox.sharedtools import normalizePath, HTMLFormatter, fileRead, saveStrToFile, initializeJavaScriptVariable

class HtmlFormField:
    def __init__(self, caption, attrName, toStrConversion = "%s"):
        self.caption = caption
        self.attrName = attrName
        self.toStrConversion = toStrConversion

class WorkflowItem:
    _paramInputInfos = None
    _formInputNames = None
    NEXT_WORKFLOW_ID = 0
    REGISTERED_WORKFLOWS = []
    def __init__(self, caption, description, onExecute, enabled, required, paramNames=[]):
        """Initialize workflow item.

        :param caption: Process human readable name.
        :param description: Process description.

        >>> namedItem = WorkflowItem("My Caption")
        >>> namedItem.caption
        'My Caption'

        >>> namedItemWithCaption = WorkflowItem("My Caption", description="My Description")
        >>> namedItem.caption
        'My Caption'
        >>> namedItemWithCaption.description
        'My Description'
        """
        self.id = str(self.NEXT_WORKFLOW_ID)
        WorkflowItem.NEXT_WORKFLOW_ID = WorkflowItem.NEXT_WORKFLOW_ID + 1
        self.caption = caption
        self.shortDescription = None
        self.description = description
        self.onExecute = onExecute
        self._enabled = enabled
        self._required = required
        self.paramNames = []
        self.paramNames.extend(paramNames)
        self.visibility = 0
        self.requires = []
        self.validateProc = None
        WorkflowItem.REGISTERED_WORKFLOWS.append(self)

    def getAlldDependencies(self):
        result = []

        def addItem(item):
            if not item in result:
                result.append(item)

        for dependency in self.requires:
            subList = dependency.getAlldDependencies()
            for item in subList:
                addItem(item)
            addItem(dependency)

        return result

    def __del__(self):
        WorkflowItem.REGISTERED_WORKFLOWS.remove(self)

    @property
    def href(self):
        return "/workflows/" + self.id

    @staticmethod
    def getItemById(itemId):
        """ Used for restfull web interfaces. Enables to get WorkflowItem object from it's id.

        :param String or Integer itemId: id of the object to be searched for.
        :return WorkflowItem: WorkflowItem with given itemId.

        >>> item = WorkflowItem("Test", "", None, True, True)
        >>> itemId = id(item)
        >>> WorkflowItem.getItemById(itemId)
        WorkflowItem('Test', True, True)

        """
        itemId = str(itemId)
        for item in WorkflowItem.REGISTERED_WORKFLOWS:
            if item.id == itemId:
                return item

        return None

    def isBlind(self):
        """ Returns True if onExecute property is empty.

        :return Boolean: True if onExecute property is empty
        """
        return self.onExecute == None

    def getJSON(self):
        result = {
            "itemId": self.id,
            "id" : id(self),
            "caption": self.caption,
            "isExpanded" : True
        }

        return result

    def getAllItems(self):
        return []

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def setEnabled(self, value):
        if not self._required:
            self._enabled = value

    @property
    def required(self):
        return self._required

    @required.setter
    def setRequired(self, value):
        self._required = value
        if value:
            self._enabled = True

    def harvestParamNames(self, skippedParamNames = []):
        result = []
        for paramName in self.paramNames:
            if not paramName in skippedParamNames:
                result.append((paramName, "parameter"))
        return result

    def execute(self):
        """This method executes desired workflow process. Returns True if suceeds.

        :param result: Returns True in case of sucess.

        >>> item = WorkflowItem("TestItem")
        >>> print item.execute()
        False

        >>> def executeProc():print "Executed procedure called";return True
        >>> item = WorkflowItem("TestItem", onExecute=executeProc)
        >>> print item.execute()
        Executed procedure called
        True
        """
        if self.onExecute:
            return self.onExecute()
        else:
            return False

    def __repr__(self):
        """Returns string representing the instance.

        :return: string representing the instance

        >>> item = WorkflowItem("Ahoj", "", None, False, True)
        >>> print item
        WorkflowItem('Ahoj', True, False)

        """
        s = "%s('%s'" % (self.__class__.__name__, self.caption)
        if self.description:
            s += ", '%s'" % self.description
        s += ", %s, %s" % (str(self.required), str(self.enabled))
        s += ')'
        return s

    def getShortDescription(self):
        if self.shortDescription:
            return self.shortDescription
        else:
            return self.description

    def getHTMLForm(self, inputSize = 50, skippedParamNames = []):
        import pygeotoolbox.sharedtools.config as config
        from pygeotoolbox.sharedtools import formatValueIfNotEmpty

        paramNames = self.harvestParamNames(skippedParamNames)

        if paramNames:
            html = HTMLFormatter()
            html.indent(3)
            html.addLineAndIndent("<form class='SettingsForm' id='Form_%s'>" % self.id)
            html.addLineAndIndent("<table>")
            formApplyRowId = "Form_%s_ApplyRow" % self.id
            WorkflowItem._formInputNames[formApplyRowId] = []
            paramIndex = 0
            for paramName, groupName in paramNames:
                if groupName <> "ChildParam":
                    valueInfo = config.valueInfos[paramName]
                    params = [
                        formatValueIfNotEmpty(" title='%s'", valueInfo.description),
                        formatValueIfNotEmpty(" required", valueInfo.required),
                        formatValueIfNotEmpty(" type='text' pattern='%s'", valueInfo.inputPattern),
                        formatValueIfNotEmpty(" size=%d", inputSize)
                    ]

                    inputId = "input_%s_%d" % (self.id, paramIndex)
                    WorkflowItem._formInputNames[formApplyRowId].append(inputId)
                    onKeyUpProc = 'onInputKeyUpProc("%s")' % inputId
                    html.addLine("<tr%s><td><input%s value='%s' onkeyup='%s' id='%s'></input></td><td style='padding-left:5px'>%s</td></tr>" %
                                 (formatValueIfNotEmpty(" class='%s_Class'", groupName),
                                  " ".join(params),
                                  config.getValue(paramName), onKeyUpProc,
                                  inputId,
                                  valueInfo.caption))
                    self._paramInputInfos[inputId] = [paramName, config.getValue(paramName), formApplyRowId]
                    paramIndex = paramIndex + 1

            onClickProc = 'onApplyButtonClick("%s")' % formApplyRowId
            html.addLine("<tr id='%s' class='ApplyRow'><td></td><td align='left'><button type='button' onclick='%s'>&nbsp;&nbsp;Použij&nbsp;&nbsp;</button></td></tr>" % (formApplyRowId, onClickProc))
            html.unIndentAndAddLine("</table>")
            html.unIndentAndAddLine("<form>")
            return html.html
        else:
            return ""

    def getAllItemsJSON(self):
        result = {}

        if self.onExecute:
            result[self.id] = self.getJSON()

        return result


    def getHTML(self):
        paramNames = self.harvestParamNames()
        skippedNames = []
        for paramName, group in paramNames:
            if group == "SharedParam":
                skippedNames.append(paramName)

        def printSequence(sequence, indent = ""):
            msg = "%s%s\t%s\t%s" % (indent, sequence.caption, str(sequence.required), str(sequence.enabled))

            print msg
            if hasattr(sequence, "items"):
                for item in sequence.items:
                    printSequence(item, indent + "\t")

        self._html = HTMLFormatter()

        def indentToHTML(indent):
            strValue = ""
            for i in range(indent):
                strValue += "&nbsp;&nbsp;&nbsp;&nbsp;"
            return "<span>%s</span>" % strValue

        def indentToFontSize(indent=0):
            sizeId = ["medium", "small", "smaller"]
            if indent >= len(sizeId):
                return "smaller"
            else:
                return sizeId[indent]

        def htmlSequence(sequence, indent = 0, showRoot = True):
            hasItems = hasattr(sequence, "items") and sequence.items
            if showRoot:
                itemId = sequence.id
                msg = HTMLFormatter()
                msg.indent(6)
                msg.addLineAndIndent("<tr style='font-size:%s' id='%s' onmouseenter='ShowElementById(\"#%s\")' onmouseleave='HideElementById(\"#%s\")'>" % (indentToFontSize(indent), itemId + "_ROW", itemId, itemId))
                if sequence.required:
                    checkBoxStr = ""
                else:
                    checkBoxStr = '<input id="%s" type="checkbox" name="vehicle" value="Bike"' % (itemId + "_CB")
                    if sequence.enabled:
                        checkBoxStr +=  " checked"
                    checkBoxStr += '>'

                if hasItems:
                    itemIcon = "<img src='http://localhost/src/folder-horizontal.png' onclick='ToggleFolder(this, \"%s\")'/>&nbsp;" % itemId
                else:
                    itemIcon = ''

                msg.addLine('<td id="%s"></td>' % (itemId + "_StatusTD"))
                msg.addLine('<td id="%s"></td>' % (itemId + "_ResultTD"))
                msg.addLine("<td>%s%s%s%s</td>" % (indentToHTML(indent), checkBoxStr, itemIcon, sequence.caption.replace(' ', '&nbsp;')))

                if sequence.isBlind():
                    runBtnHTML = ""
                else:
                    runBtnHTML = '<button style="display: none;width:6em" RunButton" id="%s_RunButton"  type="button" onclick="run(\'%s\', \'%s\')">Spusť</button>' % (itemId, sequence.id, itemId)

                msg.addLine('<td id="%s" class="RunButtonTD">%s</td>' % (itemId + "_RunButtonTD", runBtnHTML))

                formHTML = sequence.getHTMLForm(skippedParamNames=skippedNames)

                msg.addLine("<td>%s%s</td>" % (sequence.description, formHTML))
                msg.unIndentAndAddLine("</tr>")
                self._html.addLine(msg.html)
                subItemsIndent = indent + 1
            else:
                subItemsIndent = indent

            if hasItems:
                for item in sequence.items:
                    htmlSequence(item, subItemsIndent)

        def getValueIfNotEmpty(value, template = "%s"):
            if value:
                return template % value
            else:
                return ""

        WorkflowItem._paramInputInfos = {}
        WorkflowItem._formInputNames = {}
        self._html.indent(4)
        if not self.isBlind():
            self._html.addLineAndIndent('<table class="WorkflowTable">')
            htmlSequence(self, 0, False)
            self._html.addLine('<tr class="RunAllRow"><td></td><td></td><td></td><td><button type="button" onclick="RunAll()" style="width:6em">Spusť vše</button></td></tr>')
            self._html.unIndentAndAddLine("</table>")

        fullHtml = fileRead(normalizePath("workflow/WorkflowTemplate.html"))
        fullHtml = fullHtml.replace('<div id="DynamicContentDiv" class="ConsoleDiv"></div>', '<div id="DynamicContentDiv">\n%s</div>' % self._html.html)
        fullHtml = fullHtml.replace("<WORKFLOWTABLE />", "")
        fullHtml = fullHtml.replace("<#TITLE#/>", self.caption)
        fullHtml = fullHtml.replace("<#DESCRIPTION#/>", getValueIfNotEmpty(self.description, '<p class="Description" id="Description">%s</p>'))
        fullHtml = fullHtml.replace("<#SHORTDESCRIPTION#/>", getValueIfNotEmpty(self.getShortDescription(), '<p class="ShortDescription" id="ShortDescription">%s</p>'))
        fullHtml = fullHtml.replace("<#PROPERTIES_FORM#/>", getValueIfNotEmpty(self.getHTMLForm(), '%s'))
        fullHtml = fullHtml.replace("<#MAIN_STATUS#/>", '<div id="%s"></div>' % (self.id + "_StatusTD"))

        if self.validateProc:
            htmlFormatter = HTMLFormatter()
            htmlFormatter.addLineAndIndent('<div style="vertical-align: middle">')
            htmlFormatter.addLine('<button type="button" onclick="validate()" style="width:6em" title="Zkontroluje nastavení pomocí volání funkce na serveru">Zkontroluj</button>')
            htmlFormatter.addLine('<span id="ValidationMessage"></span>')
            htmlFormatter.unIndentAndAddLine('</div>')
            validateHTML = htmlFormatter.html
        else:
            validateHTML = ""

        fullHtml = fullHtml.replace("<#VALIDATEBUTTON#/>", validateHTML)


        from pygeotoolbox.sharedtools import replaceJavaScriptBlock, replaceHTMLBlock

        fullHtml = replaceJavaScriptBlock(fullHtml, "DEV", "")
        fullHtml = replaceJavaScriptBlock(fullHtml, "DEPENDSONITEMS", self.getDependsOnJSON())
        fullHtml = replaceJavaScriptBlock(fullHtml, "WORKFLOWITEMID", self.id)
        fullHtml = replaceJavaScriptBlock(fullHtml, "WORKFLOWITEMS", dumps(self.getAllItemsJSON(), indent=4))
        fullHtml = replaceJavaScriptBlock(fullHtml, "PARAM_INPUT_INFOS", dumps(WorkflowItem._paramInputInfos, indent=4))
        fullHtml = initializeJavaScriptVariable(fullHtml, "FormInputNames", dumps(WorkflowItem._formInputNames, indent=4))

        fullHtml = replaceHTMLBlock(fullHtml, "Example", "")
        return fullHtml

    def getDependsOnJSON(self):
        result = []
        for item in self.getAlldDependencies():
            isValid, msg = item.validate()
            result.append({
                "caption" : item.caption,
                "href" : item.href,
                "isValidMessage" : msg,
                "isValid" : isValid
            })

        return dumps(result, indent=4)

    def validate(self):
        """Validates item by self.validateProc. If not present, assumes item is oky.

        :return (Boolean, String): Validation state and error message if failed.
        """
        if self.validateProc:
            return self.validateProc()
        else:
            return (True, "")

    @property
    def isValid(self):
        """validating item and returns result.

        :return Boolean: True if validation was successfull
        """
        result, message = self.validate()

        return result



class HtmlFormMasterTemplateWorkflowItem(WorkflowItem):
    """ Template for field form.

    >>> a = HtmlFormMasterTemplateWorkflowItem()
    >>> content = a.getHTMLForm(40)
    >>> open("c:/temp/htmlmastertemplate.html", "w").write(content)
    """

    def __init__(self):
        WorkflowItem.__init__(self, "Test", "Test escription", None, True, True)
        self.htmlParams = [
            HtmlFormField("Text Field Example", "textField")
        ]
        self.textField = "Text Field Example Value"