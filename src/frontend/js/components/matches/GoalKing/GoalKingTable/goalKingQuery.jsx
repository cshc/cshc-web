import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';
import { NoFilter } from 'util/constants';

export const GOAL_KING_QUERY = gql`
  query GoalKing($member_Gender: String, $season_Slug: String, $team: String) {
    goalKingEntries(member_Gender: $member_Gender, season_Slug: $season_Slug, team: $team) {
      results(pageSize: 1000) {
        member {
          firstName
          lastName
          gender
          id
        }
        m1Goals
        m2Goals
        m3Goals
        m4Goals
        m5Goals
        m6Goals
        mvGoals
        mindGoals
        l1Goals
        l2Goals
        l3Goals
        l4Goals
        l5Goals
        l6Goals
        l7Goals
        lvGoals
        lindGoals
        mixedAGoals
        mixedBGoals
        totalGoals
        gpg
      }
    }
  }
`;

export const goalKingOptions = {
  options: ({ season, team }) => ({
    variables: {
      season_Slug: season,
      team: team !== NoFilter ? team : undefined,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, goalKingEntries }, ...props }) => ({
    networkStatus,
    error,
    data: goalKingEntries,
    loadingMessage: 'Loading...',
    ...props,
  }),
};

export default compose(graphql(GOAL_KING_QUERY, goalKingOptions), withApolloResults);
