# Matches

This is one of the main CSHC apps. Matches are at the heart of the club's data so a lot of the site's functionality is contained within this app.

Goal King and Accidental Tourist statistics are automatically calculated as part of a nightly cronjob and the stats cached in the GoalKing model/table. This is one of a number of tables used to facilitate the speedy display of data which would otherwise take an unacceptable amount of time to calculate 'live'.

### Feeds

RSS/Atom feeds of the latest match reports and an ical calendar feed of all matches this season are automatically generated - see feeds.py

### URLS

|(Example) URL                                      |View                               |Description                                 |
|---------------------------------------------------|-----------------------------------|--------------------------------------------|
|**/matches/**                                      |MatchListView                      |Searchable/filterable list of all matches.|
|**/matches/<pk>**                                  |MatchDetailView                    |Details of a particular match.|
|**/matches/<23-Apr-13>/**                          |MatchesByDateView                  |List of matches on a particular date.|
|**/matches/goal-king/<2012-2013>/**                |GoalKingSeasonView                 |Goal King stats table for a particular season. If the season is not supplied in the URL, the current season's stats will be displayed.|
|**/matches/accidental-tourist/<2012-2013>/**       |AccidentalTouristSeasonView        |Accidental Tourist stats table for a particular season. If the season is not supplied in the URL, the current season's stats will be displayed.|
|**/matches/naughty-step/**                         |NaughtyStepView                    |Statistics on the number of cards (red/yellow/green) received by members.|
|**/matches/feed/rss/**                             |RssMatchReportsFeed                |RSS feed of match reports.|
|**/matches/feed/atom/**                            |AtomMatchReportsFeed               |Atom feed of match reports.|
|**/matches/cshc_matches.ics**                      |MatchICalFeed                      |Calendar feed of this season's matches.|

### Models

|Name           |Description                                                                    |
|---------------|-------------------------------------------------------------------------------|
|**Match**      |One entry for each match we play. See module docstring in match.py for more details.|
|**Appearance** |Used to track which members (players) play in each match.|
|**GoalKing**   |Auto-updated goals and travelling statistics for each member in a particular season. Used for display of Goal King and Accidental Tourist statistics.|

### GraphQL

The following GraphQL queries are provided for the teams app:
|Query                        |Filter Options                    |Description                                              |
|-----------------------------|----------------------------------|---------------------------------------------------------|
|**matches**                  |_venue\_Name_, _oppTeam\_Name_, _oppTeam\_Club\_Slug_, _ourTeam\_Slug_, _season\_Slug_ |List of match edges |
|**appearances**              |                                  |List of appearance nodes                                 |
|**goal\_king\_entries**      |_member\_Gender_, _season\_Slug_  |List of goal king entries                                |

### React Apps

#### MatchList

The ```MatchList``` React app forms part of the **MatchListView** (```/matches/```) and displays a paginated/filterable/searchable list of Matches. Data is fetched from the server using the ```matches``` GraphQL query.

#### MatchDetail

The ```MatchDetail``` React app forms part of the **MatchDetailView** (```/matches/<pk>```) and includes a table of previous matches between the two teams. Data is fetched from the server using the ```matches``` GraphQL query.

#### GoalKing

The ```GoalKing``` React app forms part of the **GoalKingSeasonView** (```/matches/goal-king/<season_slug>```) and displays a filterable list of Goal King entries (filterable by mens/ladies and season). Data is fetched from the server using the ```goal_king_entries``` GraphQL query.

### Admin Interface

You can add/edit/remove matches and appearances (typically done in-line for a particular match) through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/matches/). Note - GoalKing is deliberately hidden from the admin interface as it is handled programmatically.
