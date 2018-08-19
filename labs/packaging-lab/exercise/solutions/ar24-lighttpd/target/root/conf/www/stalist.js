var mainTable;var _cols={mac:0,name:1,signal:2,beam:3,ack:4,txrx:5,ccq:6,uptime:7,ip:8,action:9,rate_count:10,aprepeater:11};var _initialized=false;function handleError(b,c,a){if(b&&b.status!=200&&b.status!=0){window.location.reload()}}function kickEnd(a,c,b){$(this).enable();refreshStaList()}function kickStation(b,e,d){$(b).parent().parent("tr").hide();var c="/stakick.cgi?staif="+e+"&staid="+d;jQuery.ajax({url:c,cache:false,dataType:"json",success:kickEnd,error:handleError});return false}function refreshStaList(){$.ajax({cache:false,url:"/sta.cgi",dataType:"json",success:showStaList,error:handleError,complete:function(a,b){if(b!="success"){refreshStaList()}}})}function refreshAll(){if(typeof reloadStatus=="function"){reloadStatus()}refreshStaList()}function formatDistance(e){var d=(e<150)?150:e;var b=toFixed(d/1000,1);var a=toFixed(d/1609.344,1);var c=[a,"miles","("+b,"km)"];return c.join(" ")}function getStaInfo(b){var a=[b.mac,b.name,b.signal+" / "+b.noisefloor,(b.airmax.beam<sl_global.beam_angles.length?sl_global.beam_angles[b.airmax.beam]:sl_global.beam_angles[sl_global.beam_angles.length-1]),formatDistance(sl_global.autoack?(b.ack>0?b.distance:sl_global.distance):0),b.tx+" / "+b.rx,b.ccq,b.uptime,b.lastip,0,b.rates.length,b.aprepeater];return a}function showStaList(b){mainTable.fnClearTable();for(var d=0;d<b.length;++d){var c=b[d];var e=c.mac.replace(/:/g,"");var a=mainTable.fnAddData(getStaInfo(c),true)}}function tableCell(b,c){var a=mainTable.oApi._fnColumnIndexToVisible(mainTable.fnSettings(),c);if(a==null){return $()}return $("td",b).eq(a)}function updateMac(e,c){var a=c[_cols.rate_count]>8?520:400;var d="openPage('stainfo.cgi?ifname="+sl_global.wlan_iface;d+="&sta_mac="+c[_cols.mac]+"', 700, "+a+");";var b='<a href="#" onClick="'+d+'">'+c[_cols.mac]+"</a>";b+=((c[_cols.aprepeater]==0)?"":"&nbsp;("+$.l10n._("AP-Repeater")+")");b+="&nbsp;&nbsp;&nbsp;";tableCell(e,_cols.mac).html(b)}function updateName(b,a){if(a[_cols.name].length>0){tableCell(b,_cols.name).text(a[_cols.name])}else{tableCell(b,_cols.name).html("&nbsp;")}}function updateCcq(b,a){if(a[_cols.ccq]<=0){tableCell(b,_cols.ccq).text("-")}}function updateUptime(c,b){var a=secsToCountdown(b[_cols.uptime],$.l10n._("day"),$.l10n._("days"));tableCell(c,_cols.uptime).text(a)}function updateIp(c,b){var a=b[_cols.ip]!="0.0.0.0"?'<a href="http://'+b[_cols.ip]+'" target="_blank">'+b[_cols.ip]+"</a>":$.l10n._("unknown");tableCell(c,_cols.ip).html(a)}function updateAction(c,a){var b="&nbsp;";if(a[_cols.aprepeater]==0){b='<a href="#" onClick="return kickStation(this, \''+sl_global.wlan_iface+"', '"+a[_cols.mac]+"');\">kick</a>"}tableCell(c,_cols.action).html(b)}function updateRow(d,c,a,b){updateMac(d,c);updateName(d,c);updateCcq(d,c);updateUptime(d,c);updateIp(d,c);updateAction(d,c);return d}$(document).ready(function(){if(_initialized){return}else{_initialized=true}$.l10n.init({dictionary:l10n_stalist});$("#_refresh").click(refreshAll);$("#sta_list th").removeClass("initial_hide");mainTable=$("#sta_list").dataTable({aaSorting:[[1,"asc"]],bLengthChange:false,bPaginate:false,bFilter:false,bInfo:false,bSortClasses:false,bAutoWidth:false,oLanguage:{sEmptyTable:$.l10n._("Loading, please wait...")},fnRowCallback:updateRow,fnInitComplete:function(a){a.oLanguage.sEmptyTable=$.l10n._("No Associated Stations")},aoColumnDefs:[{sClass:"centered",aTargets:[_cols.signal,_cols.beam,_cols.ack,_cols.txrx,_cols.ccq,_cols.action]},{sClass:"uptime",aTargets:[_cols.uptime]},{bSortable:false,aTargets:[_cols.action]},{bVisible:false,aTargets:[_cols.rate_count,_cols.aprepeater]},{bVisible:sl_global.autoack,aTargets:[_cols.ack]},{bVisible:(sl_global.phased_array&&sl_global.airmax_on),aTargets:[_cols.beam]},{sType:"string",aTargets:[_cols.beam]},{sType:"rate",aTargets:[_cols.txrx]},{sType:"signal",aTargets:[_cols.signal]}]});refreshStaList()});$.fn.dataTableExt.aTypes.push(function(a){if(/^\d{1,3}[\.]\d{1,3}[\.]\d{1,3}[\.]\d{1,3}$/.test(a)){return"ip-address"}return null});$.fn.dataTableExt.oApi.fnSortByIp=function(g,f,h){var c=g.split(".");var a=f.split(".");var e=h?-1:1;for(var d=0;d<c.length&&d<a.length;++d){var b=parseInt(c[d]),j=parseInt(a[d]);if(b!=j){return((b<j)?e:-e)}}return 0};$.fn.dataTableExt.oSort["ip-address-asc"]=function(d,c){return $.fn.dataTableExt.oApi.fnSortByIp(d,c,true)};$.fn.dataTableExt.oSort["ip-address-desc"]=function(d,c){return $.fn.dataTableExt.oApi.fnSortByIp(d,c,false)};$.fn.dataTableExt.oApi.fnSortByRate=function(c,b,h){var e=c.split(/\s+/);var a=b.split(/\s+/);var g=h?-1:1;for(var f=0;f<e.length&&f<a.length;++f){var d=Number(e[f]);if(isNaN(d)){d=0}var j=Number(a[f]);if(isNaN(j)){j=0}if(d!=j){return((d<j)?g:-g)}}return 0};$.fn.dataTableExt.oSort["rate-asc"]=function(d,c){return $.fn.dataTableExt.oApi.fnSortByRate(d,c,true)};$.fn.dataTableExt.oSort["rate-desc"]=function(d,c){return $.fn.dataTableExt.oApi.fnSortByRate(d,c,false)};$.fn.dataTableExt.oSort["signal-asc"]=function(d,c){return $.fn.dataTableExt.oApi.fnSortByRate(d,c,true)};$.fn.dataTableExt.oSort["signal-desc"]=function(d,c){return $.fn.dataTableExt.oApi.fnSortByRate(d,c,false)};