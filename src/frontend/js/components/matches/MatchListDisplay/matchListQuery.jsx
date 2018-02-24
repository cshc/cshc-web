import gql from 'graphql-tag';
import { graphql } from 'react-apollo';
import { djangoDate } from 'util/cshc';

export const MATCH_LIST_QUERY = gql`
  query MatchList(
    $page: Int
    $pageSize: Int
    $orderBy: String
    $ourTeam_Gender: String
    $ourTeam_Slug: String
    $ourTeamId: ID
    $oppTeamId: ID
    $oppTeam_Club_Slug: String
    $season_Slug: String
    $fixtureType: String
    $venueId: ID
    $date: String
    $reportAuthorId: ID
    $appearances_MemberId_In: ID
    $mom: String
    $lom: String
    $result: String
  ) {
    matches(
      orderBy: $orderBy
      ourTeam_Gender: $ourTeam_Gender
      ourTeam_Slug: $ourTeam_Slug
      ourTeamId: $ourTeamId
      oppTeamId: $oppTeamId
      oppTeam_Club_Slug: $oppTeam_Club_Slug
      season_Slug: $season_Slug
      fixtureType: $fixtureType
      venueId: $venueId
      date: $date
      reportAuthorId: $reportAuthorId
      appearances_MemberId_In: $appearances_MemberId_In
      mom: $mom
      lom: $lom
      result: $result
    ) {
      totalCount
      results(page: $page, pageSize: $pageSize) {
        reportAuthor {
          id
        }
        id
        venue {
          name
          shortName
          slug
        }
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

export const matchListOptions = {
  options: ({ queryVariables }) => ({
    variables: {
      ...queryVariables,
      date: queryVariables.date ? djangoDate(queryVariables.date) : undefined,
    },
    fetchPolicy: 'cache-and-network',
  }),
  props: ({ ownProps, data: { networkStatus, error, matches }, ...props }) => ({
    networkStatus,
    error,
    matches,
    ...ownProps,
    ...props,
  }),
};

export default graphql(MATCH_LIST_QUERY, matchListOptions);
