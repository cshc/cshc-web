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
    $isUmpire: Boolean
    $isCoach: Boolean
    $squadmembership_Season_Slug: String
    $squadmembership_Team_Slug: String
    $prefPosition_In: String
    $teamcaptaincy_Season_Slug: String
    $appearances_Match_Season_Slug: String
    $appearances_Match_OurTeam_Slug: String
  ) {
    members(
      name: $name
      isCurrent: $isCurrent
      gender: $gender
      isUmpire: $isUmpire
      isCoach: $isCoach
      squadmembership_Season_Slug: $squadmembership_Season_Slug
      squadmembership_Team_Slug: $squadmembership_Team_Slug
      prefPosition_In: $prefPosition_In
      teamcaptaincy_Season_Slug: $teamcaptaincy_Season_Slug
      appearances_Match_Season_Slug: $appearances_Match_Season_Slug
      appearances_Match_OurTeam_Slug: $appearances_Match_OurTeam_Slug
    ) {
      results(pageSize: 5000) {
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
  options: ({
    currentSeason,
    textSearch,
    current,
    captains,
    umpires,
    coaches,
    gender,
    position,
    team,
    season,
  }) => ({
    variables: {
      name: textSearch || undefined,
      isCurrent: current || undefined,
      gender: gender !== NoFilter ? gender : undefined,
      isUmpire: umpires || undefined,
      isCoach: coaches || undefined,
      prefPosition_In: Member.getPreferredPositions(position),
      squadmembership_Season_Slug: undefined,
      squadmembership_Team_Slug: undefined,
      teamcaptaincy_Season_Slug: captains ? (season && season !== NoFilter ? season : currentSeason) : undefined,
      appearances_Match_Season_Slug: season && season !== NoFilter ? season : undefined,
      appearances_Match_OurTeam_Slug: team && team !== NoFilter ? team : undefined,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data, ...props }) => ({
    networkStatus: data.networkStatus,
    loading: data.loading,
    error: data.error,
    data: data.members,
    loadingMessage: 'Loading members...',
    ...props,
  }),
};

export default compose(graphql(MEMBER_LIST_QUERY, memberListOptions), withApolloResults);
