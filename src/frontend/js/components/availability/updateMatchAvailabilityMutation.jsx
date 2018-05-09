import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

/** 
 * Mutation to update the availability (playing or umpiring) for a 
 * particular member and match.
*/
export const UPDATE_MATCH_AVAILABILITY_MUTATION = gql`
  mutation UpdateAvailability($input: UpdateMatchAvailabilityInput!) {
    updateMatchAvailability(input: $input) {
      errors
      availability {
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
`;

export const updateMatchAvailabilityOptions = {
  props: ({ mutate }) => ({
    onUpdateAvailability: availability => mutate({ variables: { input: { availability } } }),
  }),
};

export default graphql(UPDATE_MATCH_AVAILABILITY_MUTATION, updateMatchAvailabilityOptions);
