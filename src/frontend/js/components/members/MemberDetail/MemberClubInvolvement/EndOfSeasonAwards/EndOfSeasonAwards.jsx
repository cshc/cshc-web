import React from 'react';
import PropTypes from 'prop-types';
import groupBy from 'lodash/groupBy';
import keys from 'lodash/keys';
import Urls from 'util/urls';
import { Timeline2, Timeline2Item, CustomScrollbar } from 'components/Unify';

/**
 *  A list of end of season awards, grouped by season
 */
const EndOfSeasonAwards = ({ data }) => {
  // Group awards by season
  const grouped = groupBy(data.results, awardWinner => awardWinner.season.slug);
  return (
    <CustomScrollbar maxHeight="200px">
      <Timeline2 className="g-pb-40">
        {keys(grouped).map((seasonSlug) => {
          const seasonNode = (
            <a href={`${Urls.eos_award_winners()}?season=${seasonSlug}`}>{seasonSlug}</a>
          );
          return (
            <Timeline2Item key={seasonSlug} dateSmall={seasonNode}>
              {grouped[seasonSlug].map(awardWinner => (
                <h6 className="h6" key={awardWinner.award.name}>
                  {awardWinner.award.name}
                </h6>
              ))}
            </Timeline2Item>
          );
        })}
      </Timeline2>
    </CustomScrollbar>
  );
};

EndOfSeasonAwards.propTypes = {
  data: PropTypes.shape().isRequired,
};

export default EndOfSeasonAwards;
