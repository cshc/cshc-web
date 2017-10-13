import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

export const MATCH_LIST_QUERY = gql`
  query MatchList($venue_Name: String) {
    matches(venue_Name: $venue_Name) {
      edges {
        node {
          id
          ourTeam {
            id
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
              id
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
              id
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
  }),
  props: ({ data: { networkStatus, error, matches }, ...props }) => ({
    networkStatus,
    error,
    matches,
    ...props,
  }),
};

export default graphql(MATCH_LIST_QUERY, matchListOptions);
