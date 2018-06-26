import React from 'react';
import PropTypes from 'prop-types';
import { Pie } from 'react-chartjs-2';
import Member from 'models/member';
import ProgressBar from 'components/common/ProgressBar';
import MemberAvatar from 'components/members/MemberAvatar';
import AwardCount from 'components/awards/AwardCount';
import Urls from 'util/urls';
import styles from './style.scss';

/**
 * 'Card' representation of a club member, with profile pic, stats about games played, goals scored and
 * win/draw/loss record and a link to their profile.
 */
const SquadRosterCard = ({ memberStats, teamTotals }) => {
  const playedPercentage = 100 * (memberStats.played / teamTotals.played);
  const goalsPercentage = 100 * (memberStats.goals / teamTotals.goals);
  const wldData = [];
  const wldLabels = [];
  const wldBgColors = [];
  const wldHoverColors = [];
  if (memberStats.won > 0) {
    wldLabels.push('Won');
    wldData.push(memberStats.won);
    wldBgColors.push('#00ff00');
    wldHoverColors.push('#00ff00');
  }
  if (memberStats.drawn > 0) {
    wldLabels.push('Drawn');
    wldData.push(memberStats.drawn);
    wldBgColors.push('lightgrey');
    wldHoverColors.push('lightgrey');
  }
  if (memberStats.lost > 0) {
    wldLabels.push('Lost');
    wldData.push(memberStats.lost);
    wldBgColors.push('red');
    wldHoverColors.push('red');
  }
  const wld = {
    labels: wldLabels,
    datasets: [
      {
        data: wldData,
        backgroundColor: wldBgColors,
        hoverBackgroundColor: wldHoverColors,
      },
    ],
  };
  const wldOptions = {
    responsive: true,
    legend: {
      display: false,
      layout: {
        padding: 0,
      },
    },
  };
  const mom = <AwardCount iconClass="star" awardCount={memberStats.mom} />;
  const lom = <AwardCount iconClass="lemon" awardCount={memberStats.lom} />;
  return (
    <div className="col-md-6 col-lg-3 g-mb-30">
      <article className="g-bg-white">
        <figure className={styles.imageContainer}>
          <MemberAvatar member={memberStats.member} rounded={false} />
          {memberStats.mom > 0 && <div className={styles.mom}>{mom}</div>}
          {memberStats.lom > 0 && <div className={styles.lom}>{lom}</div>}
        </figure>
        <div className="u-shadow-v24 g-pa-25">
          <a href={Urls.member_detail(memberStats.member.id)} title="View Profile">
            <h3 className="h5 g-mb-5 text-center">
              {Member.fullName(memberStats.member)}
              {memberStats.isCaptain && ' (C)'}
              {memberStats.isViceCaptain && ' (VC)'}
            </h3>
          </a>
          <p className="text-center g-mb-5">
            &nbsp;{memberStats.member.prefPosition !== 'Not known' &&
              memberStats.member.prefPosition}&nbsp;
          </p>
          <div className="d-flex">
            <div className={styles.progress}>
              <ProgressBar
                label="Played"
                value={memberStats.played}
                progressValue={playedPercentage}
              />
              <ProgressBar
                label="Goals"
                value={memberStats.goals}
                progressValue={goalsPercentage}
                color="blue"
              />
            </div>
            <div className={styles.pie}>
              <Pie data={wld} options={wldOptions} />
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
