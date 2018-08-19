var AFMeterMax=50;var colors=["#d2001b","#e0201a","#f2541b","#f8901e","#fac922","#faeb26","#eaed26","#d3ed25","#b9ed25","#9bee25","#7fe726","#64dd26","#4cd228","#3ac82a","#2ec02d","#28ba2f"];function update_meter(b,d,c){var a=Math.floor(100*d/c);if(a>100){a=100}$("#"+b).css({width:""+a+"%"}).show()}function log10(a){return(Math.log(a)/Math.log(10))}function getAirFiberMinSignal(){return -85}function getAirFiberMaxSignal(){return AFMeterMax}function updateAirFiberSignalLevelsForChain(d,e,b,f,a,c){if(f){if(c||a==1000){$("#"+e+b+"_bar").hide();$("#"+e+b+"_bar_border").hide();$("#"+e+b+"_spacer").hide();$("#"+e+b+"_value").html("<span class='overload'>"+l10n_get("Overload")+"</span>");$("#"+e+b+"_value").show();$("#"+e+b+"_row").show()}else{if(d&&a!=-1000){$("#"+e+b+"_bar").show();$("#"+e+b+"_bar_border").show();$("#"+e+b+"_spacer").show();$("#"+e+b+"_value").html(a+"&nbsp;"+l10n_get("dBm"));$("#"+e+b+"_value").show();$("#"+e+b+"_row").show();update_meter(e+b+"_bar",((d&&a>getAirFiberMinSignal())?(a-getAirFiberMinSignal()):getAirFiberMinSignal()),getAirFiberMaxSignal())}else{$("#"+e+b+"_bar").show();$("#"+e+b+"_bar_border").show();$("#"+e+b+"_spacer").show();$("#"+e+b+"_value").html("&nbsp;-");$("#"+e+b+"_value").show();$("#"+e+b+"_row").show();update_meter(e+b+"_bar",getAirFiberMinSignal(),getAirFiberMaxSignal())}}}else{$("#"+e+b+"_row").hide()}}function updateAirFiberTemperature(a,b){$("#dactemp"+a).text(b+" \u00B0C ("+(Math.round(b*9/5)+32)+" \u00B0F)")}function updateAirFiberSignalLevels(a,c){var b=(c.linkstate=="operational");updateAirFiberSignalLevelsForChain(b,"signal",0,!!(a&1),c.rxpower0,c.rxoverload0);updateAirFiberSignalLevelsForChain(b,"signal",1,!!(a&2),c.rxpower1,c.rxoverload1);updateAirFiberTemperature(0,c.dactemp0);updateAirFiberTemperature(1,c.dactemp1);updateAirFiberSignalLevelsForChain(b,"remote_signal",0,b&&c.remote_rxpower0valid,c.remote_rxpower0,c.remote_rxoverload0);updateAirFiberSignalLevelsForChain(b,"remote_signal",1,b&&c.remote_rxpower1valid,c.remote_rxpower1,c.remote_rxoverload1)};