# Teams

This app deals with Cambridge South teams, team captains, team statistics etc.

A key concept is the ClubTeamSeasonParticipation model. This stores details of a team's activity in a particular season (playing record, division, cup, team photo etc).

Up-to-date league table data is scraped from the East League's website and displayed on the team details page. See league_scraper.py for details.

Each team's playing record this season and the Southerners stats are automatically calculated as part of a nightly cronjob and the stats cached in the ClubTeamSeasonParticipation and Southerners models/tables. This is done to facilitate the speedy display of data which would otherwise take an unacceptable amount of time to calculate 'live'.

### Feeds

RSS/Atom feeds of each team's match reports and an ical calendar feed of each team's matches this season are automatically generated - see feeds.py


### URLS

|(Example) URL                          |View                        |Description                                 |
|---------------------------------------|----------------------------|--------------------------------------------|
|**/teams/**                            |ClubTeamListView            |List of all CSHC teams |
|**/teams/playing-record/**             |PlayingRecordView           |The playing records through the seasons of each team.|
|**/teams/southerners/<2012-2013>/**    |SouthernersSeasonView       |Statistics table comparing the performance of CSHC teams in a particular season. If the season is not supplied in the URL, the current season's stats will be displayed.|
|**/teams/\<m1\>/<2012-2013>**            |ClubTeamDetailView          |Details of a particular CSHC team (including the team's playing record) for a particular season. If the season is not supplied in the URL, the current season's details will be displayed.|
|**/teams/\<m1\>.ics**                    |ClubTeamMatchICalFeed       |Calendar feed of a particular team's matches.|
|**/teams/\<m1\>.rss**                    |RssClubTeamMatchReportsFeed |RSS feed of a particular team's match reports.|


### Models

|Name                            |Description                                                             |
|--------------------------------|------------------------------------------------------------------------|
|**ClubTeam**                    |The various teams within Cambridge South Hockey Club.                   |
|**ClubTeamSeasonParticipation** |Details associated with a particular team in a particular season.       |
|**Southerner**                  |Auto-updated playing record statistics for each CSHC team.              |
|**TeamCaptaincy**               |Details of who was captain and vice-captain for a particular team in a particular season.|


### GraphQL

The following GraphQL queries are provided for the teams app:
|Query                   |Filter Options                    |Description                                              |
|------------------------|----------------------------------|---------------------------------------------------------|
|**club\_teams**         |                                  |List of club team nodes                                  |
|**participations**      |                                  |List of club team season participation nodes             |
|**captaincies**         |                                  |List of team captaincy nodes                             |

### React Apps

#### TeamDetail

The ```TeamDetail``` React app forms part of the **ClubTeamDetailView** (```/teams/<slug>```) and displays the following details for the specified team and season:
* Previous results
* Upcoming fixtures
* League Table
* Squad Roster

Data is fetched from the server using the following GraphQL queries:
* Previous results and upcoming fixtures:  ```matches``` GraphQL query (documented in the **matches** app)
* League table: ```divisionResults``` GraphQL query (documented in the **competitions** app)
* Squad Roster: ```squadStats``` GraphQL query (documented in the **members** app)

### Admin Interface

You can add/edit/remove teams, captains and participation info through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/teams/). Note - Southerner is deliberately hidden from the admin interface as it is handled programmatically.
