var channel = new MessageChannel();
var port1 = channel.port1;
var iframe = document.querySelector('iframe');
iframe.addEventListener("load", onLoad);

function onLoad() {
    // Listen for button clicks
    var timeframe = [2020, 2050, 2100];
    var total_co2emissions_lr_count = 0;
    $(".next-2").click(function () {
        if (total_co2emissions_lr_count < 2) {
            total_co2emissions_lr_count = total_co2emissions_lr_count + 1;
            port1.postMessage([2005, timeframe[total_co2emissions_lr_count]]);
        }
    });
    $(".back-2").click(function () {
        if (total_co2emissions_lr_count > 0) {
            total_co2emissions_lr_count = total_co2emissions_lr_count - 1;
            port1.postMessage([2005, timeframe[total_co2emissions_lr_count]]);
        }
    });


    // Transfer port2 to the iframe
    iframe.contentWindow.postMessage('init', '*', [channel.port2]);
    port1.postMessage([2005, 2020]);
}
