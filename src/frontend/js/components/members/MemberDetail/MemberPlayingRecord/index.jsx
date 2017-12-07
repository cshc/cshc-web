import { addUrlProps } from 'react-url-query';
import MemberPlayingRecord, { urlPropsQueryConfig } from './MemberPlayingRecord';

export default addUrlProps({ urlPropsQueryConfig })(MemberPlayingRecord);
