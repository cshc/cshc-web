import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import { NoFilter } from 'util/constants';

export const SQUAD_ROSTER_QUERY = gql`
  query SquadStats($season: Int, $team: Int, $fixtureType: String) {
    squadStats(season: $season, team: $team, fixtureType: $fixtureType) {
      totals {
        played
        won
        drawn
        lost
        goals
        cleanSheets
      }
      squad {
        played
        won
        drawn
        lost
        goals
        cleanSheets
        mom
        lom
        isCaptain
        isViceCaptain
        member {
          modelId
          firstName
          lastName
          prefPosition
          shirtNumber
          gender
          thumbUrl(profile: "squad-list")
        }
      }
    }
  }
`;

export const squadRosterOptions = {
  options: ({ teamId, seasonId, fixtureType }) => ({
    variables: {
      team: teamId,
      season: seasonId,
      fixtureType: fixtureType !== NoFilter ? fixtureType : undefined,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, squadStats }, ...props }) => ({
    networkStatus,
    error,
    squadStats,
    ...props,
  }),
};

export default graphql(SQUAD_ROSTER_QUERY, squadRosterOptions);
