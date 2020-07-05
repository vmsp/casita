import './styles.css';

import './logo_custo_justo.png';
import './logo_imovirtual.png';
import './logo_olx.svg';

window.jQuery = window.$ = require('jquery');
require('waypoints/lib/jquery.waypoints');
require('waypoints/lib/shortcuts/infinite');

new Waypoint.Infinite({
  element: $('.infinite-container')[0]
});
