import Raven from 'raven-js';
import 'process';

Raven.config('https://d1e1fdd048d749cab077ed7ab1b8eeca@sentry.io/247406', {
  release: window.CSHC_VERSION,
}).install();
