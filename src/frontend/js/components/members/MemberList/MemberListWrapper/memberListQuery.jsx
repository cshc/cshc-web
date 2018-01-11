import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';
import { NoFilter } from 'util/constants';
import Member from 'models/member';

export const MEMBER_LIST_QUERY = gql`
  query MemberList(
    $name: String
    $isCurrent: Boolean
    $gender: String
    $appearances_Match_Season_Slug: String
    $appearances_Match_OurTeam_Slug: String
    $prefPosition_In: String
    $teamcaptaincy_Season_Slug: String
  ) {
    members(
      name: $name
      isCurrent: $isCurrent
      gender: $gender
      appearances_Match_Season_Slug: $appearances_Match_Season_Slug
      appearances_Match_OurTeam_Slug: $appearances_Match_OurTeam_Slug
      prefPosition_In: $prefPosition_In
      teamcaptaincy_Season_Slug: $teamcaptaincy_Season_Slug
    ) {
      results(pageSize: 1000) {
        firstName
        lastName
        id
        gender
        shirtNumber
        prefPosition
        addrPosition
        numAppearances
        goals
      }
    }
  }
`;

export const memberListOptions = {
  options: ({ currentSeason, textSearch, current, captains, gender, position, team }) => ({
    variables: {
      name: textSearch || undefined,
      isCurrent: current || undefined,
      gender: gender !== NoFilter ? gender : undefined,
      prefPosition_In: Member.getPreferredPositions(position),
      appearances_Match_OurTeam_Slug: team && team !== NoFilter ? team : undefined,
      appearances_Match_Season_Slug: team && team !== NoFilter ? currentSeason : undefined,
      teamcaptaincy_Season_Slug: captains ? currentSeason : undefined,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, members }, ...props }) => ({
    networkStatus,
    error,
    data: members,
    ...props,
  }),
};

export default compose(graphql(MEMBER_LIST_QUERY, memberListOptions), withApolloResults);
