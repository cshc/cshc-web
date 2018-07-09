import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';
import { NoFilter } from 'util/constants';

export const MEMBER_STATS_QUERY = gql`
  query MemberStats($memberId: Int!, $fixtureType: String) {
    memberStats(memberId: $memberId, fixtureType: $fixtureType) {
      season {
        slug
      }
      memberStats {
        played
        won
        drawn
        lost
        goals
        goalsFor
        goalsAgainst
        totalPoints
        cleanSheets
        mom
        lom
        teamRepresentations {
          team {
            slug
            shortName
            position
          }
          appearanceCount
        }
      }
    }
    clubTeams {
      results(pageSize: 50) {
        id
        shortName
        slug
        ordinal
        gender
      }
    }
  }
`;

export const memberStatsOptions = {
  options: ({ memberId, fixtureType }) => ({
    variables: {
      memberId,
      fixtureType: fixtureType === NoFilter ? undefined : fixtureType,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({
    ownProps,
    fixtureType,
    data: { networkStatus, error, memberStats, clubTeams },
    ...props
  }) => ({
    networkStatus,
    error,
    clubTeams,
    data: memberStats,
    loadingMessage: 'Loading member stats...',
    ...props,
  }),
};

export default compose(graphql(MEMBER_STATS_QUERY, memberStatsOptions), withApolloResults);
