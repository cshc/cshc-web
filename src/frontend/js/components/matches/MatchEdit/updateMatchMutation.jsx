import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

export const UPDATE_MATCH_MUTATION = gql`
  mutation EditMatch($input: UpdateMatchInput!) {
    updateMatch(input: $input) {
      errors
      match {
        id
      }
    }
  }
`;

export const updateMatchOptions = {
  props: ({ mutate }) => ({
    onUpdateMatch: editMatchInput => mutate({ variables: { input: { match: editMatchInput } } }),
  }),
};

export default graphql(UPDATE_MATCH_MUTATION, updateMatchOptions);
