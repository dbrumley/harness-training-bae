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

  $netmode = cfg_get_def($cfg, "netmode", "airfiber");
  $curr_iface = $wlan_iface;
  $curr_ifidx = get_wlan_index($curr_iface); 
  init_board_inc($curr_iface);
  $oldwmode = cfg_get_wmode($cfg, $curr_iface);
  $radio_chains = $radio["chains"];
  if (strlen($oldwmode) == 0) {
	  $oldwmode = "sta";
  }
  if (strlen($wmode) == 0) {
	  $wmode = $oldwmode;
  }
	if (strlen($country) == 0) {
		if (strlen($old_country) == 0) {
			$country = cfg_get_country($cfg, $curr_iface, $country);
			$old_country = $country;
		} else {
			$country = $old_country;
		}
	}

	if ($REQUEST_METHOD == "POST")
	{
		if ($cc != "changed")
        { 
			/* common variables */
			set_wmode_af($cfg, $wmode, $tx_chan_freq, $rx_chan_freq, $af_duplex);
			set_essid($cfg, $curr_ifidx, $essid);
			set_country($cfg, $curr_ifidx, $country, $radio["subsystemid"]);
			update_power_limits($cfg, $curr_ifidx, $country);
			set_txpower($cfg, $curr_ifidx, $txpower);
			set_rate_af($cfg, $curr_ifidx, $rate, $rate_auto);
			cfg_set($cfg, "radio.$curr_ifidx.rxgain", $rxgain);
			set_af_key($cfg, $curr_ifidx, $af_key, $af_key_type);
			cfg_save($cfg, $cfg_file);
			cfg_set_modified($cfg_file);
			$message = dict_translate("Configuration saved");
		}
		else
		{
			$essid = htmlspecialchars($essid);
			$af_key = htmlspecialchars($af_key);
			update_power_limits($cfg, $curr_ifidx, $country);
			$txpower = adjust_txpower($cfg, $curr_ifidx, $txpower);
			include("lib/link.tmpl");
			exit;
    	}
    }

  /* retrieve common variables */
  $essid = cfg_get_essid($cfg, $curr_ifidx, $essid);
  $country = cfg_get_country($cfg, $curr_iface, $country);
  $old_country = $country;
  update_power_limits($cfg, $curr_ifidx, $country);
  $txpower = cfg_get_adjusted_txpower($cfg, $curr_ifidx, $txpower);
  $rate_auto = cfg_get_def($cfg, "radio.$curr_ifidx.rate.auto", "enabled");
  $rxgain = cfg_get_def($cfg, "radio.$curr_ifidx.rxgain", "high");
  $af_duplex = cfg_get_def($cfg, "radio.$curr_ifidx.duplex", "half");
  $rate = cfg_get_rate_af($cfg, $curr_iface, $rate);
  $af_key = cfg_get_key_af($cfg, $curr_ifidx);
  $af_key_type = 1;
  if (strlen($af_key) > 2 && "s:" == substr($af_key, 0, 2)) {
     $af_key_type = 2;
     $af_key = substr($af_key, 2, strlen($af_key) - 2);
  }
  $tx_chan_freq = cfg_get_def($cfg, "radio.$curr_ifidx.tx_freq", $tx_chan_freq);
  $rx_chan_freq = cfg_get_def($cfg, "radio.$curr_ifidx.rx_freq", $rx_chan_freq);
  $af_duplex    = cfg_get_def($cfg, "radio.$curr_ifidx.duplex",  $af_duplex);
  $essid = htmlspecialchars($essid);
  $af_key = htmlspecialchars($af_key);
  include("lib/link.tmpl");
>
