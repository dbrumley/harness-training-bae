#!/sbin/cgi
<?
include("lib/settings.inc");
$cfg = @cfg_load($cfg_file_bak);
include("lib/l10n.inc");
include("lib/misc.inc");

$chain_names = get_chain_names($cfg);
$chain1_name = $chain_names[0];
$chain2_name = $chain_names[1];
>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
  <title><? echo get_title($cfg, dict_translate("Antenna Alignment Tool")); ></title>
  <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
  <link href="/130904.1419/style.css" rel="stylesheet" type="text/css" />
  <script type="text/javascript" language="javascript" src="jsl10n.cgi"></script>
  <script type="text/javascript" src="/130904.1419/js/jquery.js"></script>
  <script type="text/javascript" language="javascript" src="/130904.1419/signal.js"></script>
  <script type="text/javascript" language="javascript" src="/130904.1419/slider-min.js"></script>
  <link type="text/css" rel="StyleSheet" href="/130904.1419/bluecurve.css" />
  <script type="text/javascript" language="javascript">
var timerID = null;
var lastSignal = null;

function reloadSignal() {
	timerID = null;
	jQuery.getJSON("status.cgi?"+(new Date().getTime()), update);
}

function refreshDisplay(s)
{
	lastSignal = s;
	$('#signal0_barinfo').toggle(s != null && s.airfiber.rxpower0 != 0);
	$('#signal1_row').toggle(s != null && s.airfiber.rxpower1 != 0);
    $('#remote_signal0_row').toggle(s != null && s.airfiber.remote_rxpower0valid != 0);
    $('#remote_signal1_row').toggle(s != null && s.airfiber.remote_rxpower1valid != 0);
    /*
    $('#remote_txpower_row').toggle(s != null && s.airfiber.remote_txpower != '--' && s.airfiber.remote_txpower != 'n/a' );
    $('#remote_txpower').text(s != null ? s.airfiber.remote_txpower : 'n/a');
    */
	if (typeof updateAirFiberSignalLevels == 'function' && s != null) {
		updateAirFiberSignalLevels(s.wireless.rx_chainmask, s.airfiber);
	}
}

function update(s) {
	refreshDisplay(s);
	if (timerID != null)
		clearTimeout(timerID);
	timerID = setTimeout('reloadSignal()', 250);
}

function createSlider() {
	var slider = new Slider(document.getElementById("slider-1"), document.getElementById("slider-input-1"));
	var rs     = document.getElementById("rssifield");
	var refsig = getAirFiberMinSignal();
	slider.setMaximum(65);
	slider.onchange = function() {
		var val = this.getValue();
		if (rs) {
			rs.value = refsig + val;
		}
		AFMeterMax = val;
		refreshDisplay(lastSignal);
	}
	rs.slider = slider;
	rs.onchange = function() {
		var intVal = parseFloat(this.value);
		noise  = getAirFiberMinSignal();
        intVal = -1 * (refsig - intVal);
		this.slider.setValue(intVal);
	}
	rs.onchange();
}

function init() {
	createSlider();
	reloadSignal();
}
jQuery(document).ready(init);

var l10n_lang = {
	'dBm': '<? echo dict_translate("dBm");>',
	'Overload': '<? echo dict_translate("Overload"); >',

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

//-->
</script>

</head>

<body class="popup">
<br />
<form action="#">
<table cellspacing="0" cellpadding="0" align="center" style="width: 490px;" class="popup">
	<tr><th><? echo dict_translate("Antenna Alignment"); ></th></tr>
	<tr>
	  <td>
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
        <!--
		<div id="remote_txpower_row" class="row">
			<span class="label"><? echo dict_translate("Remote Power:"); >&nbsp;</span>
			<span class="value" id="remote_txpower">&nbsp;</span>
		</div>
        -->
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
		<div class="row">
		  <span class="label"><? echo dict_translate("Max Signal:"); ></span>
		  <span class="value">
			<div class="slider" id="slider-1">
	          <input class="slider-input" id="slider-input-1" name="slider-input-1"/>
			</div>
			<input type="text" class="std_width" id="rssifield" name="rssifield" size="4" value="-20" />
			<span>&nbsp;<? echo dict_translate("dBm");></span>
		  </span>
		</div>
	  </td>
	</tr>
</table>
</form>
</body>
</html>
