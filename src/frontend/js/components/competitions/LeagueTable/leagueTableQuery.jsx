/**
 * Apollo component for fetching the division results for a particular
 * division.
 */
import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';

export const LEAGUE_TABLE_QUERY = gql`
  query LeagueTable($division_Id: ID, $season_Id: ID) {
    divisionResults(division_Id: $division_Id, season_Id: $season_Id) {
      edges {
        node {
          teamName
          played
          won
          drawn
          lost
          goalsFor
          goalsAgainst
          goalDifference
          points
          position
          notes
          ourTeam {
            genderlessAbbrName
            slug
          }
          oppTeam {
            name
            club {
              name
              slug
            }
          }
        }
      }
    }
  }
`;

export const leagueTableOptions = {
  options: ({ divisionId, seasonId }) => ({
    variables: {
      division_Id: divisionId,
      season_Id: seasonId,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, divisionResults }, ...props }) => ({
    networkStatus,
    error,
    data: divisionResults,
    ...props,
  }),
};

export default compose(graphql(LEAGUE_TABLE_QUERY, leagueTableOptions), withApolloResults);
