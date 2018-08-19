#!/sbin/cgi
<?
SecureVar("cmd*");
SecureVar("lines");
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file);
include("lib/l10n.inc");
include("lib/link.inc");
include("lib/misc.inc");
include("lib/system.inc");

if ($cfg == -1) {
	include("lib/busy.tmpl");
	exit;
}

$wmode_type = get_wmode_type(cfg_get_wmode($cfg, $wlan_iface));
$netmode_cfg = cfg_get_def($cfg, "netmode", "airfiber");
if (strlen($netmode)==0) {
	$netmode = $netmode_cfg;
}
$country = cfg_get_country($cfg, $wlan_iface, $country);

if ($REQUEST_METHOD == "POST") {
	cfg_set($cfg, "airview.tcp_port", $av_tcp_port);
	cfg_update_dmz_mgmt($cfg);
	cfg_save($cfg, $cfg_file);
	cfg_set_modified($cfg_file);
	$message = dict_translate("Configuration saved");
}

$av_tcp_port = cfg_get_def($cfg, "airview.tcp_port", $airview_tcp_port);

include("lib/ubnt.tmpl");
>
