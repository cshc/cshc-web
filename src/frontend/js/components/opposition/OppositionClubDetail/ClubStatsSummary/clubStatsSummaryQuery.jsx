import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';

export const CLUB_STATS_QUERY = gql`
  query ClubStatsQuery($club_Slug: String!) {
    oppositionClubStats(club_Slug: $club_Slug) {
      results(pageSize: 100) {
        team {
          shortName
          slug
        }
        homePlayed
        homeWon
        homeDrawn
        homeLost
        homeGf
        homeGa
        awayPlayed
        awayWon
        awayDrawn
        awayLost
        awayGf
        awayGa
        totalPlayed
        totalWon
        totalDrawn
        totalLost
        totalGf
        totalGa
      }
    }
  }
`;

export const clubStatsOptions = {
  options: ({ clubSlug }) => ({
    variables: {
      club_Slug: clubSlug,
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
