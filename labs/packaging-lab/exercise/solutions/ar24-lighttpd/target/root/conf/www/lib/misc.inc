<?

Function is_first_login $cfg, $idx, $uri (
	if (cfg_get_def($cfg, "radio.$idx.countrycode", 0) != 0) {
		$retval = 0;
	}
	else {
		if (isset($uri) && strstr($uri, "test.cgi") > 0) {
			$retval = 0;
		}
		else {
			$retval = 1;
		}
	}
	return $retval;
);

Function devname2ifname $ifname (
    $dev = ereg_replace("air0", "AIRCONFIG", $ifname);
    $dev = ereg_replace("eth0", "CONFIG",    $dev);
    $dev = ereg_replace("af0",  "DATA",      $dev);
    $dev = ereg_replace("br0",  "MGMT",      $dev);
    return $dev;
);

function get_bridges_list (
	$netif = "/sys/class/net";
	if (fileinode($netif) != -1)
	{
	      @openDir($netif);
	      $f = readDir();
	      while (strlen($f) != 0 ) {
      		if ($f != "." && $f != "..") {
              		if (fileinode($netif + "/" + $f + "/bridge") != -1) {
                        	$brifc[count($brifc)] = $f;
	      		}
              	}
                $f = readDir();
              }
              @closeDir();
      	}
        return $brifc;
);

function br_portno2ifc $brname, $portno (
	$ifc = "";
	$brif = "/sys/class/net/" + $brname + "/brif";
	if (fileType($brif) == "dir")
	{
        	$done = 0;
		@openDir($brif);
		$f = readDir();
		while (strlen($f) != 0 && !$done) {
			if ($f != "." && $f != "..") {
                        	$port = $brif + "/" + $f + "/port_no";
                                $fp = @fopen($port, "r");
				if ($fp != -1)
				{
	                                $no = fgets($fp, 10);
                                        if (intVal($portno) == HexDec($no)) {
                                        	$done = 1;
                                                $ifc = $f;
                                        }
                                        @fclose($fp);
				}
			}
			$f = readDir();
		}
		@closeDir();
        }
        return $ifc;
);

Function get_chain_names $cfg
(
	$chain_names[0] = dict_translate("Chain 0");
	$chain_names[1] = dict_translate("Chain 1");
	return $chain_names;
);

>
