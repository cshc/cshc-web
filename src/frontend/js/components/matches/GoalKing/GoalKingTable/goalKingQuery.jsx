import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import { FilterName, NoFilter } from 'util/constants';

export const GOAL_KING_QUERY = gql`
  query GoalKing($member_Gender: String, $season_Slug: String, $team: String) {
    goalKingEntries(member_Gender: $member_Gender, season_Slug: $season_Slug, team: $team) {
      edges {
        node {
          member {
            firstName
            lastName
            gender
            modelId
          }
          m1Goals
          m2Goals
          m3Goals
          m4Goals
          m5Goals
          l1Goals
          l2Goals
          l3Goals
          l4Goals
          mixedGoals
          indoorGoals
          totalGoals
          gpg
        }
      }
    }
  }
`;

export const goalKingOptions = {
  options: ({ activeFilters }) => ({
    variables: {
      season_Slug: activeFilters[FilterName.Season] || undefined,
      team:
        activeFilters[FilterName.Team] !== NoFilter ? activeFilters[FilterName.Team] : undefined,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, goalKingEntries }, ...props }) => ({
    networkStatus,
    error,
    entries: goalKingEntries,
    ...props,
  }),
};

export default graphql(GOAL_KING_QUERY, goalKingOptions);
