import React from 'react';
import PropTypes from 'prop-types';
import { MatchItem } from 'util/constants';
import MatchData from 'components/matches/MatchData';
import Urls from 'util/urls';

const MatchDetail = ({ ourTeam, oppTeam, data }) => (data.results ? (
  <div>
    <p>
        This table lists the most recent matches between {ourTeam.longName} and {oppTeam.name}. A
        full list of matches between {ourTeam.longName} and {oppTeam.club.name} can be found{' '}
      <a href={`${Urls.match_list()}?opposition=${oppTeam.club.slug}&team=${ourTeam.slug}`}>
          here
      </a>.
    </p>
    <MatchData
      matches={data.results}
      exclude={[MatchItem.opposition, MatchItem.ourTeam]}
      dateFormat="Do MMM YY"
    />
  </div>
) : (
  <p>
    {ourTeam.name} and {oppTeam.longName} have not played each other before. A full list of
      matches between {ourTeam.longName} and {oppTeam.club.name} can be found{' '}
    <a href={`${Urls.match_list()}?opposition=${oppTeam.club.slug}&team=${ourTeam.slug}`}>
        here
    </a>.
  </p>
));

MatchDetail.propTypes = {
  ourTeam: PropTypes.shape({
    slug: PropTypes.string,
    longName: PropTypes.string,
  }).isRequired,
  oppTeam: PropTypes.shape({
    name: PropTypes.string,
    club: PropTypes.shape({
      slug: PropTypes.string,
      name: PropTypes.string,
    }),
  }).isRequired,
  data: PropTypes.shape().isRequired,
};

export default MatchDetail;
