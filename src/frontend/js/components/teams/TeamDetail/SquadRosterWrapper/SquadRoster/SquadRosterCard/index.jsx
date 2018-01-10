import React from 'react';
import PropTypes from 'prop-types';
import { VictoryPie } from 'victory';
import Member from 'models/member';
import ProgressBar from 'components/common/ProgressBar';
import IconList from 'components/common/IconList';
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
  const wldColors = [];
  if (memberStats.won > 0) {
    wldData.push({ x: 'W', y: memberStats.won });
    wldColors.push('#00ff00');
  }
  if (memberStats.drawn > 0) {
    wldData.push({ x: 'D', y: memberStats.drawn });
    wldColors.push('lightgrey');
  }
  if (memberStats.lost > 0) {
    wldData.push({ x: 'L', y: memberStats.lost });
    wldColors.push('red');
  }

  const mom = <AwardCount iconClass="star-o" awardCount={memberStats.mom} />;
  const lom = <AwardCount iconClass="lemon-o" awardCount={memberStats.lom} />;
  const captain = memberStats.isCaptain || memberStats.isViceCaptain;
  return (
    <div className="col-md-6 col-lg-3 g-mb-30">
      <article className="g-bg-white">
        <figure className={styles.imageContainer}>
          <MemberAvatar member={memberStats.member} rounded={false} />
          {captain && (
            <div className={styles.captain}>
              {mom}
              <div>{memberStats.isCaptain ? 'Captain' : 'Vice-Captain'}</div>
              {lom}
            </div>
          )}
          {!captain && memberStats.mom > 0 && <div className={styles.mom}>{mom}</div>}
          {!captain && memberStats.lom > 0 && <div className={styles.lom}>{lom}</div>}
        </figure>
        <div className="u-shadow-v24 g-pa-25">
          <a href={Urls.member_detail(memberStats.member.id)} title="View Profile">
            <h3 className="h5 g-mb-5 text-center">{Member.fullName(memberStats.member)}</h3>
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
              <VictoryPie
                colorScale={wldColors}
                data={wldData}
                height={150}
                width={150}
                padding={10}
                labelRadius={28}
                style={{ labels: { fontSize: 25, fontWeight: 'bold' } }}
                labels={d => d.x}
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
