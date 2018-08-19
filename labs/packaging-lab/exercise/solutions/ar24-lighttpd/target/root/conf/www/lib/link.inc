<?
Function get_iface_index $cfg, $iface
(
	$index = 0; /* not found */
	$idx = 1;
	$devname = "dummy";

	while ($index == 0 && strlen($devname) != 0 && $idx <= 32) {
		$devname = cfg_get_def($cfg, "netconf.$idx.devname", "");
		if ($devname == $iface) {
			$index = $idx;
		}
		$idx++;
	}
	return $index;
);

Function get_airfiber_link_iface_index $cfg, $iface
(
	$index = 0; /* not found */
	$idx = 1;
	$devname = "dummy";

	while ($index == 0 && strlen($devname) != 0 && $idx <= 32) {
		$devname = cfg_get_def($cfg, "afnetconf.$idx.devname", "");
		if ($devname == $iface) {
			$index = $idx;
		}
		$idx++;
	}
	return $index;
);

Function get_wlan_index $iface
(
	return "1";
);

Function get_phyname $index
(
	return "af0";
);

Function set_wmode_af $cfg, $wmode, $tx_freq, $rx_freq, $duplex (
	$netmode = cfg_get_def($cfg, "netmode", "airfiber");
	$wireless = "slave";
	switch ($wmode)
	{
	case "aprepeater"; /* Should never happen */
	case "ap";
		$wireless = "master";
		break;
	case "sta";
	default;
                $wireless = "slave";
		break;
	};

	cfg_set($cfg, "ebtables.sys.status", "enabled");
	cfg_set($cfg, "ebtables.sys.arpnat.status", "disabled");
        cfg_set($cfg, "ebtables.sys.eap.status", "disabled");
	cfg_set($cfg, "radio.1.mode", $wireless);
        cfg_set($cfg, "radio.1.duplex", $duplex);
	cfg_set($cfg, "radio.1.tx_freq", $tx_freq);
	cfg_set($cfg, "radio.1.rx_freq", $rx_freq);
);

Function cfg_get_wmode $cfg, $wlan_iface (
	$idx = get_wlan_index($wlan_iface);
	$mode = strtolower(cfg_get_def($cfg, "radio.$idx.mode", "managed"));
	if ($mode == "master") {
		$result = "ap";
	} else {
		$result = "sta";
	}
	return $result;
);

Function set_essid $cfg, $idx, $essid (
	return cfg_set($cfg, "radio.$idx.linkname", $essid);
);

Function set_txpower $cfg, $idx, $power (
	return cfg_set($cfg, "radio.$idx.txpower", $power);
);

Function set_obey $cfg, $idx, $obey (
	cfg_del($cfg, "radio.$idx.regulatory");
	cfg_set($cfg, "radio.$idx.reg_obey", $obey);
	return cfg_set($cfg, "radio.$idx.obey", $obey);
);

Function set_country $cfg, $idx, $country, $subsystemid (
	$result = $cfg;
	if (strlen($country)) {
		if ($idx == 1) {
			cfg_set($cfg, "radio.countrycode", $country);
		}
		cfg_set($cfg, "radio.$idx.countrycode", $country);
		$result = cfg_set($cfg, "radio.$idx.subsystemid", $subsystemid);
	}
	return $result;
);

Function update_power_limits $cfg, $idx, $country (
	global $cmd_afrd;
	global $txpower_reg_max;
	global $txpower_max;
	global $txpower;

	$txpower_reg_max = 0;
	exec("$cmd_afrd power_max $country", $lines, $res);
	if ($res == 0) {
		$txpower_reg_max = $lines[0];
	}
	$txpower_max = $radio["txpower_max"];
	if(strlen($txpower)) {
		$txpower = adjust_txpower($txpower);
	}
);



Function set_af_key $cfg, $idx, $af_key, $af_key_type (
	if ($af_key_type == 2) {
		$af_key = "s:" + $af_key;
	}
	return cfg_set($cfg, "radio.1.key", $af_key);
);

Function set_rate_af $cfg, $idx, $rate, $auto (
	if (!strlen($auto)) {
		$auto = "disabled";
	}
	cfg_set($cfg, "radio.$idx.rate.auto", $auto);
	return cfg_set($cfg, "radio.$idx.rate", $rate);
);

Function cfg_get_essid $cfg, $idx, $essid (
	if (!strlen($essid)) {
		$essid = "UBNT";
	}
        return cfg_get_def($cfg, "radio.$idx.linkname", $essid);
);

Function cfg_get_country $cfg, $wlan_iface, $country (
	global $radio;
	if (count($radio) < 2) {
		init_board_inc($wlan_iface);
	}

	if ($radio["ccode_locked"] == 1 || $radio["ccode_fixed"] == 1) {
		$ret = $radio["ccode"];
	} else {
		if (!strlen($country)) {
			$country = $radio["ccode"];
			if (!strlen($country)) {
				$country = "840";
			}
		}
		$idx = get_wlan_index($wlan_iface);
		if ($idx == 1) {
			$key = "radio.countrycode";
		}
		else {
			$key = "radio.$idx.countrycode";
		}
		$ret = cfg_get_def($cfg, $key, $country);
	}

	return $ret;
);

Function cfg_get_txpower $cfg, $idx, $txpower (
	global $txpower_max;
        if (!strlen($txpower)) {
        	$txpower = $txpower_max;
        }
        return cfg_get_def($cfg, "radio.$idx.txpower", $txpower);
);


Function adjust_txpower $newtxpower (
	global $txpower_max;
	global $txpower_min;
	global $txpower_reg_max;

	if (!strlen($newtxpower)) {
		$newtxpower = 0;
	}
	$newtxpower = intval($newtxpower);
	if ($txpower_reg_max != 0) {
		if ($newtxpower > $txpower_reg_max) {
			$newtxpower = $txpower_reg_max;
		}
		if ($newtxpower == 0) {
			$newtxpower = $txpower_reg_max;
		}
	} 
	/* Check hardware limits */
	if (strlen($txpower_max)) {
		if ($newtxpower == 0) {
			$newtxpower = $txpower_max;
		}
		if ($newtxpower > $txpower_max) {
			$newtxpower = $txpower_max;
		} 
		if ($newtxpower < $txpower_min) {
			$newtxpower = $txpower_min;
		}
	}
	return $newtxpower;
);

Function cfg_get_adjusted_txpower $cfg, $idx, $oldtxpower (
	$newtxpower = cfg_get_txpower($cfg,$idx,$oldtxpower);
	return adjust_txpower($newtxpower);
);

Function cfg_get_rate_af $cfg, $wlan_iface, $rate (
        global $feature_airfiber;
	$idx = get_wlan_index($wlan_iface);
	if (!strlen($rate) || $rate == "8x" /* temporary workaround */) {
		$rate = "6x";
	}
	return cfg_get_def($cfg, "radio.$idx.rate", $rate);
);

Function cfg_get_security $cfg, $wlan_iface, $security, $wmode (
       	$sec = "AES-128";
	return $sec;
);

Function cfg_get_key_af $cfg, $idx (
	return cfg_get_def($cfg, "radio.1.key", $wep_key_id);
);

Function cfg_get_ipv4addr $cfg, $iface, $ip (
	if (!strlen($ip)) {
		$ip = if_get_ipaddr($iface);
	}
	$idx = get_iface_index($cfg, $iface);
	$ip = cfg_get_def($cfg, "netconf.$idx.ip", $ip);
	return $ip;
);

Function cfg_get_ipv4mask $cfg, $iface, $mask (
	if (!strlen($mask)) {
		$mask = "255.255.255.0";
	}
	$idx = get_iface_index($cfg, $iface);
	$mask = cfg_get_def($cfg, "netconf.$idx.netmask", $mask);
	return $mask;
);

Function cfg_get_ipv4gw $cfg, $iface, $gw (
	if (!strlen($gw)) {
		$gw = "0.0.0.0";
	}
	return cfg_get_def($cfg, "route.1.gateway", $gw);
);

Function cfg_get_firewall $cfg, $firewall, $netmode
(
	$tbl = "ebtables";
	if ($netmode != "bridge") {
		$tbl = "iptables";
	}
	$f = cfg_get_def($cfg, $tbl+".status", $firewall);
	$firewall_chain = cfg_get_def($cfg, $tbl+".sys.fw.status", $firewall);

	if ($f == "enabled" && $firewall_chain == "enabled")
	{
		$firewall = "enabled";
	}
	else {
		$firewall = "disabled";
	}
	return $firewall;
);

Function get_mgmt_info $cfg (
	$res["http"] = cfg_get_def($cfg, "httpd.port", "80");
	$res["airview"] = cfg_get_def($cfg, "airview.tcp_port", "18888");
	$res["icmp"] = "8";
	$res["sptest"] = "9";
	if (cfg_get_def($cfg, "sshd.status", "enabled") == "enabled") {
		$res["ssh"] = cfg_get_def($cfg, "sshd.port", "22");
	}
	if (cfg_get_def($cfg, "httpd.https.status", "disabled") == "enabled") {
		$res["https"] = cfg_get_def($cfg, "httpd.https.port", "443");
	}
	if (cfg_get_def($cfg, "telnetd.status", "disabled") == "enabled") {
		$res["telnet"] = cfg_get_def($cfg, "telnetd.port", "23");
	}        
        if (cfg_get_def($cfg, "snmp.status", "disabled") == "enabled") {
        	$res["snmp"] = "161";
        }
        if (cfg_get_def($cfg, "discovery.status", "enabled") == "enabled") {
        	$res["discover"] = "1001";
        }
	return $res;
);

Function cfg_update_dmz_mgmt $cfg (
	$netmode = cfg_get_def($cfg, "netmode", "bridge");
        if ($netmode != "bridge" &&
	    cfg_get_def($cfg, "iptables.status", "disabled") == "enabled" &&
	    cfg_get_def($cfg, "iptables.sys.status", "disabled") == "enabled" &&
	    cfg_get_def($cfg, "iptables.sys.dmz.status", "disabled") == "enabled" &&
	    cfg_get_def($cfg, "iptables.sys.dmz.1.except.status", "disabled") == "enabled")
	{
		$ports = get_mgmt_info($cfg);
		Reset($ports);
		$i = 1;
		$c = count($ports);
		while($i <= $c);
			$key = key($ports);
			$proto = "TCP";
			if ($key == "snmp" || $key == "sptest") {
				$proto = "UDP";
			}
			$port = $ports[$key];
			if ($key == "icmp") {
				$proto = "ICMP";
			}
			cfg_set($cfg, "iptables.sys.dmz.1.except."+$i+".port", $port);
			cfg_set($cfg, "iptables.sys.dmz.1.except."+$i+".proto", $proto);
			cfg_set($cfg, "iptables.sys.dmz.1.except."+$i+".status", "enabled");
			next($ports);
			$i++;
		endwhile;
		while($i <= 8);
			if (cfg_get_def($cfg, "iptables.sys.dmz.1.except."+$i+".status", "disabled") == "enabled")
			{
				cfg_set($cfg, "iptables.sys.dmz.1.except."+$i+".status", "disabled");
			}
			$i++;
		endwhile;
        }
);

Function generate_frequency_list $name, $country
(
	global $cmd_afrd;
	echo "/* airfiber frequencies for $country */\n";
	echo ""+$name+" = [\n";
	PassThru($cmd_afrd + "freq_list $country");
	echo " ];\n";
);

Function generate_speed_list $name
(
	global $cmd_af;
	echo "/* airfiber speeds */\n";
	echo ""+$name+" = [\n";
        PassThru($cmd_af + "list speed | sed -r -e 's~^~\"~;s~,~,\"~g;s~x~x\"~g;s~,\"8x\"~~' "); /* stripping 8x away is a temporary workaround */
	/* workaround for explorer array termination (,) problem: one extra element at the end. */
	echo "];\n";
);

Function module_loaded $module
(
	global $proc_modules;
	$lines = @file($proc_modules);
	if ($lines == "-1" || count($lines) == 0 || strlen($module) == 0) {
		$result = -1;
	}
	else {
		$result = 0;
		$c = count($lines);
		$l = strlen($module);
		while ($c) {
			$c--;
			if (substr($lines[$c], 0, $l) == $module) {
				$result = 1;
				$c = 0;
			}
		}
	}
	return $result;
);

Function is_test
(
	global $test_lock_file;
	$result = 1;
	if (fileinode($test_lock_file) == -1) {
		$result = 0;
	} else {
		$fp = @fopen($test_lock_file, "r");
		if ($fp != -1) {
			$result = @fgets($fp, 10);
			$result = intval($result);
			@fclose($fp);
		}
	}
	return $result;
);

Function is_testmode_active
(
	global $test_lock_file;
	$result = 0;
	if (substr(sprintf("%o",filePerms($test_lock_file)), 3, 3) == "755") {
		$result = 1;
	}
	return $result;
);

Function cfg_get_vlan_status $cfg, $iface, $vlan_status (
	if ($vlan_status == "on" || $vlan_status == "enabled")
	{
		$vlan_status = "enabled";
	}
	else
	{
		$vlan_status = "disabled";
	}
	$enabled = cfg_get_def($cfg, "vlan.status", $vlan_status);
	$vlan_status = cfg_get_def($cfg, "vlan.1.status", $vlan_status);

	if ($enabled != "enabled" || $vlan_status != "enabled")
	{
		$vlan_status = "disabled";
	}
	return $vlan_status;
);

Function cfg_get_vlan_tag $cfg, $iface, $vlan_tag (
	return cfg_get_def($cfg, "vlan.1.id", $vlan_tag);
);

Function cfg_get_vlan_ifc $cfg, $iface, $vlan_ifc (
	global $wlan_iface;

	$netmode = cfg_get_def($cfg, "netmode", "bridge");
	$ifc = cfg_get_def($cfg, "vlan.1.devname", $iface);
	if ($netmode == "bridge") {
		if ($ifc == $wlan_iface) {
			return "wlan";
		} else {
			return "lan";
		}
	} else {
		if ($ifc == $iface) {
			return "wan";
		} else {
			return "lan";
		}
	}
);

Function init_board_inc $iface
(
	global $radio;
	$keys[] = "name";
	$keys[] = "shortname";
	$keys[] = "bus";
	$keys[] = "ccode";
	$keys[] = "ccode_locked";
	$keys[] = "ccode_fixed";
	$keys[] = "subsystemid";
	$keys[] = "subvendorid";
	$keys[] = "txpower_max";
	$keys[] = "txpower_min";
	$keys[] = "def_antenna";
	$keys[] = "caps";
	$keys[] = "chains";
	$keys[] = "airfiber";
	$keys[] = "antennas";

	$idx = get_wlan_index($iface);
	$radio["index"] = $idx;

	$i = 0;
	while ($i < count($keys)) {
		$cfg_var = "radio$idx" + "_$keys[$i]";
		global $$cfg_var;
		$radio[$keys[$i]] = $$cfg_var;
		$i++;
	}

	$i = 0;
	while ($i < count($idx_keys)) {
		$cfg_var = "radio$idx" + "_$idx_keys[$i]";
		global $$cfg_var; $arr = $$cfg_var;
		$j = 0;
		while ($j < count($$cfg_var)) {
			$key_name = $idx_keys[$i]+ "_$j";
			$radio[$key_name] = $arr[$j];
			$j++;
		}
		$i++;
	}
);

Function get_status $status_value
(
	$status = "disabled";
	if (strlen($status_value)) {
		$status = "enabled";
	}
	return $status;
);

Function change_country $cfg, $idx, $country, $subsystemid
(
	global $cfg_file, $cmd_af;
	set_country($cfg, $idx, $country, $subsystemid);
	cfg_save($cfg, $cfg_file);
	exec("$cmd_af set countrycode $country", $lines, $res);
);

Function cfg_put $f_name, $str
(
	$res = 0;
	$f = @fopen($f_name, "w");
	if ($f != -1) {
		$str = ereg_replace(13, "", $str);
		fputs($f, $str);
		fclose($f);
		cfg_set_modified($f_name);
	} else {
		$res = -2;
	}
        return $res;
);

Function fill_eth_speed
(
	echo "<option value=\"0\">" + dict_translate("Auto") + "</option>";
	echo "<option value=\"1\">" + dict_translate("100Mbps-Full") + "</option>";
	echo "<option value=\"2\">" + dict_translate("100Mbps-Half") + "</option>";
	echo "<option value=\"3\">" + dict_translate("10Mbps-Full") + "</option>";
	echo "<option value=\"4\">" + dict_translate("10Mbps-Half") + "</option>";
);

Function fill_eth_speed_gige
(
	echo "<option value=\"0\">" + dict_translate("Auto") + "</option>";
	/* echo "<option value=\"1\">" + dict_translate("1000Mbps-Full") + "</option>"; */
	echo "<option value=\"3\">" + dict_translate("100Mbps-Full") + "</option>";
	echo "<option value=\"4\">" + dict_translate("100Mbps-Half") + "</option>";
	echo "<option value=\"5\">" + dict_translate("10Mbps-Full") + "</option>";
	echo "<option value=\"6\">" + dict_translate("10Mbps-Half") + "</option>";
);

Function get_eth_speed $cfg, $ifname
(
	$speed = 0;
	$idx = get_iface_index($cfg, $ifname);
	if ($idx > 0) {
		$eth_autoneg = cfg_get_def($cfg, "netconf.$idx.autoneg", "enabled");
		if ($eth_autoneg != "enabled") {
			$eth_duplex = cfg_get_def($cfg, "netconf.$idx.duplex", "enabled");
			$eth_speed = cfg_get_def($cfg, "netconf.$idx.speed", "100");
			if ($eth_speed == "100") {
				$speed = 1;
			}
			elseif ($eth_speed == "10") {
				$speed = 3;
			}
			if ($speed > 0 && $eth_duplex != "enabled") {
				$speed += 1;
			}
		}
	}

	return $speed;
);

Function set_eth_speed $cfg, $ifname, $ifspeed
(
	$idx = get_iface_index($cfg, $ifname);
	if ($idx > 0) {
		$speed_int = IntVal($ifspeed);
		if ($speed_int == 0) {
			cfg_set($cfg, "netconf.$idx.autoneg", "enabled");
                        cfg_del($cfg, "netconf.$idx.duplex");
                        cfg_del($cfg, "netconf.$idx.speed");
		}
		else {
			if ($speed_int % 2 == 1) {
				$duplex = "enabled";
			}
			else {
				$duplex = "disabled";
			}

			if ($speed_int <= 2) {
				$speed = 100;
			}
			else {
				$speed = 10;
			}

			cfg_set($cfg, "netconf.$idx.autoneg", "disabled");
			cfg_set($cfg, "netconf.$idx.duplex", $duplex);
			cfg_set($cfg, "netconf.$idx.speed", $speed);
		}
	}
);

Function get_eth_speed_af_data $cfg, $ifname
(
        $idx = get_airfiber_link_iface_index($cfg, $ifname);
	$speed = 0;
	$eth_autoneg = cfg_get_def($cfg, "afnetconf.$idx.autoneg", "enabled");
	if ($eth_autoneg != "enabled") {
		$eth_duplex = cfg_get_def($cfg, "afnetconf.$idx.duplex", "enabled");
		$eth_speed  = cfg_get_def($cfg, "afnetconf.$idx.speed", "100");
		if ($eth_speed == "1000") {
			$speed = 1;
		}
		elseif ($eth_speed == "100") {
			$speed = 3;
		}
		elseif ($eth_speed == "10") {
			$speed = 5;
		}
		if ($speed > 0 && $eth_duplex != "enabled") {
			$speed += 1;
		}
	}

	return $speed;
);

Function set_eth_speed_af_data $cfg, $ifname, $ifspeed
(
        $idx = get_airfiber_link_iface_index($cfg, $ifname);
	$speed_int = IntVal($ifspeed);
	if ($speed_int == 0) {
                cfg_set($cfg, "afnetconf.$idx.devname", "af0");
		cfg_set($cfg, "afnetconf.$idx.autoneg", "enabled");
		cfg_del($cfg, "afnetconf.$idx.duplex");
		cfg_del($cfg, "afnetconf.$idx.speed");
	}
	else {
		if ($speed_int % 2 == 1) {
			$duplex = "enabled";
		}
		else {
			$duplex = "disabled";
		}

		if ($speed_int <= 2) {
			$speed = 1000;
		}
		elseif ($speed_int <= 4) {
			$speed = 100;
		}
		else {
			$speed = 10;
		}

                cfg_set($cfg, "afnetconf.$idx.devname", "af0");
		cfg_set($cfg, "afnetconf.$idx.autoneg", "disabled");
		cfg_set($cfg, "afnetconf.$idx.duplex", $duplex);
		cfg_set($cfg, "afnetconf.$idx.speed", $speed);
	}
);

Function get_role_index $cfg, $role
(
	$index = 0; /* not found */
	$idx = 1;
	$devname = "dummy";

	while ($index == 0 && strlen($devname) != 0 && $idx <= 32) {
		$devname = cfg_get_def($cfg, "netconf.$idx.devname", "");
		$devrole = cfg_get_def($cfg, "netconf.$idx.role", "");
		if ($devrole == $role) {
			$index = $idx;
		}
		$idx++;
	}
	return $index;
);

>
