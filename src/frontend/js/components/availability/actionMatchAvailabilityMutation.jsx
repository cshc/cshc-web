import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

export const ACTION_MATCH_AVAILABILITY_MUTATION = gql`
  mutation ActionMatchAvailability($input: ActionMatchAvailabilityInput!) {
    actionMatchAvailability(input: $input) {
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

export const actionMatchAvailabilityOptions = {
  props: ({ mutate }) => ({
    onActionAvailability: actionMatchAvailabilityInput =>
      mutate({ variables: { input: { availability: actionMatchAvailabilityInput } } }),
  }),
};

export default graphql(ACTION_MATCH_AVAILABILITY_MUTATION, actionMatchAvailabilityOptions);
