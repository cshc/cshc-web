import React from 'react';
import PropTypes from 'prop-types';
import groupBy from 'lodash/groupBy';
import keys from 'lodash/keys';
import sortBy from 'lodash/sortBy';
import { Timeline2, Timeline2Item, CustomScrollbar } from 'components/Unify';
import Urls from 'util/urls';

/**
 *  A list of committee memberships, grouped by season.
 */
const CommitteeMemberships = ({ data }) => {
  // Group committee memberships by season
  const grouped = groupBy(data.edges, e => e.node.season.slug);
  // Sort by (descending) season (most recent season first)
  const sorted = sortBy(keys(grouped), seasonSlug => -parseInt(seasonSlug.split('-')[0], 10));

  return (
    <CustomScrollbar maxHeight="200px">
      <Timeline2 className="g-pb-40">
        {sorted.map(seasonSlug => (
          <Timeline2Item
            key={seasonSlug}
            dateSmall={
              <a
                href={Urls.about_committee_season(seasonSlug)}
                title={`View ${seasonSlug} Committee details`}
              >
                {seasonSlug}
              </a>
            }
          >
            {grouped[seasonSlug].map(edge => (
              <h6 className="h6" key={edge.node.position.name}>
                {edge.node.position.name}
              </h6>
            ))}
          </Timeline2Item>
        ))}
      </Timeline2>
    </CustomScrollbar>
  );
};

CommitteeMemberships.propTypes = {
  data: PropTypes.shape().isRequired,
};

export default CommitteeMemberships;
