# Awards

This app provides support for keeping track of - and categorizing - uploaded documents.

This is a very simple app - there are no views directly associated with it, but it does provide a couple of template tags, together with their associated templates.

### Models

|Name                       | Description  |
|---------------------------|----------------
|**Document**               |Represents an uploaded document, provided with various meta data. |
|**DocumentCategory**       |Represents a category of document. Can be nested within another category. |

### Template Tags

|Name                       | Parameters                   | Description                                                                    |
|---------------------------|------------------------------|--------------------------------------------------------------------------------|
|**document**               | ```title```, ````category``` | ```inclusion tag``` to render a link to a document                             |
|**document_list**          | ```category```               | ```inclusion tag``` to render a list of documents within a particular category |


### Admin Interface

You can add/edit/remove documents and document categories through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/documents/).
