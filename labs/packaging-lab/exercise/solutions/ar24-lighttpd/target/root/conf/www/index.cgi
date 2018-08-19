#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file_bak);
include("lib/l10n.inc");
include("lib/link.inc");
include("lib/system.inc");
include("lib/misc.inc");

$chain_names = get_chain_names($cfg);
$chain1_name = $chain_names[0];
$chain2_name = $chain_names[1];
$wmode    = cfg_get_wmode($cfg, $wlan_iface);
$security = cfg_get_security($cfg, $wlan_iface, $security, $wmode);
>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
	"http://www.w3.org/TR/html4/DTD/loose.dtd">
<html>
<head>
<title><? echo get_title($cfg, dict_translate("Main")); ></title>
<meta http-equiv="X-UA-Compatible" content="IE=EmulateIE7" >
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta name="SKYPE_TOOLBAR" content="SKYPE_TOOLBAR_PARSER_COMPATIBLE" />
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<meta http-equiv="Cache-Control" content="no-cache">
<link rel="shortcut icon" href="/130904.1419/favicon.ico" >
<link href="/130904.1419/style.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript" src="/130904.1419/signal.js"></script>
<script type="text/javascript" language="javascript" src="/130904.1419/util.js"></script>
<script type="text/javascript" language="javascript" src="/130904.1419/index.js"></script>
<script type="text/javascript" language="javascript" src="/130904.1419/js/jquery.js"></script>
<script type="text/javascript" language="javascript" src="/130904.1419/js/jquery.cookie.js"></script>
<!--[if lte IE 8]><script type="text/javascript" src="/130904.1419/js/excanvas.js"></script><![endif]-->
<script type="text/javascript" src="/130904.1419/js/jquery.flot.js"></script>
<script type="text/javascript" language="javascript" src="/130904.1419/common.js"></script>
<? flush(); >
<script type="text/javascript" language="javascript">
//<!--
var status_reload_interval = 0;
var global = {
	'wlan_iface': "<? echo $wlan_iface;>",
	'chain_count': "<? echo $radio1_chains; >",
	'security': "<? echo $security; >",
	'has_gps' : <? if ($feature_gps == 1) { echo "true"; } else { echo "false"; } >,
	'_': '_'
};
var l10n_lang = {
	'Access Point WDS': "<? echo dict_translate("Access Point WDS");>",
	'Access Point': "<? echo dict_translate("Access Point");>",
	'Station WDS': "<? echo dict_translate("Station WDS");>",
	'Station': "<? echo dict_translate("Station");>",
	'Spectral Analyzer': "<? echo dict_translate("Spectral Analyzer");>",
	'Active': "<? echo dict_translate("Active");>",
	'clients': "<? echo dict_translate("clients");>",
	'Idle for': "<? echo dict_translate("Idle for");>",
	'Back to': "<? echo dict_translate("Back to");>",
	'Switching back to': "<? echo dict_translate("Switching back to");>",
	'in': "<? echo dict_translate("in");>",
	's': "<? echo dict_translate("s");>",

	'Bridge': "<? echo dict_translate("Bridge");>",
	'Router': "<? echo dict_translate("Router");>",
	'SOHO Router': "<? echo dict_translate("SOHO Router");>",
	'3G Router': "<? echo dict_translate("3G Router");>",

	'Auto': "<? echo dict_translate("Auto");>",
	'Lower': "<? echo dict_translate("Lower");>",
	'Upper': "<? echo dict_translate("Upper");>",
	'Enabled': "<? echo dict_translate("Enabled");>",
	'Peers': "<? echo dict_translate("Peers");>",
	'Disabled': "<? echo dict_translate("Disabled");>",
	'Connected': "<? echo dict_translate("Connected");>",
	'Not Connected': "<? echo dict_translate("Not Connected");>",
	'Not Associated': "<? echo dict_translate("Not Associated");>",

	'none': '<? echo dict_translate("none"); >',
	'None': '<? echo dict_translate("None"); >',

	'day': '<? echo dict_translate("day"); >',
	'days': '<? echo dict_translate("days"); >',
	/* cable status */
	'Plugged': '<? echo dict_translate("Plugged"); >',
	'Unplugged': '<? echo dict_translate("Unplugged"); >',
	'Full': '<? echo dict_translate("Full"); >',
	'Half': '<? echo dict_translate("Half"); >',
	/* antennas */
	'Unknown': "<? echo dict_translate("Unknown"); >",
	'Main': "<? echo dict_translate("Main"); >",
	'Not detected': "<? echo dict_translate("Not detected"); >",

	/* airmax priority */
	'High': "<? echo dict_translate("High");>",
	'Medium': "<? echo dict_translate("Medium");>",
	'Low': "<? echo dict_translate("Low");>",

	/* airfiber stuff */
	'airFiber' : "<? echo dict_translate("airFiber");>",
	'AES-128' : "<? echo dict_translate("AES-128");>",
	'slave': "<? echo dict_translate("Slave");>",
	'master': "<? echo dict_translate("Master");>",
	'reset': "<? echo dict_translate("Reset");>",
	'duplex-full': '<? echo dict_translate("Full Duplex"); >',
	'duplex-half': '<? echo dict_translate("Half Duplex"); >',
	'regdom-fcc': '<? echo dict_translate("FCC / IC"); >',
	'regdom-etsi': '<? echo dict_translate("ETSI"); >',
	'regdom-acma': '<? echo dict_translate("ACMA"); >',
	'regdom-none': '<? echo dict_translate("Other"); >',
	'speed-0x': '<? echo dict_translate("1/4x (QPSK SISO)"); >',
	'speed-1x': '<? echo dict_translate("1x (QPSK SISO)"); >',
	'speed-2x': '<? echo dict_translate("2x (QPSK MIMO)"); >',
	'speed-4x': '<? echo dict_translate("4x (16QAM MIMO)"); >',
	'speed-6x': '<? echo dict_translate("6x (64QAM MIMO)"); >',
	'speed-8x': '<? echo dict_translate("8x (256QAM MIMO)"); >',
	'speed-n/a': '<? echo dict_translate("Unknown"); >',
	'linkstate-reset': '<? echo dict_translate("RF Off"); >',
	'linkstate-idle': '<? echo dict_translate("RF Off"); >',
	'linkstate-syncing': '<? echo dict_translate("Syncing"); >',
	'linkstate-beaconing': '<? echo dict_translate("Beaconing"); >',
	'linkstate-registering': '<? echo dict_translate("Registering"); >',
	'linkstate-enabling': '<? echo dict_translate("Enabling"); >',
	'linkstate-listening': '<? echo dict_translate("Listening"); >',
	'linkstate-calibrating': '<? echo dict_translate("RF Off"); >',
	'linkstate-operational': '<? echo dict_translate("Operational"); >',
	'cpstat-Unplugged': '<? echo dict_translate("Unplugged"); >',
	'cpstat-Unknown': '<? echo dict_translate("Unknown"); >',
	'cpstat-10Mbps-Half': '<? echo dict_translate("10Mbps-Half"); >',
	'cpstat-10Mbps-Full': '<? echo dict_translate("10Mbps-Full"); >',
	'cpstat-100Mbps-Half': '<? echo dict_translate("100Mbps-Half"); >',
	'cpstat-100Mbps-Full': '<? echo dict_translate("100Mbps-Full"); >',
	'dpstat-nolink': '<? echo dict_translate("No Link"); >',
	'dpstat-10Mbps-Half': '<? echo dict_translate("10Mbps-Half"); >',
	'dpstat-10Mbps-Full': '<? echo dict_translate("10Mbps-Full"); >',
	'dpstat-100Mbps-Half': '<? echo dict_translate("100Mbps-Half"); >',
	'dpstat-100Mbps-Full': '<? echo dict_translate("100Mbps-Full"); >',
	'dpstat-1000Mbps-Full': '<? echo dict_translate("1000Mbps-Full"); >',
	'security-AES-128':  '<? echo dict_translate("AES-128"); >',
	'Overload': '<? echo dict_translate("Overload"); >',
	'dBm': '<? echo dict_translate("dBm"); >',

	'_': '_' /* end marker */
};

function l10n_get(w) {
	var t = l10n_lang[w];
	if (t)
		return t;
	if (window.console && window.console.log)
		window.console.log('L10N ERROR: untranslated "' + w + '"');
	return w;
}

<? gen_update_check($cfg); >

function init() {
	$('#noscript').remove();
	$('#extrainfo span').addClass('initial_hide');
	$('#signalinfo').hide();
	reloadStatus();

	$('#extrainfo a').click( function(){
			$('#extrainfo a').removeClass('underline');
			$(this).addClass('underline');
			refreshContent($(this).attr('href'));
			return false;
	});

	$('#extrainfo span.all').removeClass('initial_hide');
	$('#extrainfo a:first').trigger('click');

	fwUpdateCheck(false, fw_check);
}

$(document).ready(init);
//-->
</script>
</head>
<? flush(); >
<body>
<table class="maintable" cellpadding="0" align="center" cellspacing="0"><?
$top_tab = "main"; include("lib/head.tmpl");
>  <tr>
<td colspan="2" class="centr">
<noscript id="noscript"><? echo dict_translate("warn_no_script|You have disabled JavaScript in your browser, but the functionality of this page depends on it. Please, enable JavaScript and refresh this page."); >
</noscript>

<br>
	<table border="0" cellpadding="0" cellspacing="0" class="linktable">
	  <tr><th colspan="2"><? echo dict_translate("Status"); ></th></tr>
	  <tr><td valign="top" style="width: 45%">
		<div class="fieldset" id="general_info">
		  <div id="hostinfo" class="row">
			<span class="label"><? echo dict_translate("Device Name:"); ></span>
			<span class="value" id="hostname">&nbsp;</span>
		  </div>
			<div id="linkmodeinfo" class="row">
			<span class="label"><? echo dict_translate("Operating Mode:"); ></span>
			<span class="value" id="linkmode">&nbsp;</span>
			</div>
			<div id="linkstateinfo" class="row">
			<span class="label"><? echo dict_translate("RF Link Status:"); ></span>
			<span class="value" id="linkstate">&nbsp;</span>
			</div>
			<div id="linknameinfo" class="row">
			<span class="label" id="linkname_label"><? echo dict_translate("Link Name:"); ></span>
			<span class="value" id="linkname">&nbsp;</span>
			</div>
<? if ($feature_airview == 1) { >
		  <div id="astatusinfo" class="row">
			<span class="label"><? echo dict_translate("airView Status:"); ></span>
			<span class="value" id="astatus">&nbsp;</span>
		  </div>
<? } >
		  <div id="securityinfo" class="row">
			<span class="label"><? echo dict_translate("Security:"); ></span>
			<span class="value" id="security">&nbsp;</span>
		  </div>
		  <div id="fwversioninfo" class="row">
			<span class="label"><? echo dict_translate("Version:"); ></span>
			<span class="value" id="fwversion">&nbsp;</span>
		  </div>
		  <div id="uptimeinfo" class="row">
			<span class="label"><? echo dict_translate("Uptime:"); ></span>
			<span class="value" id="uptime">&nbsp;</span>
		  </div>
		  <div id="dateinfo" class="row">
			<span class="label"><? echo dict_translate("Date:"); ></span>
			<span class="value" id="date">&nbsp;</span>
		  </div>
		</div>

		<div class="fieldset" id="radioinfo">
		  <div id="duplexinfo" class="row">
			<span class="label"><? echo dict_translate("Duplex:"); ></span>
			<span class="value" id="af_duplex">&nbsp;</span>
		  </div>
		  <div id="txfreqinfo" class="row">
			<span class="label"><? echo dict_translate("TX Frequency:"); ></span>
			<span class="value" id="tx_frequency">&nbsp;</span>
		  </div>
		  <div id="rxfreqinfo" class="row">
			<span class="label"><? echo dict_translate("RX Frequency:"); ></span>
			<span class="value" id="rx_frequency">&nbsp;</span>
		  </div>
		  <div id="regdomaininfo" class="row">
			<span class="label"><? echo dict_translate("Regulatory Domain"); ></span>
			<span class="value" id="regdomain">&nbsp;</span>
		  </div>
		  <div id="dactempinfo" class="row">
			<span class="label"><? echo dict_translate("Internal Temperature"); >:</span>
			<span class="value">
			<span id="dactemp0">-</span><span>&nbsp;/&nbsp;</span><span id="dactemp1">-</span>
			<span>&nbsp;</span>
			</span>
		  </div>
		<? if(0) { >
		  <div id="antennainfo" class="row">
			<span class="label"><? echo dict_translate("Antenna:"); ></span>
			<span class="value" id="antenna">&nbsp;</span>
		  </div>
		<? } >
		</div>
		<div class="fieldset" id="ifinfo" />
	  </td>
	  <td valign="top">
		<div class="fieldset" id="cinfo">
		  <div id="signal0_row" class="row">
			<span class="label"><? echo $chain1_name; >&nbsp;<? echo dict_translate("Signal Strength:"); ></span>
			<span class="value">
				<span id="signal0_bar_border" class="percentborder"><div id="signal0_bar" class="mainbar">&nbsp;</div></span><span id="signal0_spacer">&nbsp;</span><span id="signal0_value"></span>
			</span>
		  </div>
		  <div id="signal1_row" class="row">
			<span class="label"><? echo $chain2_name; >&nbsp;<? echo dict_translate("Signal Strength:"); ></span>
			<span class="value">
				<span id="signal1_bar_border" class="percentborder"><div id="signal1_bar" class="mainbar">&nbsp;</div></span><span id="signal1_spacer">&nbsp;</span><span id="signal1_value"></span>
			</span>
		  </div>
		  <div id="remote_signal0_row" class="row">
			<span class="label"><? echo dict_translate("Remote"); >&nbsp;<? echo $chain1_name; >&nbsp;<? echo dict_translate("Signal Strength:"); ></span>
			<span class="value">
				<span id="remote_signal0_bar_border" class="percentborder"><div id="remote_signal0_bar" class="mainbar">&nbsp;</div></span><span id="remote_signal0_spacer">&nbsp;</span><span id="remote_signal0_value"></span>
			</span>
		  </div>
		  <div id="remote_signal1_row" class="row">
			<span class="label"><? echo dict_translate("Remote"); >&nbsp;<? echo $chain2_name; >&nbsp;<? echo dict_translate("Signal Strength:"); ></span>
			<span class="value">
				<span id="remote_signal1_bar_border" class="percentborder"><div id="remote_signal1_bar" class="mainbar">&nbsp;</div></span><span id="remote_signal1_spacer">&nbsp;</span><span id="remote_signal1_value"></span>
			</span>
		  </div>
		  <div id="speedinfo" class="row">
			<span class="label"><? echo dict_translate("Current Modulation Rate:") ></span>
			<span class="value" id="speed">&nbsp;</span>
		  </div>
		  <div id="remote_speedinfo" class="row">
			<span class="label"><? echo dict_translate("Remote Modulation Rate:") ></span>
			<span class="value" id="remote_speed">&nbsp;</span>
		  </div>
		  <div id="capacityinfo" class="row">
			<span class="label"><? echo dict_translate("TX Capacity:") ></span>
			<span class="value" id="txcapacity">&nbsp;</span>
		  </div>
		  <div id="capacityinfo" class="row">
			<span class="label"><? echo dict_translate("RX Capacity:") ></span>
			<span class="value" id="rxcapacity">&nbsp;</span>
		  </div>
          <div id="txpowerinfo" class="row">
            <span class="label"><? echo dict_translate("TX Power:"); ></span>
            <span class="value" id="txpowerdisp">&nbsp;</span>
          </div>
          <div id="remote_txpower_row" class="row initial_hide">
            <span class="label"><? echo dict_translate("Remote TX Power:"); ></span>
            <span class="value" id="remote_txpower">&nbsp;</span>
          </div>          
          <div id="rxgaininfo" class="row">
            <span class="label"><? echo dict_translate("RX Gain:"); ></span>
            <span class="value" id="rxgaindisp">&nbsp;</span>
          </div>
          <div id="remote_rxgain_row" class="row initial_hide">
            <span class="label"><? echo dict_translate("Remote RX Gain:"); ></span>
            <span class="value" id="remote_rxgain">&nbsp;</span>
          </div>		  
		  <div id="distanceinfo" class="row">
			<span class="label"><? echo dict_translate("Distance:"); ></span>
			<span class="value" id="distance">&nbsp;</span>
		  </div>
<? if ($feature_ccq) { >
		  <div id="ccqinfo" class="row">
			<span class="label"><? echo dict_translate("Transmit CCQ:"); ></span>
			<span class="value">
			  <span id="ccq">&nbsp;</span>
			  <span>&nbsp;</span>
			</span>
		  </div>
<? } >
		<div class="fieldset"/>
		<div class="fieldset"/>
		<div class="fieldset initial_hide" id="airsyncinfo">
			<span class="label"><? echo dict_translate("airSync:"); ></span>
			<span class="value" id="airsyncstatus">&nbsp;</span>
		</div>
		<div class="fieldset"/>
		<div class="fieldset">
			<div class="row initial_hide">
				<span class="label"><? echo dict_translate("GPS Receiver:"); ></span>
				<span class="value" id="gps_status">&nbsp;</span>
			</div>
			<div class="row gpsinfo">
				<span class="label"><? echo dict_translate("GPS Signal Quality:"); ></span>
				<span class="value">
					<span class="percentborder"><div id="gpsbar" class="mainbar">&nbsp;</div></span>
					<span >&nbsp;</span>
					<span id="gps_qual">&nbsp;</span>
					<span >&nbsp;%</span>
				</span>
			</div>
			<div class="row gpsinfo">
				<span class="label"><? echo dict_translate("Latitude / Longitude:"); ></span>
				<span class="value" id="gps_coord">&nbsp;</span>
			</div>
			<div class="row gpsinfo">
				<span class="label"><? echo dict_translate("Altitude:"); ></span>
				<span class="value" id="gps_alt">&nbsp;</span>
			</div>
			<div class="row gpsinfo">
				<span class="label"><? echo dict_translate("Synchronization:"); ></span>
				<span class="value" id="gps_sync">&nbsp;</span>
			</div>
		</div>
	   </td>
	</tr>
	<tr><td colspan="2">&nbsp;</td></tr>
	<tr><th colspan="2"><? echo dict_translate("Monitor"); ></th></tr>
	<tr>
	<td colspan="2" id="extrainfo">
	<span 
	id="performancegraph" class="all"><a href="performance.cgi" target="extraFrame"><? echo dict_translate("Performance"); ></a> | </span><span
	id="throughputgraph" class="disabledmonitor"><a href="throughput.cgi" target="extraFrame"><? echo dict_translate("Throughput"); ></a> | </span><span
	id="capacitygraph" class="disabledmonitor"><a href="capacity.cgi" target="extraFrame"><? echo dict_translate("Capacity"); ></a> | </span><span
	id="ifaces" class="disabledmonitor"><a href="ifaces.cgi" target="extraFrame"><? echo dict_translate("Interfaces"); ></a> | </span><span
	id="ppp_info" class="disabledmonitor"><a href="pppinfo.cgi" target="extraFrame"><? echo dict_translate("PPPoE Information"); ></a> | </span><span
	id="dhcpc_info" class="disabledmonitor"><a href="dhcpc.cgi" target="extraFrame"><? echo dict_translate("DHCP Client"); ></a> | </span><span
	id="arp" class="disabledmonitor"><a href="arp.cgi" target="extraFrame"><? echo dict_translate("ARP Table"); ></a> | </span><span
	id="brmacs" class="disabledmonitor"><a href="brmacs.cgi" target="extraFrame"><? echo dict_translate("Bridge Table"); ></a> | </span><span
	id="sroutes" class="disabledmonitor"><a href="sroutes.cgi" target="extraFrame"><? echo dict_translate("Routes"); ></a> | </span><span
	id="fwall" class="disabledmonitor"><a href="fw.cgi?netmode=<? echo $netmode;>" id="a_fw" target="extraFrame"><? echo dict_translate("Firewall"); ></a> | </span><span
	id="pfw" class="disabledmonitor"><a href="pfw.cgi" target="extraFrame"><? echo dict_translate("Port Forward"); ></a> | </span><span
	id="dhcp_leases" class="disabledmonitor"><a href="leases.cgi" target="extraFrame"><? echo dict_translate("DHCP Leases"); ></a> | </span><span
	id="satelites" class="satelites"><a href="gpsstats.cgi" target="extraFrame"><? echo dict_translate("GPS Details"); ></a> | </span><span
	id="log" class="all"><a href="log.cgi" target="extraFrame"><? echo dict_translate("Log"); ></a></span>
	</td>
	</tr>
	<tr>
	<td colspan="2" align="center">
	<div id="extraFrame">
	</div>
	</td>
	</tr>
	</table>
	</td>
	</tr>
	<tr>
	  <td colspan="2">
		<table cellpadding="0" align="center" cellspacing="0" width="100%">
			<tr>
				<td height="10" class="footlogo"><img src="/glogo.cgi" border="0"></td>
				<td height="10" class="foottext"><? echo dict_translate($oem_copyright); ></td>
			</tr>
			</table>
	  </td>
	</tr>
</table>
</body>
</html>
