/**
 * Apollo component for fetching the division results for a particular
 * division.
 */
import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';

export const LEAGUE_TABLE_QUERY = gql`
  query LeagueTable($divisionId: ID, $seasonId: ID) {
    divisionResults(divisionId: $divisionId, seasonId: $seasonId) {
      results(pageSize: 100) {
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
`;

export const leagueTableOptions = {
  options: ({ divisionId, seasonId }) => ({
    variables: {
      divisionId,
      seasonId,
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
