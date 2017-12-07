import gql from 'graphql-tag';
import { compose, graphql } from 'react-apollo';
import withApolloResults from 'components/common/ApolloResults';
import { withApollo } from 'react-apollo/withApollo';

export const MATCH_LIST_QUERY = gql`
  query MatchList(
    $venue_Name: String
    $season_Slug: String
    $ourTeam_Slug: String
    $oppTeam_Club_Slug: String
    $appearances_Member_Id: ID
  ) {
    matches(
      venue_Name: $venue_Name
      season_Slug: $season_Slug
      ourTeam_Slug: $ourTeam_Slug
      oppTeam_Club_Slug: $oppTeam_Club_Slug
      appearances_Member_Id: $appearances_Member_Id
    ) {
      edges {
        node {
          id
          modelId
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
            member {
              modelId
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
          appearances {
            member {
              modelId
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
  }
`;

export const matchListOptions = {
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

export default compose(graphql(MATCH_LIST_QUERY, matchListOptions), withApolloResults);
