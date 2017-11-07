import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

export const MATCH_LIST_QUERY = gql`
  query MatchList(
    $venue_Name: String
    $season_Slug: String
    $ourTeam_Slug: String
    $oppTeam_Club_Slug: String
  ) {
    matches(
      venue_Name: $venue_Name
      season_Slug: $season_Slug
      ourTeam_Slug: $ourTeam_Slug
      oppTeam_Club_Slug: $oppTeam_Club_Slug
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
    matches,
    ...props,
  }),
};

export default graphql(MATCH_LIST_QUERY, matchListOptions);
