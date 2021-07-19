var channel_10 = new MessageChannel();
var port_10_1 = channel_10.port1;
var iframe_10_1 = document.querySelector('#hydrogen_electricity_comp_viz_iframe');
iframe_10_1.addEventListener("load", onLoad);

function onLoad() {
    // Listen for button clicks
    var timeframe10_1 = [2005, 2025, 2040, 2050];
    var hydrogen_el_comp_viz_iframe_lr_count = 1;
    $(".next-11").click(function () {
        if (hydrogen_el_comp_viz_iframe_lr_count < 3) {
            hydrogen_el_comp_viz_iframe_lr_count = hydrogen_el_comp_viz_iframe_lr_count + 1;
            port_10_1.postMessage([2005, timeframe10_1[hydrogen_el_comp_viz_iframe_lr_count]]);
        }
    });
    $(".back-11").click(function () {
        if (hydrogen_el_comp_viz_iframe_lr_count > 1) {
            hydrogen_el_comp_viz_iframe_lr_count = hydrogen_el_comp_viz_iframe_lr_count - 1;
            port_10_1.postMessage([2005, timeframe10_1[hydrogen_el_comp_viz_iframe_lr_count]]);
        }
    });


    // Transfer port2 to the iframe
    iframe_10_1.contentWindow.postMessage('init', '*', [channel_10.port2]);
    setTimeout(function(){   port_10_1.postMessage([2005, 2025]); }, 400);
}
