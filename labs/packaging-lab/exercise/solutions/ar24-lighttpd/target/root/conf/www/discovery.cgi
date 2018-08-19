#!/sbin/cgi
<?

include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
include("lib/link.inc");

$iface = "br0";
$vlan_status = cfg_get_vlan_status($cfg,  $iface, "disabled");
if($vlan_status == "enabled"){
    $iface = "br1";
}
if (IsSet($discover) && $discover == "y") {
	if (!IsSet($duration) || $duration < 0) {
		$duration = 500;
	}
	PassThru($cmd_discover + " -i $iface -j -d " + EscapeShellCmd($duration));
	exit;
}

>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
<title><? echo get_title($cfg, dict_translate("Discovery")); ></title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<meta http-equiv="Pragma" content="no-cache">
<link rel="shortcut icon" href="/130904.1419/favicon.ico" >
<link href="/130904.1419/style.css" rel="stylesheet" type="text/css">
<script type="text/javascript" language="javascript" src="jsl10n.cgi"></script>
<script type="text/javascript" language="javascript" src="/130904.1419/js/jquery.js"></script>
<script type="text/javascript" language="javascript" src="/130904.1419/js/jquery.dataTables.js"></script>
<script type="text/javascript" language="javascript">

var mainTable;
var devices = [];
var curr_poll = 0;
var intervals = [[0, 500], [1000, 1000], [20000, 5000]];
var expire_after = 60000;
var ip_col = 6;

</script>
<script type="text/javascript" language="javascript" src="/130904.1419/discovery.js"></script>
</head>

<body class="popup">
<table cellspacing="0" cellpadding="0" align="center" class="popup" style="margin-top: 20px;">
	<tr><th><? echo dict_translate("Device Discovery"); ></th></tr>
	<tr>
		<td class="center">
			<span id="loader"><? echo dict_translate("Scanning, please wait..."); ><br/>
				<img src="/130904.1419/images/ajax-loader.gif" />
			</span>

			<span id="results" class="initial_hide">
			<table id="devices" class="listhead dataTables_head" cellspacing="0" cellpadding="0" align="center">
				<thead>
				<tr>
					<th><? echo dict_translate("MAC Address"); ></th>
					<th><? echo dict_translate("Device Name"); ></th>
					<th><? echo dict_translate("Mode"); ></th>
					<th><? echo dict_translate("SSID"); ></th>
					<th><? echo dict_translate("Product"); ></th>
					<th><? echo dict_translate("Firmware"); ></th>
					<th><? echo dict_translate("IP Address"); ></th>
				</tr>
				</thead>
				<tbody />
			</table>
			</span>
		</td>
	</tr>
	<tr><th>&nbsp;</th></tr>
	<tr id="btn_row" class="initial_hide">
		<td class="change">
			<input type="button" id="scan_btn" onclick="window.location.reload()" value="<? echo dict_translate("Scan"); >" />
		</td>
	</tr>
</table>

</body>
</html>
