import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';

export const END_OF_SEASON_AWARDS_QUERY = gql`
  query EndOfSeasonAwards($memberId: ID!) {
    endOfSeasonAwardWinners(memberId: $memberId) {
      results(pageSize: 1000) {
        season {
          slug
        }
        award {
          name
        }
      }
    }
  }
`;

export const endOfSeasonAwardsOptions = {
  options: ({ memberId }) => ({
    variables: {
      memberId,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ ownProps, data: { networkStatus, error, endOfSeasonAwardWinners }, ...props }) => ({
    networkStatus,
    error,
    data: endOfSeasonAwardWinners,
    ...props,
  }),
};

export default compose(
  graphql(END_OF_SEASON_AWARDS_QUERY, endOfSeasonAwardsOptions),
  withApolloResults,
);
