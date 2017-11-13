# Venues

This app handles one model - a Venue. It is pretty simple and a good example of a self-contained app. The only dependency it has on another app's models is for retrieving a list of fixtures for a particular venue.

Venues are typically astro pitches but the model can be used for any geographical location, ideally with a physical address. For example, the clubhouse is listed as a 'Venue'.

### URLS

|(Example) URL         |View            |Description                                 |
|----------------------|----------------|--------------------------------------------|
|**/venues/**          |VenueListView   |Lists all venues, home and away. Filterable by home/away, current season, team and division.|
|**/venues/<leys>/**   |VenueDetailView |Details on a particular venue. Includes all past results and future fixtures at this venue.|

### Models

|Name       |Description    |
|-----------|----------------
|**Venue**  |The various venues at which hockey matches are played, plus one or two other locations (e.g. clubhouse).|


### GraphQL

The following GraphQL queries are provided for the venues app:
|Query                   |Filter Options                    |Description                                              |
|------------------------|----------------------------------|---------------------------------------------------------|
|**venues**              |_name_, _isHome_, _matches\_Division_, _matches\_OurTeam\_Slug_, _matches\_Season\_Slug_ |Filterable list of venue edges |

### React Apps

#### VenueList

The ```VenueList``` React app forms part of the **VenueListView** (```/venues/```) and displays a filterable/searchable list of match venues. You can also switch between map and list views of the venues. Data is fetched from the server using the ```venues``` GraphQL query.

#### VenueDetail

The ```VenueDetail``` React app forms part of the **VenueDetailView** (```/venues/<slug>```) and displays a list of previous results and upcoming fixtures at a particular venue.  Data is fetched from the server using the ```matches``` GraphQL query (documented in the **matches** app).


### Admin Interface

You can add/edit/remove venues through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/venues/).
