# Members

This app deals with club members and their membership in squads and the committee.

Members are closely related to Users. To distinquish:

A Member:
- participates in matches (see the Appearance model)
- (potentially) holds committee positions
- (hopefully) wins awards

A User:
- logs in/out of the website
- has permissions (e.g. to access the admin interface)

A User may request (via a button on their profile page) that their corresponding Member be associated (linked) with their User. This is done as a manual step by an administrator using the admin interface (the Member model has a 'User' field.) Once a Member is linked to a User, the User may edit their profile picture (and preferred playing position) via their profile page.

### URLS

|(Example) URL                 |View             |Description                                              |
|------------------------------|-----------------|---------------------------------------------------------|
|**/members/**                 |MemberListView   |List of all members (filterable).                        |
|**/members/<32>/**            |MemberDetailView |Details of a particular member.                          |

### Models

|Name                    |Description                                                                    |
|------------------------|-------------------------------------------------------------------------------|
|**Member**              |Club members - see above description for more details.                         |
|**SquadMembership**     |Associates a member with a squad (in a particular season).                     |
|**CommitteePosition**   |Definitions of the various committee positions.                                |
|**CommitteeMembership** |Tracks which member held which committee position in a particular season.      |

### GraphQL

The following GraphQL queries are provided for the teams app:
|Query                        |Filter Options                    |Description                                              |
|-----------------------------|----------------------------------|---------------------------------------------------------|
|**members**                  |_is\_Current_, _pref\_Position_, _gender_, _appearances\_Match\_Season\_Slug_, _appearances\_Match\_OurTeam\_Slug_    |List of club member edges |
|**committee_positions**      |                                  |List of Committee Position nodes                         |
|**committee_memberships**    |                                  |List of Committee Membership nodes                       |
|**squad_memberships**        |                                  |List of Squad Membership nodes                           |
|**squad\_stats**             |_team_, _season_                  |Custom node that provides stats for the team as a whole (```totals```) and each squad member (```squad```).   |

### React Apps

#### MemberList

The ```MemberList``` React app forms part of the **MemberListView** (```/members/```) and displays a filterable/searchable list of Members. You can also switch between map and list views of the members (although the map view is only available for users with the appropriate permissions). Data is fetched from the server using the ```members``` GraphQL query.

### Admin Interface

You can add/edit/remove members, squad membership and committee positions and memberships through the [admin interface](//www.cambridgesouthhockeyclub.co.uk/admin/members/).