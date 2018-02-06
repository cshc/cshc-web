import React from 'react';
import PropTypes from 'prop-types';
import Accordion from 'components/common/Accordion';
import MatchEditTopBar from './MatchEditTopBar';
import Result from './Result';
import Appearances from './Appearances';
import AwardWinners from './AwardWinners';
import Report from './Report';
import { AccordionId } from './util';

/**
 *  The top-level component for the Match Edit app.
 * 
 *  This component basically consists of a sticky top bar with Save and Cancel
 *  options and an accordion that wraps the various sections of the form.
 */
const MatchEdit = ({ matchId, ourTeam, oppTeam, ourTeamGender }) => (
  <div>
    <MatchEditTopBar matchId={matchId} />
    <section className="container g-pt-0 g-pb-40">
      <Accordion multiselectable accordionId={AccordionId}>
        <Result ourTeam={ourTeam} oppTeam={oppTeam} />
        <Appearances ourTeamGender={ourTeamGender} />
        <AwardWinners />
        <Report />
      </Accordion>
    </section>
  </div>
);

MatchEdit.propTypes = {
  matchId: PropTypes.number.isRequired,
  ourTeamGender: PropTypes.string.isRequired,
  ourTeam: PropTypes.string.isRequired,
  oppTeam: PropTypes.string.isRequired,
};

MatchEdit.defaultProps = {};

export default MatchEdit;
