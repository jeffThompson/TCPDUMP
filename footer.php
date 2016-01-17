			</tbody>
			</table>
		</section> <!-- end data -->

		<!-- colophon -->
		<footer>
			<a name="colophon"></a>
			<h1>COLOPHON</h1>
			<p>TCPDUMP is an online performance, documenting every server my computer connects to over a period of one month. Servers are listed with their DNS or IP address, where they occurred in the overall connection count (multiple connections to the same server are ignored), and geolocation and whois lookup. Data can be sorted using the headers at the top of the page.</p>
			
			<ul>
				<li>A project by <a href="http://www.jeffreythompson.org">Jeff Thompson</a></li>
				<li><a href="https://github.com/jeffThompson/TCPDUMP">Code/full data</a> for this project</li>
				<li>CC <a href="http://creativecommons.org/licenses/by-nc-sa/3.0/">BY-NC-SA</a></li>
				<li>2014–15</li>
			</ul>
		</footer> <!-- end footer -->

	</div> <!-- end wrapper -->

	<!-- misc js utilities -->
	<script>
		// commas to count #s
		var counts = document.getElementsByClassName('count');
		for (var i=0; i<counts.length; i++) {
			var val = counts[i].innerHTML;
			while (/(\d+)(\d{3})/.test(val.toString())){
				val = val.toString().replace(/(\d+)(\d{3})/, '$1'+','+'$2');
			}
			counts[i].innerHTML = val;
		}

		// <wbr> after all periods and dashes in URLs
		var urls = document.getElementsByClassName('urlString');
		for (var i=0; i<urls.length; i++) {
			var s = urls[i].innerHTML;
			s = s.replace(/\./g, '.<wbr>');
			s = s.replace(/\-/g, '-<wbr>');
			urls[i].innerHTML = s;
		}
	</script>

</body>
</html>

