import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import { format, startOfToday } from 'date-fns';
import { DefaultPageSize } from 'util/constants';

/** 
 * GraphQL query to fetch the upcoming match availabilities.
*/
export const MATCH_AVAILABILITY_QUERY = gql`
  query MatchAvailabilities(
    $teamId: ID
    $today: String!
    $page: Int
    $pageSize: Int
    $availabilityType: String
  ) {
    matches(ourTeamId: $teamId, date_Gte: $today) {
      totalCount
      results(page: $page, pageSize: $pageSize) {
        id
        date
        time
        homeAway
        ourTeam {
          id
          shortName
          slug
        }
        oppTeam {
          id
          name
          club {
            id
            slug
          }
        }
        venue {
          id
          slug
          name
          shortName
        }
        availabilities(availabilityType: $availabilityType) {
          results(pageSize: 1000) {
            id
            availability
            comment
            member {
              id
              firstName
              lastName
            }
          }
        }
      }
    }
  }
`;

export const matchAvailabilityOptions = {
  options: ({ teamId, availabilityType, page, pageSize }) => ({
    variables: {
      page: page || 1,
      pageSize: pageSize || DefaultPageSize,
      teamId,
      today: format(startOfToday(), 'YYYY-MM-DD'),
      availabilityType,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ ownProps, data: { networkStatus, error, matches }, ...props }) => ({
    networkStatus,
    error,
    matches,
    ...ownProps,
    ...props,
    page: ownProps.page || 1,
    pageSize: ownProps.pageSize || DefaultPageSize,
  }),
};

export default graphql(MATCH_AVAILABILITY_QUERY, matchAvailabilityOptions);
