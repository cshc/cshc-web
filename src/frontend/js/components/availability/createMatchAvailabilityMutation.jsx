import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

/** 
 * Mutation to update the availability (playing or umpiring) for a 
 * particular member and match.
*/
export const CREATE_MATCH_AVAILABILITY_MUTATION = gql`
  mutation CreateAvailability($input: CreateMatchAvailabilityInput!) {
    createMatchAvailability(input: $input) {
      errors
      matchAvailabilities {
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

export const createMatchAvailabilityOptions = {
  props: ({ mutate }) => ({
    onCreateAvailability: availability => mutate({ variables: { input: { availability } } }),
  }),
};

export default graphql(CREATE_MATCH_AVAILABILITY_MUTATION, createMatchAvailabilityOptions);
