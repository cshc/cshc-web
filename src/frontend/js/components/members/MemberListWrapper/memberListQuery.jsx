import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import { FilterName, NoFilter } from 'util/constants';
import Member from 'models/member';

export const MEMBER_LIST_QUERY = gql`
  query MemberList(
    $isCurrent: Boolean
    $gender: String
    $appearances_Match_Season_Slug: String
    $appearances_Match_OurTeam_Slug: String
    $prefPosition_In: String
  ) {
    members(
      isCurrent: $isCurrent
      gender: $gender
      appearances_Match_Season_Slug: $appearances_Match_Season_Slug
      appearances_Match_OurTeam_Slug: $appearances_Match_OurTeam_Slug
      prefPosition_In: $prefPosition_In
    ) {
      edges {
        node {
          firstName
          lastName
          id
          modelId
          gender
          prefPosition
          addrPosition
          numAppearances
          goals
        }
      }
    }
  }
`;

export const memberListOptions = {
  options: ({ currentSeason, activeFilters }) => ({
    variables: {
      isCurrent: activeFilters[FilterName.Current] || undefined,
      gender:
        activeFilters[FilterName.Gender] !== NoFilter
          ? activeFilters[FilterName.Gender]
          : undefined,
      prefPosition_In: Member.getPreferredPositions(activeFilters[FilterName.Position]),
      appearances_Match_OurTeam_Slug:
        activeFilters[FilterName.Team] !== NoFilter ? activeFilters[FilterName.Team] : undefined,
      appearances_Match_Season_Slug:
        activeFilters[FilterName.Team] !== NoFilter ? currentSeason : undefined,
    },
    fetchPolicy: 'cache-first',
  }),
  props: ({ data: { networkStatus, error, members }, ...props }) => ({
    networkStatus,
    error,
    members,
    ...props,
  }),
};

export default graphql(MEMBER_LIST_QUERY, memberListOptions);
