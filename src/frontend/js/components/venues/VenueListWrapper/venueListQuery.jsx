import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import { FilterName } from 'util/constants';

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
  options: ({ activeFilters }) => ({
    variables: {
      isHome: activeFilters[FilterName.HomeGround],
      matches_Season_Slug: activeFilters[FilterName.Season] || undefined,
      name_Icontains: activeFilters[FilterName.TextSearch] || undefined,
      matches_OurTeam_Slug: activeFilters[FilterName.VenueTeam] || undefined,
      matches_Division: activeFilters[FilterName.VenueDivision] || undefined,
    },
    fetchPolicy: 'cache-first',
  }),
  props: ({ data: { networkStatus, error, venues }, ...props }) => ({
    networkStatus,
    error,
    venues,
    ...props,
  }),
};

export default graphql(VENUE_LIST_QUERY, venueListOptions);
