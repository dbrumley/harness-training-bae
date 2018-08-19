<?
	$ccode_include_fail = 0;
	if (fileSize("/etc/ccodes.inc") < 1) {
		global $cmd_regdomain;
		$def_cntry_output = "<option value=\"840\">United States</option>";

		$fd_in = popen ($cmd_afrd + "ccodes_inc", "r");
		if ($fd_in == -1) {
			echo $def_cntry_output;
			$ccode_include_fail = 1;
		}
		$fd_out = fopen("/etc/ccodes.inc", "w");
		if ($fd_out == -1) {
			echo $def_cntry_output;
			$ccode_include_fail = 1;
		}
		$cont = 1;
		$size = 0;
		while ($cont > 0) {
			$buf = fgets($fd_in, 1024);
			fputs($fd_out, $buf);
			$len = strlen($buf);
			$size += $len;
			if (!$len) { $cont = 0; }
		}
		if ($size == 0) {
			echo $def_cntry_output;
			$ccode_include_fail = 1;
		}
		fclose($fd_out);
		pclose($fd_in);
	}
	if (!$ccode_include_fail) {
		include("/etc/ccodes.inc"); }
>
