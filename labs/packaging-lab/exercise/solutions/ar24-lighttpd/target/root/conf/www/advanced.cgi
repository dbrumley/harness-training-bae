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

  $netmode_cfg = cfg_get_def($cfg, "netmode", "airfiber");
  if (strlen($netmode)==0) {
    $netmode = $netmode_cfg;
  }

  $ccode = cfg_get_country($cfg, $wlan_iface, "");
  if ($REQUEST_METHOD == "POST") {
    if (strlen($error_msg) == 0) {
        if(strlen($gps_sync) == 0) {
          $gps_sync = "disabled";
        }
        cfg_set($cfg, "radio.1.gps_sync", $gps_sync);
        if (isset($eth0_speed)) {
          set_eth_speed($cfg, "eth0", $eth0_speed);
        }
        if (isset($af0_speed)) {
          set_eth_speed_af_data($cfg, "af0", $af0_speed);
        }
        if(strlen($flowcntl) == 0) {
          $flowcntl = "disabled";
        }
        cfg_set($cfg, "afnetconf.1.flowcntl", $flowcntl);
    }
    cfg_save($cfg, $cfg_file);
    cfg_set_modified($cfg_file);
    $message = dict_translate("Configuration saved");
  }

  $eth0_speed = get_eth_speed($cfg, "eth0");
  $af0_speed = get_eth_speed_af_data($cfg, "af0");
  $gps_sync = cfg_get_def($cfg, "radio.1.gps_sync", "disabled");
  $flowcntl = cfg_get_def($cfg, "afnetconf.1.flowcntl", "disabled");

  include("lib/advanced.tmpl");
>
