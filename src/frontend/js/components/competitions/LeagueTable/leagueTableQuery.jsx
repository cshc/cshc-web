import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

export const LEAGUE_TABLE_QUERY = gql`
  query LeagueTable($division_Id: ID) {
    divisionResults(division_Id: $division_Id) {
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
  options: ({ divisionId }) => ({
    variables: {
      division_Id: divisionId,
    },
  }),
  props: ({ data: { networkStatus, error, divisionResults }, ...props }) => ({
    networkStatus,
    error,
    divisionResults,
    ...props,
  }),
};

export default graphql(LEAGUE_TABLE_QUERY, leagueTableOptions);
