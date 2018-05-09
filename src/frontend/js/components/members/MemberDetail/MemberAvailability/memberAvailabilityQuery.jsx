import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import format from 'date-fns/format';
import startOfToday from 'date-fns/start_of_today';

/** 
 * GraphQL query to fetch the upcoming match availabilities for a particular member.
*/
export const MEMBER_AVAILABILITY_QUERY = gql`
  query MatchAvailabilitiesForMember($availabilityType: String!, $memberId: ID, $today: String!) {
    matchAvailabilities(
      availabilityType: $availabilityType
      memberId: $memberId
      match_Date_Gte: $today
    ) {
      results(pageSize: 1000) {
        id
        match {
          id
          ourTeam {
            slug
            shortName
          }
          oppTeam {
            name
            slug
          }
          date
          time
          venue {
            name
            slug
          }
        }
        availability
        comment
      }
    }
  }
`;

export const memberAvailabilityOptions = {
  options: ({ member, availabilityType }) => ({
    variables: {
      memberId: member.id,
      availabilityType,
      today: format(startOfToday(), 'YYYY-MM-DD'),
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ ownProps, data: { networkStatus, error, matchAvailabilities }, ...props }) => ({
    networkStatus,
    error,
    matchAvailabilities: matchAvailabilities ? matchAvailabilities.results : [],
    ...ownProps,
    ...props,
  }),
};

export default graphql(MEMBER_AVAILABILITY_QUERY, memberAvailabilityOptions);
