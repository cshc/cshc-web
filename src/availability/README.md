# Availability

This app handles the match availability of players and umpires, i.e. which members can play/umpire which matches.

The main models is the `MatchAvailability` model which ties a `Member` to a `Match`, together with their availability (playing or umpiring). 

### URLS

|(Example) URL                 |View                          |Description                                              |
|------------------------------|------------------------------|---------------------------------------------------------|
|**/availability/playing/m1/**    |ManageTeamPlayingAvailabilityView   |Manage the playing availabilities for a particular team's upcoming fixtures.    |
|**/availability/umpiring/**    |ManageUmpiringAvailabilityView   |Manage the umpiring availabilities for all team's upcoming fixtures.    |


### Models

|Name                       | Description  |
|---------------------------|----------------
|**MatchAvailability**                  |Represents the playing/umpiring availability of a particular member for a particular match. |

### GraphQL

_Full automatic documentation of all GraphQL queries and mutations can be found on the [GraphiQL page](//wwww.cambridgesouthhockeyclub.co.uk/graphql)_


The following GraphQL queries are provided for the availability app:
|Query                        |Description                                               |
|-----------------------------|----------------------------------------------------------|
|**matchAvailabilities**      |List of MatchAvailability objects                         |

The following GraphQL mutations are provided for the availability app:
|Mutation                     |Description                                               |
|-----------------------------|----------------------------------------------------------|
|**updateMatchAvailability**  |Update the availability for a particular member and match |

### React Apps

#### MemberDetail

The ```MemberDetail``` React app includes two 'routes' that make use of the Availability app's GraphQL queries and mutations. This React app allows the authenticated user to update their match availabilities directly from their member page.

### ManageAvailability

The ```ManageAvailability``` React app handles the management of both playing availabilities (e.g. for a particular team) and umpiring availabilities (for all teams).

### Admin Interface

You can add/edit/remove match availabilities through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/availability/).

**Note: This admin interface should only be used in extenuating circumstances as the front-end should provide all the required functionality***
