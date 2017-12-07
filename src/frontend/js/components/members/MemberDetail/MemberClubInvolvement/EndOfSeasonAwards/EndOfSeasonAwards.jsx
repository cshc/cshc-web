import React from 'react';
import PropTypes from 'prop-types';
import groupBy from 'lodash/groupBy';
import keys from 'lodash/keys';
import { Timeline2, Timeline2Item, CustomScrollbar } from 'components/Unify';

/**
 *  A list of end of season awards, grouped by season
 */
const EndOfSeasonAwards = ({ data }) => {
  // Group awards by season
  const grouped = groupBy(data.edges, e => e.node.season.slug);
  return (
    <CustomScrollbar maxHeight="200px">
      <Timeline2 className="g-pb-40">
        {keys(grouped).map(seasonSlug => (
          <Timeline2Item key={seasonSlug} dateSmall={seasonSlug}>
            {grouped[seasonSlug].map(edge => (
              <h6 className="h6" key={edge.node.award.name}>
                {edge.node.award.name}
              </h6>
            ))}
          </Timeline2Item>
        ))}
      </Timeline2>
    </CustomScrollbar>
  );
};

EndOfSeasonAwards.propTypes = {
  data: PropTypes.shape().isRequired,
};

export default EndOfSeasonAwards;
