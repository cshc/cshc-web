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
  VenueList: 'venue-list',
};

const ViewType = toDict(['Table', 'Timeline', 'Cards', 'List', 'Map']);

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

const FilterName = {
  HomeGround: 'onlyHomeGrounds',
  Season: 'season',
  TextSearch: 'textSearch',
  VenueTeam: 'venueTeam',
  VenueDivision: 'venueDivision',
};

module.exports = {
  FixtureType,
  HomeAway,
  MatchAward,
  ViewType,
  SwitchableView,
  MatchItem,
  FilterName,
};
