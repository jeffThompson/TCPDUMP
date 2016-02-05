<?php include('header.php'); ?>

<?php

	# settings
	$google_zoom = 16;		# 2 = continent, ~22 = max zoom

	# load csv, sort
	$rows = array();
	$by = array();

	# load file based on sorting option
	# by url
	if (isset($_GET['sort']) && $_GET['sort'] == 'url') {
		$handle = fopen('AllServers_URL.csv', 'r');
	} 

	# by count: oldest to newest
	else if (isset($_GET['sort']) && $_GET['sort'] == 'count') {
		$handle = fopen('AllServers_ASC.csv', 'r');
	} 

	# default: count, newest to oldest
	else {
		$handle = fopen('AllServers_DESC.csv', 'r');
	}

	$row = fgetcsv($handle, 1024, ',');							// skip header
	while (($row = fgetcsv($handle, 1024, ',')) !== FALSE) {
	    $rows[] = $row;
	}
	fclose($handle);

	# display
	foreach($rows as $row) {
		$count = 		number_format($row[0]);

		$url = 			$row[3];
		$subdomain = 	$row[4];
		$domain = 		$row[5];
		$tld = 			$row[6];
		$rest = 		$row[7];

		$country = 		$row[9];
		$city = 		$row[11];
		$lat = 			$row[13];
		$lon = 			$row[14];

		echo '			<tr>';

		# url
		echo '<td class="url">';
		echo '<p><a class="urlString" href="http://' . $url . '" target="_blank">';

		# subdomain
		if ($subdomain != '') {
			echo '<span class="subdomain">' . $subdomain . '.' . '<wbr></span>';
		}

		# domain
		echo '<span class="domain">' . $domain . '</span>';
		
		# tld
		if ($tld != '') {
			echo '<span class="domain">' . '.<wbr>' . $tld . '</span>';
		}

		# rest
		if ($rest != '') {
			echo '<span class="subdomain">' . '<wbr>.' . $rest . '</span>';
		}

		# end url
		echo '</a></p></td>';

		# count
		echo '<td class="count">' . $count . '</td>';

		# metadata
		echo '<td class="metadata"><p>';
		
		# geolocation
		if ($lat != '0' && $lon != '0' && $lat != '' && $lon != '') {
			$loc_txt = '';

			# format location
			# no country? show lat/lon
			if ($country == '') {
				$loc_txt = $lat . '&deg;';
				if ($lat >= 45) {
					$loc_txt .= 'N';
				} else {
					$loc_txt .= 'S';
				}
				$loc_txt .= ', ' . $lon . '&deg;';
				if ($lon >= 0) {
					$loc_txt .= 'E';
				} else {
					$loc_txt .= 'W';
				}
			} else {
				$loc_txt = $country;
				if ($city != '') {
					$loc_txt = $city . ', ' . $loc_txt;
				}
			}

			# link to map
			echo '<a href="http://www.google.com/maps/preview/@' . $lat . ',' . $lon . ',' . $google_zoom . 'z" target="_blank">';
			echo '<span class="mapMarker"><i class="fa fa-map-marker"></i></span></a>';
		} else {
			echo '<span class="mapMarkerNoLocation"><i class="fa fa-map-marker"></i></span>';
		}
		echo '&nbsp;&nbsp;';

		# whois
		# IP addresses can't be looked up with ICANN :(
		if (filter_var($url, FILTER_VALIDATE_IP)) {
			$whois_url = 'http://whois.urih.com/record/' . $url;
		} else {
			$whois_url = 'https://whois.icann.org/en/lookup?name=' . $url;
		}
		echo '<a href="' . $whois_url . '" target="_blank">';
		echo '<span class="whois"><i class="fa fa-info"></i></span></a>';
		
		# end location/whois and row
		echo '</td>' . '</tr>' . PHP_EOL;
	}
?>

<?php include('footer.php'); ?>