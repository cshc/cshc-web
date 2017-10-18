import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

export const SQUAD_ROSTER_QUERY = gql`
  query SquadStats($season: Int, $team: Int) {
    squadStats(season: $season, team: $team) {
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
  options: ({ teamId, seasonId }) => ({
    variables: {
      team: teamId,
      season: seasonId,
    },
    fetchPolicy: 'cache-first',
  }),
  props: ({ data: { networkStatus, error, squadStats }, ...props }) => ({
    networkStatus,
    error,
    squadStats,
    ...props,
  }),
};

export default graphql(SQUAD_ROSTER_QUERY, squadRosterOptions);
