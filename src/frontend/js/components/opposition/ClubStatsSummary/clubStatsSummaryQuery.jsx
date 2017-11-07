import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

export const CLUB_STATS_QUERY = gql`
  query ClubStatsQuery($club_Slug: String!) {
    oppositionClubStats(club_Slug: $club_Slug) {
      edges {
        node {
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
    oppositionClubStats,
    ...props,
  }),
};

export default graphql(CLUB_STATS_QUERY, clubStatsOptions);
