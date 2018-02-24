import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

export const ADD_MEMBER_MUTATION = gql`
  mutation AddMember($input: AddMemberInput!) {
    addMember(input: $input) {
      newMember {
        id
        fullName
      }
    }
  }
`;

export const addMemberOptions = {
  props: ({ mutate }) => ({
    onAddMember: (firstName, lastName, gender) =>
      mutate({ variables: { input: { member: { firstName, lastName, gender } } } }),
  }),
};

export default graphql(ADD_MEMBER_MUTATION, addMemberOptions);
