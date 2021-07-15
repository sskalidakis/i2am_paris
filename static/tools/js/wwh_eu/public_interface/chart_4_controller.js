var channel_4 = new MessageChannel();
var port_4_1 = channel_6.port1;
// var iframe_1_1 = document.querySelector('iframe');
var iframe_4_1 = document.querySelector('#co2_ccs_ag_co2_reduction_viz_iframe');
iframe_4_1.addEventListener("load", onLoad);

function onLoad() {
    // Listen for button clicks
    var timeframe4_1 = [40, 60, 80,90];
    var co2_ccs_ag_co2_reduction_lr_count = 0;
    $(".next-5").click(function () {
        if (co2_ccs_ag_co2_reduction_lr_count < 3) {
            co2_ccs_ag_co2_reduction_lr_count = co2_ccs_ag_co2_reduction_lr_count + 1;
            port_4_1.postMessage([0, timeframe4_1[co2_ccs_ag_co2_reduction_lr_count]]);
        }
    });
    $(".back-5").click(function () {
        if (co2_ccs_ag_co2_reduction_lr_count > 0) {
            co2_ccs_ag_co2_reduction_lr_count = co2_ccs_ag_co2_reduction_lr_count - 1;
            port_4_1.postMessage([0, timeframe4_1[co2_ccs_ag_co2_reduction_lr_count]]);
        }
    });


    // Transfer port2 to the iframe
    iframe_4_1.contentWindow.postMessage('init', '*', [channel_4.port2]);
    port_4_1.postMessage([0, 40]);
}
