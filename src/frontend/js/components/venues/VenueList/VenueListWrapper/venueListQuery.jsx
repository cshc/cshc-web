import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';
import { FilterName, NoFilter } from 'util/constants';

export const VENUE_LIST_QUERY = gql`
  query VenueList(
    $isHome: Boolean
    $matches_Season_Slug: String
    $name_Icontains: String
    $matches_OurTeam_Slug: String
    $matches_Division: ID
  ) {
    venues(
      isHome: $isHome
      matches_Season_Slug: $matches_Season_Slug
      name_Icontains: $name_Icontains
      matches_OurTeam_Slug: $matches_OurTeam_Slug
      matches_Division: $matches_Division
    ) {
      edges {
        node {
          name
          id
          modelId
          slug
          phone
          addr1
          addr2
          addr3
          addrCity
          addrPostcode
          distance
          position
          isHome
        }
      }
    }
  }
`;

export const venueListOptions = {
  options: ({ homeGround, season, textSearch, team, division }) => ({
    variables: {
      isHome: homeGround || undefined,
      matches_Season_Slug: season || undefined,
      name_Icontains: textSearch || undefined,
      matches_OurTeam_Slug: team !== NoFilter ? team : undefined,
      matches_Division: division || undefined,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, venues }, ...props }) => ({
    networkStatus,
    error,
    data: venues,
    ...props,
  }),
};

export default compose(graphql(VENUE_LIST_QUERY, venueListOptions), withApolloResults);
