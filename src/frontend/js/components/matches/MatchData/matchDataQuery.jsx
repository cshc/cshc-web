import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';

export const MATCH_DATA_QUERY = gql`
  query MatchList(
    $page: Int
    $pageSize: Int
    $orderBy: String
    $venue_Slug: String
    $season_Slug: String
    $ourTeam_Slug: String
    $oppTeam_Club_Slug: String
    $appearances_MemberId_In: ID
    $appearances_MemberId: ID
    $date_Lte: String
  ) {
    matches(
      orderBy: $orderBy
      venue_Slug: $venue_Slug
      season_Slug: $season_Slug
      ourTeam_Slug: $ourTeam_Slug
      oppTeam_Club_Slug: $oppTeam_Club_Slug
      appearances_MemberId_In: $appearances_MemberId_In
      appearances_MemberId: $appearances_MemberId
      date_Lte: $date_Lte
    ) {
      results(pageSize: $pageSize, page: $page) {
        id
        ourTeam {
          id
          slug
          longName
          shortName
          gender
          ordinal
          position
        }
        oppTeam {
          name
          shortName
          gender
          slug
          club {
            name
            slug
            kitClashMen
            kitClashLadies
            kitClashMixed
          }
        }
        venue {
          name
          shortName
          slug
        }
        awardWinners {
          results(pageSize: 100) {
            member {
              firstName
              lastName
              gender
              thumbUrl(profile: "member-link")
              shirtNumber
            }
            awardee
            comment
            award {
              name
            }
          }
        }
        appearances {
          results(pageSize: 100) {
            member {
              firstName
              lastName
              gender
              thumbUrl(profile: "member-link")
              shirtNumber
            }
            goals
            greenCard
            yellowCard
            redCard
          }
        }
        homeAway
        hasReport
        kitClash
        fixtureType
        date
        time
        altOutcome
        ourScore
        oppScore
      }
    }
  }
`;

export const matchDataOptions = {
  options: ({ matchFilters }) => ({
    variables: matchFilters,
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ data: { networkStatus, error, matches }, ...props }) => ({
    networkStatus,
    error,
    data: matches,
    ...props,
  }),
};

export default compose(graphql(MATCH_DATA_QUERY, matchDataOptions), withApolloResults);
