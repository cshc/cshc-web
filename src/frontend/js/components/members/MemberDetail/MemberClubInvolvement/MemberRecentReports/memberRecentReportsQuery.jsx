import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';

export const MEMBER_REPORTS_QUERY = gql`
  query MemberReports(
    $page: Int
    $pageSize: Int
    $orderBy: String
    $reportAuthorId: ID
    $date_Lte: Date
  ) {
    matches(orderBy: $orderBy, reportAuthorId: $reportAuthorId, date_Lte: $date_Lte) {
      results(pageSize: $pageSize, page: $page) {
        id
        date
        matchTitleText
      }
    }
  }
`;

export const memberReportsOptions = {
  options: ({ matchFilters }) => ({
    variables: matchFilters,
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, matches }, ...props }) => ({
    networkStatus,
    error,
    loadingMessage: 'Loading reports...',
    matches,
    ...props,
  }),
};

export default compose(graphql(MEMBER_REPORTS_QUERY, memberReportsOptions), withApolloResults);
