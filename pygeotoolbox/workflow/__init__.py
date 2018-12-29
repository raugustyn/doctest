registeredWorkflows = []

def getRegisteredWorkflows():
    """ Returns registered workflows list.

    :return List of WorkflowItem : Registered workflows list
    """
    return registeredWorkflows

def registerWorkflow(workflowItem, visibility = 0):
    """Registers workflow into workflow list. As a result, WorkflowRegistryItem
    will be append to the registeredWorkflows list.

    :param WorkflowItem workflowItem: Workflow instance to be registered
    :param String visibility: Visibility tag, used in visibility url query parameter.

    """
    workflowItem.visibility = visibility
    registeredWorkflows.append(workflowItem)


from workflowitem import WorkflowItem, HtmlFormField
from workflowsequence import WorkflowSequence

class Workflow(WorkflowSequence):
    """This class is just better name for root workflow sequence item.
    >>> Workflow("My Workflow")
    Workflow('My Workflow', [])
    """
    pass

class GeneralizationWorkflow(Workflow):
    """ This is generic class representing generealization workflow.
    """

    def __init__(self, caption, description = ''):
        self.preProcessing = WorkflowSequence("PreProcessing", "", [], True, True)
        self.generalization =  WorkflowSequence("Generalizace", "", [], True, True)
        self.postProcessing = WorkflowSequence("PostProcessing", "", [], True, True)
        items = [
            self.preProcessing,
            self.generalization,
            self.postProcessing
        ]
        Workflow.__init__(self, caption, description=description, items=items, enabled=True, required=True)

def buildHTMLPageContent(title, content):
    """Takes standard HTML page template and generates result with given content and title.

    :param String title: Page title.
    :param String content: HTML code used as page content.
    :return String: HTML code of the requested page.

    """
    from pygeotoolbox.sharedtools.base import fileRead, replaceHTMLBlock, replaceJavaScriptBlock
    from pygeotoolbox.sharedtools import normalizePath

    html = fileRead(normalizePath("workflow/WebPageTemplate.html"))
    html = html.replace("<title>Title</title>", "<title>%s</title>" % title)
    html = html.replace('<h1 id="IdentifierH1">Title</h1>', '<h1 id="IdentifierH1">%s</h1>' % title)
    html = html.replace('<div id="DynamicContentDiv"></div>', '<div id="DynamicContentDiv">%s</div>' % content)
    html = replaceHTMLBlock(html, "DEV", "")
    html = replaceJavaScriptBlock(html, "DEV", "")

    return html