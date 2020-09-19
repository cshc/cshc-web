# Awards

This app deals with awards - both those awarded each match (i.e. Player of the Match and Lemon of the Match) and at the End of Season dinner (e.g. Player of the Season, etc.).

This is a very simple app - there are no views directly associated with it. Typically you just add match award winners as you enter the details for a match result and end of season award winners once they're decided at the end of a season.

Awards appear on the website in the following locations:
- Player (member) profile pages (end of season and match awards)
- Match details (match awards)

### URLS

|(Example) URL                 |View                          |Description                                              |
|------------------------------|------------------------------|---------------------------------------------------------|
|**/awards/end-of-season/**    |EndOfSeasonAwardWinnersView   |List of all End of Season Award Winners (filterable).    |

### Models

|Name                       | Description  |
|---------------------------|----------------
|**Award**                  |A base class with common award functionality (the award name)|
|**MatchAward**             |The various awards that can be awarded at a match. Currently there are just two instances - POM and LOM|
|**EndOfSeasonAward**       |The various awards that can be awarded at the end of a season. Note - these can change from year to year so some years you may need to add some awards (via the admin interface)|
|**AwardWinner**            |A base class with common award winner functionality (member, comment etc)|
|**MatchAwardWinner**       |All the POM and LOM award winners|
|**EndOfSeasonAwardWinner** |All the end of season award winners|

### GraphQL

The following GraphQL queries are provided for the awards app:
|Query                        |Filter Options                    |Description                                              |
|-----------------------------|----------------------------------|---------------------------------------------------------|
|**matchAwards**              |                                  |List of MatchAward nodes                                 |
|**endOfSeasonAwards**        |                                  |List of EndOfSeasonAward nodes                           |
|**matchAwardWinners**        |                                  |List of MatchAwardWinner nodes                           |
|**endOfSeasonAwardWinners**  |                                  |List of EndOfSeasonAwardWinner nodes                     |

### React Apps

#### EndOfSeasonAwardWinnerList

The ```EndOfSeasonAwardWinnerList``` React app forms part of the **EndOfSeasonAwardWinnersView** (```/awards/end-of-season/```) and displays a filterable list of End of Season Award Winners. Data is fetched from the server using the ```endOfSeasonAwardWinners``` GraphQL query.

### Admin Interface

You can add/edit/remove awards and award winners through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/awards/).
