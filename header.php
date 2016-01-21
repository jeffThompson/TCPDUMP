<!doctype html>
<html profile="http://www.w3.org/2005/10/profile" itemscope itemtype="http://schema.org/Article">
	<meta charset="UTF-8">

	<title>TCPDUMP</title>
	<meta name="description" content="A month-long performance documenting every unique server from which my computer attempts to download a file.">

	<!--
            _______   _____   __ __   
          /\_______)\/\ __/\ /_/\__/\ 
          \(___  __\/) )__\/ ) ) ) ) )
            / / /   / / /   /_/ /_/ / 
           ( ( (    \ \ \_  \ \ \_\/  
            \ \ \    ) )__/\ )_) )    
            /_/_/    \/___\/ \_\/     

      _____    __    __   __    __    __ __   
     /\ __/\  /\_\  /_/\ /_/\  /\_\  /_/\__/\ 
     ) )  \ \( ( (  ) ) )) ) \/ ( (  ) ) ) ) )
    / / /\ \ \\ \ \/ / //_/ \  / \_\/_/ /_/ / 
    \ \ \/ / / \ \  / / \ \ \\// / /\ \ \_\/  
     ) )__/ /  ( (__) )  )_) )( (_(  )_) )    
     \/___\/    \/__\/   \_\/  \/_/  \_\/     

	TCPDUMP
	Jeff Thompson | 2014-15 | www.jeffreythompson.org

	A month-long performance documenting every unique server from which
	my computer attempts to download a file.

	-->

	<?php
		# settings
		$performing = 			true;				# is the performance in progress?
		$local_domain = 		'jeff-thompson';	# what's the computer's local domain?
		$ignore_local_domains = true;				# ignore connections from the local domain?
		$unique_urls = 			true;				# ignore repeat URLs?
		$refresh_rate = 		5 * 60;				# auto-refresh rate (in seconds) while performing
	?>

	<!-- enable responsiveness on mobile devices-->
	<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1">

	<!-- social sharing links -->
	<meta name="twitter:card" value="A month-long performance documenting every unique server from which my computer attempts to download a file.">
	<meta name="twitter:site" content="@jeffthompson_">
	<meta name="twitter:title" content="TCPDUMP">
	<meta name="twitter:description" content="A month-long performance documenting every unique server from which my computer attempts to download a file.">
	<meta name="twitter:creator" content="@jeffthompson_">
	<meta name="twitter:image:src" content="http://www.jeffreythompson.org/tcpdump/TCPDUMP_Screenshot_Twitter.jpg"> 

	<meta property="og:title" content="TCPDUMP">
	<meta property="og:type" content="article">
	<meta property="og:url" content="http://www.jeffreythompson.org/tcpdump/">
	<meta property="og:image" content="http://www.jeffreythompson.org/tcpdump/TCPDUMP_Screenshot_FB.jpg">
	<meta property="og:description" content="A month-long performance documenting every unique server from which my computer attempts to download a file.">

	<?php 
		if (performing) {
			echo '<!-- auto-refresh while performance is running -->' . PHP_EOL;
			echo '	<meta http-equiv="refresh" content="' . $refresh_rate . '">' . PHP_EOL;
		}
	?>
	
	<!-- styles, Inconsolata, and FontAwesome -->
	<link rel="stylesheet" type="text/css" href="stylesheet.css">
	<link href='https://fonts.googleapis.com/css?family=Inconsolata' rel='stylesheet' type='text/css'>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">

	<!-- analytics -->
	<script>
	  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

	  ga('create', 'UA-11906563-7', 'auto');
	  ga('send', 'pageview');
	</script>
</head>

<body>
	<div id="wrapper">

		<!-- header -->
		<header>
			<section id="logoWrapper">
 				<div class="logoDiv">
 					<pre id="logo" aria-label="TCPDUMP ASCII art logo">
  ________   _____   __ ___  
 /\_______)\/\ __/\ /_/\__/\ 
 \(___  __\/) )__\/ ) ) ) ) )
   / / /   / / /   /_/ /_/ / 
  ( ( (    \ \ \_  \ \ \_\/  
   \ \ \    ) )__/\ )_) )    
   /_/_/    \/___\/ \_\/     </pre>

    			</div>
    			<div class="logoDiv">
    				<pre id="logo" aria-label="TCPDUMP ASCII art logo">
  _____    __    __   __    __    __ __   
 /\ __/\  /\_\  /_/\ /_/\  /\_\  /_/\__/\ 
 ) )  \ \( ( (  ) ) )) ) \/ ( (  ) ) ) ) )
/ / /\ \ \\ \ \/ / //_/ \  / \_\/_/ /_/ / 
\ \ \/ / / \ \  / / \ \ \\// / /\ \ \_\/  
 ) )__/ /  ( (__) )  )_) )( (_(  )_) )    
 \/___\/    \/__\/   \_\/  \/_/  \_\/     </pre>
				</div>
				<div style="clear:both"></div>
			</section> <!-- end logo wrapper -->

			<p id="tagline">A One-Month Performance Documenting Server Connections</p>

			<!-- navigation -->
			<ul class="inlineList">
				<li><a href="#setup">#setup</a></li>
				<li><a href="#data">#data</a></li>
				<li><a href="#colophon">#colophon</a></li>
			</ul>
		</header> <!-- end header -->

		<!-- setup info -->
		<section id="setup">
			<a name="setup"></a>
			<h1>SETUP</h1>
			<table id="setupTable" class="cyan">
				<tr>	<!-- gathering -->
					<td title="Currently gathering URLs?">Status:</td>
					
					<td><?php echo $performing ? 'In progress' : 'Completed'; ?></td>
				</tr>
				
				<tr>	<!-- ftp connection -->
					<td title="Connection established for live updates?">Connecting to FTP server:</td>
					
					<td><?php echo $performing ? 'Connected' : 'Disconnected'; ?></td></tr>
				
				<tr>	<!-- ignore local domain -->
					<td title="Ignore traffic coming from my own computer?">Ignoring local domain:</td>
					
					<td><?php echo $local_domain; ?></td>
				</tr>
				
				<tr>	<!-- combine email urls -->
					<td title="Ignore all of the many combinations of servers used by my email into larger-level blocks?">Combine email URLs:</td>
					
					<td><?php echo $ignore_local_domains ? 'Yes' : 'No'; ?></td>
				</tr>
				
				<tr>	<!-- unique urls -->
					<td title="Only show URLs once (ie: visit again and they don't show up)?">Unique URLs only:</td>
					
					<td><?php echo $unique_urls ? 'Yes' : 'No'; ?></td>
				</tr>
				
				<tr>	<!-- /dev/bp* -->
					<td title="Access to /dev/bp for TCPDUMP program">Setting /dev/bp* permissions:</td>
					
					<td>Set</td>
				</tr>
			</table>
		</section> <!-- end setup -->

		<!-- data -->
		<section id="data">
			<a name="data"></a>
			<h1>GATHERING</h1>

			<div id="loadingData">Loading data &mdash; may take a few moments...</div>

			<table id="servers">
			<thead>
			<tr>
				<th id="serverHeader" class="url" title="Click to sort by server URL"><a href="index.php?sort=url">
				<?php 
					if (isset($_GET['sort']) && $_GET['sort'] == 'url') {
						echo '&uarr;';
					}
				?>
				server</a></th>

				<th id="countHeader" class="count" title="Click to sort by position in overall connection count"><a href="index.php?sort=count">
				<?php 
					if (isset($_GET['sort']) && $_GET['sort'] == 'count') {
						echo '&uarr;';
					}
					else if (isset($_GET['sort']) == false) {
						echo '&darr;';
					}
				?>
				count</a></th>

				<th id="metadataHeader" class="metadata" title="Geolocation and whois lookup">meta</th>
			</tr>
			</thead>

			<tbody>