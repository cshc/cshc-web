import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import { DefaultPageSize } from 'util/constants';

export const EOS_LIST_QUERY = gql`
  query EndOfSeasonAwardWinners(
    $page: Int
    $pageSize: Int
    $orderBy: String
    $season_Slug: String
    $award: ID
    $memberId: ID
  ) {
    endOfSeasonAwardWinners(
      orderBy: $orderBy
      season_Slug: $season_Slug
      award: $award
      memberId: $memberId
    ) {
      totalCount
      results(page: $page, pageSize: $pageSize) {
        award {
          id
          name
        }
        awardee
        member {
          id
          firstName
          lastName
        }
        comment
        season {
          slug
        }
      }
    }
  }
`;

export const eosListOptions = {
  options: ({ page, pageSize, orderBy, season, award, member }) => ({
    variables: {
      page: page || 1,
      pageSize: pageSize || 20,
      orderBy,
      season_Slug: season,
      award,
      memberId: member,
    },
  }),
  props: ({ ownProps, data: { networkStatus, error, endOfSeasonAwardWinners }, ...props }) => ({
    networkStatus,
    error,
    endOfSeasonAwardWinners,
    ...ownProps,
    ...props,
    pageSize: ownProps.pageSize || 20,
    page: ownProps.page || 1,
  }),
};

export default graphql(EOS_LIST_QUERY, eosListOptions);
