import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import { format, startOfToday } from 'date-fns';

/** 
 * GraphQL query to fetch the upcoming match availabilities for a particular member.
*/
export const MEMBER_AVAILABILITY_QUERY = gql`
  query MatchAvailabilitiesForMember($memberId: ID, $today: String!) {
    matchAvailabilities(memberId: $memberId, match_Date_Gte: $today) {
      results(pageSize: 1000) {
        id
        match {
          id
          isHome
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
        playingAvailability
        umpiringAvailability
        comment
      }
    }
  }
`;

export const memberAvailabilityOptions = {
  options: ({ member }) => ({
    variables: {
      memberId: member.id,
      today: format(startOfToday(), 'YYYY-MM-DD'),
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ ownProps, data: { networkStatus, error, matchAvailabilities }, ...props }) => ({
    networkStatus,
    error,
    matchAvailabilities: matchAvailabilities
      ? matchAvailabilities.results.filter(
        a => (ownProps.umpiring ? a.umpiringAvailability : a.playingAvailability),
      )
      : [],
    ...ownProps,
    ...props,
  }),
};

export default graphql(MEMBER_AVAILABILITY_QUERY, memberAvailabilityOptions);
