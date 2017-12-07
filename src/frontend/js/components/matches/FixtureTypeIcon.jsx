import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import { toTitleCase } from 'util/cshc';
import { FixtureType } from 'util/constants';

/**
 * Icon representation of a fixture (friendly/league/cup etc).
 */
const FixtureTypeIcon = ({ fixtureType }) => {
  const className = classnames('fa', {
    'fa-table': fixtureType === FixtureType.League.toUpperCase(),
    'fa-trophy': fixtureType === FixtureType.Cup.toUpperCase(),
    'fa-smile-o': fixtureType === FixtureType.Friendly.toUpperCase(),
  });
  const title = `${toTitleCase(fixtureType)} match`;
  return <i className={className} title={title} />;
};

FixtureTypeIcon.propTypes = {
  fixtureType: PropTypes.oneOf([
    FixtureType.Friendly.toUpperCase(),
    FixtureType.Cup.toUpperCase(),
    FixtureType.League.toUpperCase(),
  ]).isRequired,
};

export default FixtureTypeIcon;
