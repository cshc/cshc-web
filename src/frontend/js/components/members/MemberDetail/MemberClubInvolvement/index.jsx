import React from 'react';
import PropTypes from 'prop-types';
import Urls from 'util/urls';
import { Subheading, Panel } from 'components/Unify';
import CommitteeMemberships from './CommitteeMemberships';
import EndOfSeasonAwards from './EndOfSeasonAwards';
// import MemberRecentMatches from './MemberRecentMatches';

// <MemberRecentMatches
// matchFilters={{ appearances_Member_Id: memberId }}
// showViewTypeSwitcher={false}
// />

/**
 * Top-level component for a member's Club Involvement.
 * 
 * Contains the following sections:
 * 1) Recent Matches
 * 2) Committee Positions
 * 3) End of Season awards
 * 4) Recent Match Reports written by this member
 */
const MemberClubInvolvement = ({ memberId }) => {
  const panelProps = { outlineColor: 'teal', headerColor: 'teal' };
  return (
    <div>
      <Subheading text="Club Involvement" />
      <Panel title="Recent Matches" {...panelProps}>
        <div className="card-block">
          <p>
            Note: you can view/filter/sort all matches that Graham played in{' '}
            <a href={Urls.get('match_list')} title="Match List">
              here
            </a>. This table just lists the most recent matches.
          </p>
        </div>
      </Panel>
      <div className="row">
        <div className="col-md-6 g-mb-20">
          <Panel className="g-mb-0 g-height-100x" title="Committee Positions" {...panelProps}>
            <div className="card-block">
              <p>
                Full details of the CSHC committee for each year can be found{' '}
                <a href={Urls.get('about_committee')} title="Committee Details">
                  here
                </a>. Alternatively, click on a year in the timeline below to see the full committee
                for that year.
              </p>
              <CommitteeMemberships memberId={memberId} />
            </div>
          </Panel>
        </div>
        <div className="col-md-6 g-mb-20">
          <Panel className="g-mb-0 g-height-100x" title="End of Season Awards" {...panelProps}>
            <div className="card-block">
              <p>
                All award winners for each year can be found{' '}
                <a href="#" title="TODO">
                  here
                </a>. Alternatively, click on a year in the timeline below to see the list of award
                winners for that year.
              </p>
              <EndOfSeasonAwards memberId={memberId} />
            </div>
          </Panel>
        </div>
        <div className="col-md-6 g-mb-20">
          <Panel className="g-mb-0 g-height-100x" title="Recent Match Reports" {...panelProps} />
        </div>
      </div>
    </div>
  );
};

MemberClubInvolvement.propTypes = {
  memberId: PropTypes.number.isRequired,
};

MemberClubInvolvement.defaultProps = {};

export default MemberClubInvolvement;
