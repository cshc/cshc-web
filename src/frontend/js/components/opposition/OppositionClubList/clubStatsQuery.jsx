import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';

export const CLUB_STATS_QUERY = gql`
  query ClubStatsQuery {
    oppositionClubStats {
      results(pageSize: 500) {
        club {
          name
          slug
        }
        totalPlayed
        totalWon
        totalDrawn
        totalLost
        avgGf
        avgGa
        avgGd
        avgPoints
      }
    }
  }
`;

export const clubStatsOptions = {
  options: ({}) => ({
    variables: {
      team_Slug: null,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, oppositionClubStats }, ...props }) => ({
    networkStatus,
    error,
    data: oppositionClubStats,
    loadingMessage: 'Loading club stats...',
    ...props,
  }),
};

export default compose(graphql(CLUB_STATS_QUERY, clubStatsOptions), withApolloResults);
