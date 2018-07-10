import React from 'react';
import PropTypes from 'prop-types';
import Member from 'models/member';
import ProgressBar from 'components/common/ProgressBar';
import MemberAvatar from 'components/members/MemberAvatar';
import Urls from 'util/urls';
import styles from './style.scss';

/**
 * 'Card' representation of a club member, with profile pic, stats about games played, 
 * goals scored and win/draw/loss record and a link to their profile.
 */
const SquadRosterCard = ({ memberStats, teamTotals }) => {
  const goalsPercentage = 100 * (memberStats.goals / teamTotals.goals);
  const progressItems = [];
  if (memberStats.won > 0) {
    progressItems.push({
      value: memberStats.won,
      color: '#00ff00',
    });
  }
  if (memberStats.drawn > 0) {
    progressItems.push({
      value: memberStats.drawn,
      color: 'darkgrey',
    });
  }
  if (memberStats.lost > 0) {
    progressItems.push({
      value: memberStats.lost,
      color: 'red',
    });
  }
  return (
    <div className="col-md-6 col-lg-3 g-mb-30">
      <article className="g-bg-white">
        <figure className={styles.imageContainer}>
          <MemberAvatar member={memberStats.member} rounded={false} />
        </figure>
        <div className="u-shadow-v24 g-pa-25">
          <a href={Urls.member_detail(memberStats.member.id)} title="View Profile">
            <h3 className="h5 g-mb-5 text-center">
              {Member.fullName(memberStats.member)}
              {memberStats.isCaptain && ' (C)'}
              {memberStats.isViceCaptain && ' (VC)'}
            </h3>
          </a>
          <div className="d-flex justify-content-between">
            <div className="g-min-width-35">
              {memberStats.mom > 0 && (
                <span>
                  <i className="far fa-star g-mr-3" />
                  {memberStats.mom}
                </span>
              )}
            </div>
            <p className="text-center g-mb-5">
              &nbsp;{memberStats.member.prefPosition !== 'Not known' &&
                memberStats.member.prefPosition}&nbsp;
            </p>
            <div className="g-min-width-35">
              {memberStats.lom > 0 && (
                <span>
                  {memberStats.lom}
                  <i className="far fa-lemon g-ml-3" />
                </span>
              )}
            </div>
          </div>
          <div className="d-flex">
            <div className={styles.progress}>
              <ProgressBar
                label="Played"
                value={memberStats.played}
                progressItems={progressItems}
                max={teamTotals.played}
              />
              <ProgressBar
                label="Goals"
                value={memberStats.goals}
                progressItems={[{ value: goalsPercentage, color: 'blue' }]}
              />
            </div>
          </div>
        </div>
      </article>
    </div>
  );
};

SquadRosterCard.propTypes = {
  memberStats: PropTypes.shape().isRequired,
  teamTotals: PropTypes.shape().isRequired,
};

export default SquadRosterCard;
