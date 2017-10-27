import reduce from 'lodash/reduce';

const toDict = keys =>
  reduce(
    keys,
    (acc, key) => {
      acc[key] = key;
      return acc;
    },
    {},
  );

const FixtureType = {
  Friendly: 'FRIENDLY',
  League: 'LEAGUE',
  Cup: 'CUP',
};

const HomeAway = {
  Home: 'HOME',
  Away: 'AWAY',
};

const MatchAward = {
  MOM: 'Man of the Match',
  LOM: 'Lemon of the Match',
};

const SwitchableView = {
  SquadRoster: 'squad-roster',
  MatchList: 'match-list',
};

const ViewType = {
  Table: 'Table',
  Timeline: 'Timeline',
  Cards: 'Cards',
};

const MatchItem = toDict([
  'fixtureType',
  'date',
  'opposition',
  'time',
  'venue',
  'result',
  'scorers',
  'awards',
  'report',
]);

module.exports = {
  FixtureType,
  HomeAway,
  MatchAward,
  ViewType,
  SwitchableView,
  MatchItem,
};
