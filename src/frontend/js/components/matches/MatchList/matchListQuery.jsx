/* @flow */

import gql from 'graphql-tag';
import { graphql } from 'react-apollo';

type Props = {
  matchFilters: Object,
};

export const MATCH_LIST_QUERY = gql`
  query MatchList($venue_Name: String) {
    matches(venue_Name: $venue_Name) {
      edges {
        node {
          id
          ourTeam {
            longName
            shortName
            gender
            ordinal
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
              firstName
              lastName
            }
            awardee
            comment
            award {
              name
            }
          }
          appearances {
            member {
              firstName
              lastName
            }
            goals
            greenCard
            yellowCard
            redCard
          }
          homeAway
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
  options: ({ matchFilters }: Props) => ({
    variables: matchFilters,
  }),
  props: ({ data: { networkStatus, error, matches } }) => ({
    networkStatus,
    error,
    matches,
  }),
};

export default graphql(MATCH_LIST_QUERY, matchListOptions);
